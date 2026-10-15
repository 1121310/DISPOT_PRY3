# -*- coding: utf-8 -*-
"""
ejecutar_todo.py - Reproduce TODOS los resultados del informe:

  1. Construye las bases de datos (datos/*.xlsx).
  2. Resuelve los tres metodos (LP, MINLP, MILP big-M) en los tres sistemas:
     Garver 4 corredores (TNEP.pdf), Garver 15 corredores y Sur de Brasil 46.
  3. Validaciones: fuerza bruta (Garver), flujo AC (Garver 1970), cotas
     inferiores / relajaciones, sensibilidad a big-M, a n_max y al criterio
     de seleccion del LP, y validacion cruzada con HiGHS (si esta instalado).
  4. Guarda resultados/resumen.json; luego graficas.py y tablas_latex.py
     generan las figuras y tablas del informe.

Uso:  python ejecutar_todo.py            (unos pocos minutos)
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import time
from pathlib import Path

import numpy as np

import fuerza_bruta
import tnep_lp
import tnep_milp_bigm
import tnep_minlp
import validacion_ac
from tnep_comun import (big_m_corredores, cargar_sistema, entorno_gurobi, guardar_json)

CARPETA = Path(__file__).resolve().parent
DATOS = CARPETA / "datos"
SALIDA = CARPETA / "resultados"
CASOS = {
    "garver6_tnep": "Garver 6 barras, 4 corredores",
    "garver6_15corredores": "Garver 6 barras, 15 corredores",
    "sur46_sin_redespacho": "Sur de Brasil 46 barras",
}
# Valores publicados en TNEP.pdf (LP: sec. 5.2) para la comparacion
TNEP_PDF_LP = dict(objetivo=[878.75, 728.75, 578.75, 456.625, 306.625, 156.625, 74.2, 0.0],
                   elegido=["6-4", "6-4", "6-2", "6-2", "6-2", "3-5", "6-2", None],
                   # angulos (rad, ref. barra 5) publicados en cada iteracion; None = no publicado
                   theta=[[0.16, 0.27, 0.20, 0.64, 0.00, None], [0.16, 0.27, 0.20, 0.64, 0.00, 0.94],
                          [0.16, 0.27, 0.20, 0.64, 0.00, 0.94], [0.11, 0.32, 0.20, 0.32, 0.00, 0.62],
                          [0.11, 0.32, 0.20, 0.32, 0.00, 0.62], [0.11, 0.32, 0.20, 0.32, 0.00, 0.62],
                          [0.11, 0.31, 0.19, 0.31, 0.00, 0.61], [0.11, 0.31, 0.19, 0.30, 0.00, 0.58]])
# Optimo DC sin redespacho: Romero y Monticelli (1994); optimalidad probada por Binato et al. (2001)
LITERATURA_46 = 154.420


def silencioso(funcion, *args, archivo=None, **kwargs):
    """Ejecuta `funcion` capturando su salida de consola en `archivo`."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        resultado = funcion(*args, **kwargs)
    if archivo:
        Path(archivo).parent.mkdir(parents=True, exist_ok=True)
        Path(archivo).write_text(buffer.getvalue(), encoding="utf-8")
    return resultado


def construir_bases():
    ruta = DATOS / "construir_bases_de_datos.py"
    spec = importlib.util.spec_from_file_location("construir_bases_de_datos", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    modulo.main()


def resolver_metodos(caso):
    ruta = DATOS / f"{caso}.xlsx"
    consola = SALIDA / "consola"
    lp = silencioso(tnep_lp.resolver, ruta, None, SALIDA, archivo=consola / f"lp_{caso}.txt")
    minlp = silencioso(tnep_minlp.resolver, ruta, SALIDA, archivo=consola / f"minlp_{caso}.txt")
    milp = silencioso(tnep_milp_bigm.resolver, ruta, SALIDA, archivo=consola / f"milp_{caso}.txt")
    return dict(lp=lp, minlp=minlp, milp=milp)


def relajaciones(caso, res):
    """Cotas inferiores: LP de Villasana (iteracion 1), relajacion lineal del
    MILP big-M y relajacion continua del MINLP (n continuo, QCP global)."""
    sis = cargar_sistema(DATOS / f"{caso}.xlsx")
    env = entorno_gurobi(SALIDA / "logs" / f"relajaciones_{caso}.log")
    M, _ = big_m_corredores(sis)
    m, _ = tnep_milp_bigm.construir_milp(sis, env, M)
    m.update()                      # relax() necesita el modelo actualizado
    r = m.relax()
    r.optimize()
    cota_milp = r.ObjVal
    # Relajacion continua del MINLP: QCP NO convexo (se resuelve a optimalidad
    # global por B&B espacial); se limita el tiempo y se reporta la cota valida.
    m2, _ = tnep_minlp.construir_minlp(sis, env, entero=False)
    m2.Params.TimeLimit = 120
    m2.Params.MIPGap = 1e-4
    m2.optimize()
    cota_minlp = m2.ObjBound
    info_minlp = dict(incumbente=m2.ObjVal if m2.SolCount else None, tiempo_s=m2.Runtime,
                      nodos=m2.NodeCount, estado=int(m2.Status))
    env.dispose()
    optimo = res["milp"]["costo"]
    lp1 = res["lp"]["historia"][0]["objetivo"]
    filas = dict(lp_iter1=lp1, relajacion_milp=cota_milp, relajacion_minlp=cota_minlp, optimo=optimo)
    salida = {k: dict(valor=v, brecha_pct=100 * (optimo - v) / optimo) for k, v in filas.items()}
    salida["relajacion_minlp"].update(info_minlp)
    return salida


def sensibilidad_bigM(caso, valores, incluir_auto=False, limite_tiempo=120):
    ruta = DATOS / f"{caso}.xlsx"
    sis = cargar_sistema(ruta)
    env = entorno_gurobi(SALIDA / "logs" / f"bigM_relax_{caso}.log")
    filas = []
    configuraciones = [("fijo", float(v)) for v in valores] + ([("auto", None)] if incluir_auto else [])
    for modo, valor in configuraciones:
        etiqueta = f"_M_{modo}_{valor}" if valor is not None else "_M_auto"
        r = tnep_milp_bigm.resolver(ruta, SALIDA / "sensibilidad", verbose=False, M_fijo=valor,
                                    modo=modo, etiqueta=etiqueta, exportar=False,
                                    limite_tiempo=limite_tiempo)
        print(f"   {caso} M={valor if valor is not None else 'auto'}: {r['estado']} costo={r.get('costo')} "
              f"t={r['estadisticas']['tiempo_s']:.2f} s")
        if valor is not None:
            sis.param["bigM_rad"] = valor
        sis.param["bigM_modo"] = modo
        M, _ = big_m_corredores(sis)
        m, _ = tnep_milp_bigm.construir_milp(sis, env, M)
        m.update()
        rel = m.relax()
        rel.optimize()
        e = r["estadisticas"]
        filas.append(dict(modo=modo, M=valor, costo=r.get("costo"), plan=r.get("plan_texto"),
                          relajacion=rel.ObjVal, tiempo_s=e["tiempo_s"], nodos=e.get("nodos"),
                          estado=r["estado"], brecha=r.get("brecha"), cota=r.get("cota"),
                          factible_dc=r.get("factible_dc")))
    env.dispose()
    return filas


def m_critico_garver(tol=1e-4):
    """Menor M (biseccion) con el que el MILP recupera el optimo de 1000."""
    ruta = DATOS / "garver6_tnep.xlsx"
    bajo, alto = 0.1, 1.0
    while alto - bajo > tol:
        medio = 0.5 * (bajo + alto)
        r = tnep_milp_bigm.resolver(ruta, SALIDA / "sensibilidad", verbose=False, M_fijo=medio,
                                    modo="fijo", etiqueta="_biseccion", exportar=False)
        if abs(r["costo"] - 1000) < 1e-6:
            alto = medio
        else:
            bajo = medio
    return alto


def sensibilidad_nmax():
    filas = []
    ruta = DATOS / "garver6_tnep.xlsx"
    # Variante del libro Excel MILP del curso: hasta 5 lineas en 6-2 y 6-4
    variante = {"6-2": 5, "6-4": 5}
    for nombre, mod in [("milp", tnep_milp_bigm), ("minlp", tnep_minlp)]:
        r = mod.resolver(ruta, SALIDA / "sensibilidad", verbose=False, nmax=variante, etiqueta="_nmax_excel",
                         **({"exportar": False} if nombre == "milp" else {}))
        filas.append(dict(sistema="garver6_tnep", nmax="6-2:5, 6-4:5 (Excel)", metodo=nombre,
                          costo=r["costo"], plan=r["plan_texto"], tiempo_s=r["estadisticas"]["tiempo_s"],
                          binarias=r["estadisticas"]["binarias"], enteras=r["estadisticas"]["enteras"],
                          nodos=r["estadisticas"].get("nodos")))
    ruta = DATOS / "sur46_sin_redespacho.xlsx"
    sis = cargar_sistema(ruta)
    for valor in (3, 5, 10):
        todos = {c: valor for c in sis.c_id}
        for nombre, mod in [("milp", tnep_milp_bigm), ("minlp", tnep_minlp)]:
            r = mod.resolver(ruta, SALIDA / "sensibilidad", verbose=False, nmax=todos, etiqueta=f"_nmax{valor}",
                             **({"exportar": False} if nombre == "milp" else {}))
            e = r["estadisticas"]
            filas.append(dict(sistema="sur46_sin_redespacho", nmax=valor, metodo=nombre, costo=r["costo"],
                              plan=r["plan_texto"], tiempo_s=e["tiempo_s"], binarias=e["binarias"],
                              enteras=e["enteras"], variables=e["variables"], restricciones=e["restricciones"],
                              restr_cuadraticas=e["restr_cuadraticas"], nodos=e.get("nodos")))
    return filas


def criterio_lp():
    filas = []
    for caso in CASOS:
        for criterio in ("flujo", "costo"):
            r = tnep_lp.resolver(DATOS / f"{caso}.xlsx", criterio, SALIDA / "sensibilidad", verbose=False)
            filas.append(dict(caso=caso, criterio=criterio, costo=r["costo"], plan=r["plan_texto"],
                              lp_resueltos=r["n_lp_resueltos"], factible=r["factible_dc"],
                              tiempo_s=r["tiempo_total_s"]))
    return filas


def main():
    t0 = time.perf_counter()
    print("1) Bases de datos")
    construir_bases()
    resumen = dict(casos={}, tnep_pdf_lp=TNEP_PDF_LP, literatura_46=LITERATURA_46)

    print("2) Tres metodos en los tres sistemas")
    for caso, titulo in CASOS.items():
        res = resolver_metodos(caso)
        resumen["casos"][caso] = dict(titulo=titulo, **{k: v for k, v in res.items()})
        for metodo in ("lp", "minlp", "milp"):
            r = res[metodo]
            t = r.get("tiempo_total_s", r.get("estadisticas", {}).get("tiempo_s"))
            print(f"   {titulo:32s} {metodo.upper():6s} costo = {r['costo']:10.3f} {r['unidad']:5s} "
                  f"t = {t:8.3f} s  -> {r['plan_texto']}")
        resumen["casos"][caso]["relajaciones"] = relajaciones(caso, res)

    print("3) Fuerza bruta y flujo AC (Garver)")
    resumen["fuerza_bruta"] = silencioso(fuerza_bruta.resolver, DATOS / "garver6_tnep.xlsx", "6-4,6-2,6-5,3-5",
                                         SALIDA, archivo=SALIDA / "consola" / "fuerza_bruta.txt")
    plan = resumen["casos"]["garver6_tnep"]["milp"]
    plan_txt = ",".join(f"{c}={n}" for c, n in zip(plan["corredores"], plan["plan"]) if n > 0)
    resumen["validacion_ac"] = silencioso(validacion_ac.resolver, DATOS / "garver6_tnep.xlsx", plan_txt, SALIDA,
                                          archivo=SALIDA / "consola" / "validacion_ac.txt")
    print(f"   optimo enumerado: {resumen['fuerza_bruta']['optimo']['codigo']} "
          f"(fila {resumen['fuerza_bruta']['optimo']['fila']}), perdidas AC "
          f"{resumen['validacion_ac']['perdidas_MW']:.2f} MW")

    print("4) Sensibilidad a big-M")
    resumen["bigM_garver"] = sensibilidad_bigM(
        "garver6_tnep", [0.1, 0.2, 0.3, 0.4, 0.5, 0.55, 0.57, 0.58, 0.6, 0.8, 1, 2, 5, 10, 100, 1000])
    resumen["bigM_critico_garver"] = m_critico_garver()
    resumen["bigM_46"] = sensibilidad_bigM("sur46_sin_redespacho",
                                           [0.25, 0.5, 0.75, 1, 2, 5, 10, 50, 100, 1000], incluir_auto=True)
    print(f"   M critico (Garver) = {resumen['bigM_critico_garver']:.4f} rad")

    print("5) Sensibilidad a n_max y al criterio del LP")
    resumen["nmax"] = sensibilidad_nmax()
    resumen["criterio_lp"] = criterio_lp()

    resumen["tiempo_total_s"] = time.perf_counter() - t0
    guardar_json(resumen, SALIDA / "resumen.json")

    print("6) Validacion cruzada con HiGHS (opcional)")
    try:
        import validacion_highs
        silencioso(validacion_highs.main, archivo=SALIDA / "consola" / "validacion_highs.txt")
        print("   ver resultados/validacion_highs.json")
    except ImportError:
        print("   highspy no esta instalado: se omite (pip install highspy)")
    print(f"Listo en {resumen['tiempo_total_s']:.1f} s -> {SALIDA / 'resumen.json'}")


if __name__ == "__main__":
    main()
