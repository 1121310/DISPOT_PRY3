# -*- coding: utf-8 -*-
"""
validacion_highs.py - Validacion cruzada con un segundo solver independiente.

Los modelos se construyen con gurobipy, se exportan en formato MPS estandar y se
resuelven con HiGHS (solver de codigo abierto, https://highs.dev), que no
comparte codigo con Gurobi. Se comparan:
  * cada programa lineal del metodo LP iterativo (las iteraciones registradas
    en resultados/lp_<caso>.json), y
  * el MILP big-M de cada sistema.
El MINLP bilineal es no convexo y HiGHS no lo admite; su validacion
independiente es la enumeracion exhaustiva (fuerza_bruta.py) y la coincidencia
con el MILP.

Requiere:  pip install highspy
Uso:       python validacion_highs.py
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

import tnep_lp
import tnep_milp_bigm
from tnep_comun import big_m_corredores, cargar_sistema, entorno_gurobi, guardar_json, texto_plan

CARPETA = Path(__file__).resolve().parent
RESULTADOS = CARPETA / "resultados"
CASOS = ["garver6_tnep", "garver6_15corredores", "sur46_sin_redespacho"]


def resolver_highs(ruta_mps: Path) -> dict:
    import highspy

    h = highspy.Highs()
    h.setOptionValue("output_flag", False)
    h.setOptionValue("mip_rel_gap", 0.0)
    h.setOptionValue("time_limit", 600.0)
    h.readModel(str(ruta_mps))
    t0 = time.perf_counter()
    h.run()
    estado = h.modelStatusToString(h.getModelStatus())
    valores = dict(zip(h.getLp().col_names_, h.getSolution().col_value))
    return dict(estado=estado, objetivo=h.getInfo().objective_function_value,
                tiempo_s=time.perf_counter() - t0, version=h.version(), valores=valores)


def indice(nombre: str) -> list[int]:
    """'w[3,2]' -> [3, 2]"""
    return [int(t) for t in nombre[nombre.index("[") + 1:-1].split(",")]


def plan_milp_highs(sis, valores: dict) -> list[int]:
    """Lineas por corredor segun las binarias w[c,k] de la solucion de HiGHS."""
    plan = [0] * sis.nc
    for nombre, valor in valores.items():
        if nombre.startswith("w[") and valor > 0.5:
            c, k = indice(nombre)
            plan[c] = k
    return plan


def corredor_elegido_highs(sis, valores: dict, tol: float = 1e-6):
    """Corredor que reforzaria la regla de redondeo con la solucion LP de HiGHS."""
    lineas_eq = np.zeros(sis.nc)
    for nombre, valor in valores.items():
        if nombre.startswith(("Pmas[", "Pmenos[")):
            lineas_eq[indice(nombre)[0]] += valor
    lineas_eq /= sis.c_pmax
    return None if lineas_eq.max() <= tol else sis.c_id[int(np.argmax(lineas_eq))]


def main():
    carpeta = RESULTADOS / "highs"
    carpeta.mkdir(parents=True, exist_ok=True)
    env = entorno_gurobi(RESULTADOS / "logs" / "validacion_highs.log")
    salida = dict(lp=[], milp=[])
    for caso in CASOS:
        ruta = CARPETA / "datos" / f"{caso}.xlsx"
        sis = cargar_sistema(ruta)
        # --- LP iterativo: re-resolver cada iteracion registrada ---
        historia = json.loads((RESULTADOS / f"lp_{caso}.json").read_text(encoding="utf-8"))["historia"]
        for h in historia:
            m, _ = tnep_lp.construir_lp(sis, np.array(h["n"]), env)
            mps = carpeta / f"lp_{caso}_iter{h['iteracion']}.mps"
            m.write(str(mps))
            r = resolver_highs(mps)
            eleccion = corredor_elegido_highs(sis, r["valores"])
            salida["lp"].append(dict(caso=caso, iteracion=h["iteracion"], gurobi=h["objetivo"],
                                     highs=r["objetivo"], estado=r["estado"],
                                     diferencia=abs(r["objetivo"] - h["objetivo"]),
                                     refuerzo_gurobi=h.get("corredor_elegido"), refuerzo_highs=eleccion,
                                     mismo_refuerzo=eleccion == h.get("corredor_elegido")))
        # --- MILP big-M con los parametros de la base de datos ---
        res_milp = json.loads((RESULTADOS / f"milp_{caso}.json").read_text(encoding="utf-8"))
        M, _ = big_m_corredores(sis)
        m, _ = tnep_milp_bigm.construir_milp(sis, env, M)
        mps = carpeta / f"milp_{caso}.mps"
        m.write(str(mps))
        r = resolver_highs(mps)
        plan_h = plan_milp_highs(sis, r["valores"])
        salida["milp"].append(dict(caso=caso, gurobi=res_milp["objetivo"], highs=r["objetivo"],
                                   estado=r["estado"], tiempo_highs_s=r["tiempo_s"],
                                   tiempo_gurobi_s=res_milp["estadisticas"]["tiempo_s"],
                                   diferencia=abs(r["objetivo"] - res_milp["objetivo"]),
                                   plan_gurobi=res_milp["plan_texto"], plan_highs=texto_plan(sis, plan_h),
                                   mismo_plan=plan_h == res_milp["plan"]))
        salida["version_highs"] = r["version"]
    env.dispose()
    guardar_json(salida, RESULTADOS / "validacion_highs.json")
    print(f"HiGHS {salida['version_highs']}")
    for f in salida["milp"]:
        print(f"MILP {f['caso']:22s} Gurobi {f['gurobi']:10.4f}  HiGHS {f['highs']:10.4f}  "
              f"({f['estado']}, {f['tiempo_highs_s']:.2f} s)  dif = {f['diferencia']:.2e}  "
              f"mismo plan: {'si' if f['mismo_plan'] else 'NO'}")
        print(f"     plan HiGHS: {f['plan_highs']}")
    peor = max(salida["lp"], key=lambda f: f["diferencia"])
    iguales = sum(f["mismo_refuerzo"] for f in salida["lp"])
    print(f"LP: {len(salida['lp'])} programas lineales re-resueltos; maxima diferencia "
          f"{peor['diferencia']:.2e} ({peor['caso']}, iteracion {peor['iteracion']}); "
          f"mismo corredor reforzado en {iguales}/{len(salida['lp'])}")
    for f in salida["lp"]:
        print(f"   {f['caso']:22s} iter {f['iteracion']:2d}: Gurobi {f['gurobi']:9.4f}  HiGHS {f['highs']:9.4f}  "
              f"refuerzo {str(f['refuerzo_gurobi']):>6s} / {str(f['refuerzo_highs']):>6s}")


if __name__ == "__main__":
    main()
