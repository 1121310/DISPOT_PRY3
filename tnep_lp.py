# -*- coding: utf-8 -*-
"""
tnep_lp.py - METODO 1: modelo LP iterativo de Villasana-Garver
(Villasana, Garver y Salon, IEEE Trans. PAS, 1985), resuelto con Gurobi.

En cada iteracion se resuelve el programa lineal (ecs. 3-7 de TNEP.pdf):

    min   sum_k  c_k (P+_k + P-_k)                       (3)
    s.a.  PG - B_a theta_a + K P+ - K P- = PL             (4)
          PF = T theta = X H theta_a                      (5)
          -PF_max <= PF <= PF_max                         (6)
          P+, P- >= 0 ;  theta_ref = 0                    (7)

La red existente (y las lineas ya agregadas) cumple las dos leyes de
Kirchhoff y sus limites de capacidad; los corredores candidatos actuan como
"trayectorias de sobrecarga" de Garver (1970): solo cumplen la primera ley,
no tienen limite y cada pu de flujo cuesta c_k. Tras resolver se agrega UNA
linea en el corredor mas necesario (mayor flujo de sobrecarga) y se repite
hasta que P+ y P- se anulan (procedimiento de redondeo, "round-up").

Generalizacion (identica a TNEP.pdf cuando Pmax = 1 pu = 100 MW):
  * El costo por pu de sobrecarga es c_k / Pmax_k (costo por unidad de
    capacidad), y el corredor mas necesario es el que requiere mas lineas
    equivalentes (P+ + P-)/Pmax_k. Criterio alternativo 'costo':
    c_k (P+ + P-)/Pmax_k.
  * Los corredores que alcanzan n_max dejan de aceptar sobrecarga.
  * Las barras sin conexion electrica en la red actual se fijan en theta = 0
    (como theta_6 en la primera iteracion del documento).

Uso:
    python tnep_lp.py --datos datos/garver6_tnep.xlsx
    python tnep_lp.py --datos datos/sur46_sin_redespacho.xlsx --criterio costo
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

import numpy as np

from tnep_comun import (GRB, cargar_sistema, costo_plan, encabezado, entorno_gurobi,
                        estadisticas, exportar_modelo, flujo_dc, gp, guardar_json, nombre_estado,
                        perdidas_estimadas, ramas_activas, tabla_flujos, texto_plan)

CARPETA = Path(__file__).resolve().parent


# <<modelo_lp
def construir_lp(sis, n_adic, env):
    """Programa lineal de Villasana-Garver para la red con `n_adic` lineas nuevas."""
    m = gp.Model("TNEP_LP_Villasana_Garver", env=env)
    ramas = ramas_activas(sis, n_adic)           # red existente + lineas agregadas
    grado = np.zeros(sis.nb, dtype=int)
    for r in ramas:
        grado[r["de"]] += 1
        grado[r["a"]] += 1

    # Variables: angulos (libres), flujos en ramas (acotados) y sobrecargas
    theta = m.addVars(sis.nb, lb=-GRB.INFINITY, ub=GRB.INFINITY, name="theta")
    for i in range(sis.nb):                       # referencia y barras aisladas
        if i == sis.ref or grado[i] == 0:
            theta[i].lb = theta[i].ub = 0.0
    pf = m.addVars(len(ramas), lb=[-r["pmax"] for r in ramas],
                   ub=[r["pmax"] for r in ramas], name="PF")          # (6)
    abierto = [n_adic[k] < sis.c_nmax[k] for k in range(sis.nc)]
    p_mas = m.addVars(sis.nc, lb=0.0, ub=[GRB.INFINITY if a else 0.0 for a in abierto],
                      name="Pmas")                                     # (7)
    p_menos = m.addVars(sis.nc, lb=0.0, ub=[GRB.INFINITY if a else 0.0 for a in abierto],
                        name="Pmenos")

    # (5) Segunda ley de Kirchhoff en la red: PF = b (theta_i - theta_j)
    for e, r in enumerate(ramas):
        m.addConstr(pf[e] == r["b"] * (theta[r["de"]] - theta[r["a"]]), name=f"KVL_{r['etiqueta']}_{e}")

    # (4) Balance nodal: PG - B theta + K (P+ - P-) = PL
    salida = [gp.LinExpr() for _ in range(sis.nb)]
    for e, r in enumerate(ramas):
        salida[r["de"]] += pf[e]
        salida[r["a"]] -= pf[e]
    inyeccion = [gp.LinExpr() for _ in range(sis.nb)]
    for k in range(sis.nc):          # K: +1 en la barra 'Hasta', -1 en la barra 'Desde'
        inyeccion[sis.c_a[k]] += p_mas[k] - p_menos[k]
        inyeccion[sis.c_de[k]] -= p_mas[k] - p_menos[k]
    for i in range(sis.nb):
        m.addConstr(sis.pg[i] - salida[i] + inyeccion[i] == sis.pl[i],
                    name=f"balance_{sis.barras[i]}")

    # (3) Funcion objetivo: costo de la capacidad faltante en los corredores
    costo_unit = sis.c_costo / sis.c_pmax
    m.setObjective(gp.quicksum(costo_unit[k] * (p_mas[k] + p_menos[k]) for k in range(sis.nc)),
                   GRB.MINIMIZE)
    return m, dict(theta=theta, pf=pf, p_mas=p_mas, p_menos=p_menos, ramas=ramas)
# fin_modelo_lp>>


# <<iteraciones_lp
def lp_iterativo(sis, criterio=None, max_iter=None, env=None, verbose=True, exportar=None):
    """Procedimiento iterativo: resolver LP, agregar una linea, repetir."""
    criterio = (criterio or sis.p("criterio_lp", "flujo")).lower()
    tol = float(sis.p("tolerancia", 1e-6))
    max_iter = max_iter or int(sis.c_nmax.sum()) + 1
    n_adic = np.zeros(sis.nc, dtype=int)
    historia = []
    t0 = time.perf_counter()
    estado_final = "OPTIMO"

    for it in range(1, max_iter + 1):
        m, v = construir_lp(sis, n_adic, env)
        m.Params.Method = 0           # simplex primal (como el Solver de Excel)
        m.optimize()
        if exportar and it == 1:
            exportar_modelo(m, exportar)
        if m.Status != GRB.OPTIMAL:
            estado_final = nombre_estado(m.Status)
            historia.append(dict(iteracion=it, estado=estado_final, n=n_adic.tolist()))
            break
        p_mas = np.array([v["p_mas"][k].X for k in range(sis.nc)])
        p_menos = np.array([v["p_menos"][k].X for k in range(sis.nc)])
        theta = np.array([v["theta"][i].X for i in range(sis.nb)])
        sobrecarga = p_mas + p_menos                     # pu
        lineas_eq = sobrecarga / sis.c_pmax              # lineas equivalentes
        registro = dict(
            iteracion=it, estado="OPTIMO", objetivo=m.ObjVal, n=n_adic.tolist(),
            theta=theta.tolist(), P_mas=p_mas.tolist(), P_menos=p_menos.tolist(),
            sobrecarga_MW=(sobrecarga * sis.sbase).tolist(), lineas_equivalentes=lineas_eq.tolist(),
            flujos_MW={f"{r['etiqueta']}({r['tipo'][0]})": v["pf"][e].X * sis.sbase
                       for e, r in enumerate(v["ramas"])},
            estadisticas=estadisticas(m))
        if lineas_eq.max() <= tol:
            registro["corredor_elegido"] = None
            historia.append(registro)
            break
        if criterio == "costo":
            puntaje = sis.c_costo * lineas_eq
        else:
            puntaje = lineas_eq
        k_sel = int(np.argmax(puntaje))
        registro["corredor_elegido"] = sis.c_id[k_sel]
        historia.append(registro)
        if verbose:
            print(f"  Iter {it:2d}: f.o. = {m.ObjVal:10.4f}   sobrecargas (MW) = "
                  + ", ".join(f"{sis.c_id[k]}:{sobrecarga[k] * sis.sbase:7.2f}" for k in range(sis.nc)
                              if sobrecarga[k] > tol or sis.nc <= 8)
                  + f"   -> +1 linea en {sis.c_id[k_sel]}")
        n_adic[k_sel] += 1
    else:
        estado_final = "LIMITE_DE_ITERACIONES"

    if verbose and historia and historia[-1].get("estado") == "OPTIMO":
        print(f"  Iter {historia[-1]['iteracion']:2d}: f.o. = {historia[-1]['objetivo']:10.4f}"
              "   -> sin sobrecargas: plan factible")
    return dict(n=n_adic, historia=historia, estado=estado_final,
                tiempo_total_s=time.perf_counter() - t0, criterio=criterio)
# fin_iteraciones_lp>>


def resolver(ruta_datos, criterio=None, carpeta_salida=None, verbose=True):
    sis = cargar_sistema(ruta_datos)
    salida = Path(carpeta_salida or CARPETA / "resultados")
    nombre = Path(ruta_datos).stem
    env = entorno_gurobi(salida / "logs" / f"lp_{nombre}.log")
    if verbose:
        print(encabezado("METODO LP ITERATIVO (Villasana-Garver 1985) - Gurobi " +
                         ".".join(map(str, gp.gurobi.version()))))
        print(sis.resumen())
    res = lp_iterativo(sis, criterio, env=env, verbose=verbose,
                       exportar=salida / "modelos" / f"lp_iter1_{nombre}.lp")
    n = res["n"]
    dc = flujo_dc(sis, n)
    res.update(sistema=sis.nombre, archivo=str(ruta_datos), plan=n.tolist(),
               plan_texto=texto_plan(sis, n), costo=costo_plan(sis, n),
               unidad=sis.unidad_costo, corredores=sis.c_id, factible_dc=dc["factible"],
               mensajes_dc=dc["mensajes"], theta_dc=dc["theta"].tolist(),
               flujos_dc=[dict(etiqueta=f["etiqueta"], tipo=f["tipo"], n=f["n"],
                               flujo_MW=f["flujo_MW"], carga=f["carga"]) for f in dc["flujos"]],
               perdidas_MW=perdidas_estimadas(sis, n, dc["theta"]),
               n_lp_resueltos=len(res["historia"]))
    if verbose:
        print(f"\nPlan LP: {res['plan_texto']}")
        print(f"Costo de inversion: {res['costo']:.3f} {sis.unidad_costo}   "
              f"({len(res['historia'])} LP resueltos en {res['tiempo_total_s']:.3f} s)")
        print("Verificacion por flujo DC: " + ("FACTIBLE" if dc["factible"] else
                                                "INFACTIBLE: " + "; ".join(dc["mensajes"])))
        print(tabla_flujos(sis, dc))
    guardar_json(res, salida / f"lp_{nombre}.json")
    env.dispose()
    return res


def main():
    ap = argparse.ArgumentParser(description="TNEP - modelo LP iterativo de Villasana-Garver (Gurobi)")
    ap.add_argument("--datos", default=str(CARPETA / "datos" / "garver6_tnep.xlsx"),
                    help="base de datos Excel del sistema")
    ap.add_argument("--criterio", choices=["flujo", "costo"], default=None,
                    help="regla de seleccion del corredor (por defecto, la de la base de datos)")
    ap.add_argument("--salida", default=None, help="carpeta de resultados")
    args = ap.parse_args()
    resolver(args.datos, args.criterio, args.salida)


if __name__ == "__main__":
    main()
