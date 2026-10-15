# -*- coding: utf-8 -*-
"""
fuerza_bruta.py - Enumeracion exhaustiva de planes de expansion (seccion 4.1
de TNEP.pdf). Sirve como referencia independiente de optimalidad global para
sistemas pequenos: para cada combinacion (n_1, ..., n_nD) se calcula el costo
y se verifica la factibilidad con un flujo DC (sin islas con desbalance y sin
sobrecargas).

En TNEP.pdf las 5x5x4x4 = 400 combinaciones se ordenan como
(n64, n62, n65, n35); el optimo es la combinacion 2401 (fila 226, costo 1000)
y la combinacion 4201 (fila 354, costo 1000) es infactible por sobrecarga en
6-2. Use --orden 6-4,6-2,6-5,3-5 para reproducir esa numeracion.

Uso:
    python fuerza_bruta.py --datos datos/garver6_tnep.xlsx --orden 6-4,6-2,6-5,3-5
"""
from __future__ import annotations

import argparse
import itertools
import time
from pathlib import Path

import numpy as np
import pandas as pd

from tnep_comun import cargar_sistema, encabezado, flujo_dc, guardar_json, texto_plan

CARPETA = Path(__file__).resolve().parent
MAX_COMBINACIONES = 2_000_000


def enumerar(sis, orden=None):
    orden = orden or list(range(sis.nc))
    total = int(np.prod([sis.c_nmax[k] + 1 for k in orden], dtype=float))
    if total > MAX_COMBINACIONES:
        raise ValueError(f"{total:.3e} combinaciones: la enumeracion exhaustiva no es viable "
                         "(explosion combinatoria); use los modelos MILP/MINLP")
    filas = []
    for fila, combo in enumerate(itertools.product(*[range(sis.c_nmax[k] + 1) for k in orden]), start=1):
        n = np.zeros(sis.nc, dtype=int)
        n[orden] = combo
        dc = flujo_dc(sis, n)
        filas.append(dict(fila=fila, codigo="".join(map(str, combo)),
                          **{f"n_{sis.c_id[k]}": int(n[k]) for k in range(sis.nc)},
                          costo=float(np.dot(sis.c_costo, n)), lineas=int(n.sum()),
                          factible=dc["factible"], carga_max=dc["carga_max"],
                          causa="" if dc["factible"] else dc["mensajes"][0]))
    return pd.DataFrame(filas), total


def resolver(ruta_datos, orden_txt=None, carpeta_salida=None, verbose=True):
    sis = cargar_sistema(ruta_datos)
    orden = [sis.c_id.index(c.strip()) for c in orden_txt.split(",")] if orden_txt else None
    t0 = time.perf_counter()
    df, total = enumerar(sis, orden)
    tiempo = time.perf_counter() - t0
    factibles = df[df.factible].sort_values(["costo", "fila"])
    optimo = factibles.iloc[0]
    empatados = df[np.isclose(df.costo, optimo.costo)]
    mas_baratos_infactibles = df[(~df.factible) & (df.costo <= optimo.costo)].sort_values("costo",
                                                                                           ascending=False)
    salida = Path(carpeta_salida or CARPETA / "resultados")
    salida.mkdir(parents=True, exist_ok=True)
    nombre = Path(ruta_datos).stem
    df.to_csv(salida / f"fuerza_bruta_{nombre}.csv", index=False, encoding="utf-8")
    n_opt = [int(optimo[f"n_{c}"]) for c in sis.c_id]
    res = dict(sistema=sis.nombre, combinaciones=total, factibles=int(df.factible.sum()),
               tiempo_s=tiempo, orden=[sis.c_id[k] for k in (orden or range(sis.nc))],
               optimo=dict(fila=int(optimo.fila), codigo=optimo.codigo, costo=float(optimo.costo),
                           plan=n_opt, plan_texto=texto_plan(sis, n_opt), carga_max=float(optimo.carga_max)),
               empatados_en_costo=empatados[["fila", "codigo", "costo", "factible", "carga_max", "causa"]]
               .to_dict("records"),
               top10_factibles=factibles.head(10)[["fila", "codigo", "costo", "carga_max"]].to_dict("records"),
               infactibles_mas_baratos=mas_baratos_infactibles.head(10)[
                   ["fila", "codigo", "costo", "carga_max", "causa"]].to_dict("records"))
    guardar_json(res, salida / f"fuerza_bruta_{nombre}.json")
    if verbose:
        print(encabezado("ENUMERACION EXHAUSTIVA (fuerza bruta) + flujo DC"))
        print(sis.resumen())
        print(f"Orden de enumeracion: {res['orden']}")
        print(f"{total} combinaciones evaluadas en {tiempo:.2f} s; factibles: {res['factibles']}")
        print(f"Optimo: combinacion {optimo.codigo} (fila {optimo.fila}), costo {optimo.costo:.1f} "
              f"{sis.unidad_costo} -> {res['optimo']['plan_texto']}, cargabilidad maxima "
              f"{100 * optimo.carga_max:.1f} %")
        print("Combinaciones con el mismo costo:")
        for r in res["empatados_en_costo"]:
            estado = "FACTIBLE" if r["factible"] else f"INFACTIBLE ({r['causa']})"
            print(f"   fila {r['fila']:4d}  codigo {r['codigo']}  costo {r['costo']:.1f}  {estado}")
        print("10 planes factibles mas baratos:")
        for r in res["top10_factibles"]:
            print(f"   fila {r['fila']:4d}  codigo {r['codigo']}  costo {r['costo']:7.1f}  "
                  f"carga max {100 * r['carga_max']:6.1f} %")
    return res


def main():
    ap = argparse.ArgumentParser(description="TNEP - enumeracion exhaustiva con flujo DC")
    ap.add_argument("--datos", default=str(CARPETA / "datos" / "garver6_tnep.xlsx"))
    ap.add_argument("--orden", default=None, help="orden de los corredores, p.ej. 6-4,6-2,6-5,3-5")
    ap.add_argument("--salida", default=None)
    args = ap.parse_args()
    resolver(args.datos, args.orden, args.salida)


if __name__ == "__main__":
    main()
