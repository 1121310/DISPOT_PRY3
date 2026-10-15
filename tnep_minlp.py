# -*- coding: utf-8 -*-
"""
tnep_minlp.py - METODO 2: modelo MINLP bilineal (seccion 7 de TNEP.pdf),
resuelto a optimalidad GLOBAL con Gurobi (branch-and-bound espacial para
restricciones cuadraticas no convexas, NonConvex = 2).

    min   sum_{ij in Omega} c_ij n_ij                                   (24)
    s.a.  sum_m B^a_jm(n) theta_m = PG_j - PL_j          para toda j      (25)
          P_ij = n_ij B_ij (theta_i - theta_j)       ij en Omega          (26),(28)
          -Pmax_jm <= P^a_jm <= Pmax_jm               red existente       (27),(29)
          -n_ij Pmax_ij <= P_ij <= n_ij Pmax_ij       ij en Omega          (30)
          0 <= n_ij <= n_ij^max,  n_ij entero,  theta_ref = 0             (31)

donde B^a(n) es la matriz de susceptancias aumentada que depende de n
(ec. 23). Expandir B^a(n) theta en (25) equivale a escribir el balance con los
flujos de la red existente mas los flujos P_ij de los corredores, que es la
forma (dispersa y escalable) que se implementa aqui. La no linealidad es el
producto bilineal entero x continua  n_ij * (theta_i - theta_j).

Para que el branch-and-bound espacial disponga de envolventes de McCormick
finitas, los angulos se acotan con |theta| <= theta_max (parametro de la base
de datos; se verifica a posteriori que la cota no quede activa).

Uso:
    python tnep_minlp.py --datos datos/garver6_tnep.xlsx
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from tnep_comun import (GRB, RegistroConvergencia, cargar_sistema, costo_plan, encabezado,
                        entorno_gurobi, estadisticas, exportar_modelo, flujo_dc, gp, guardar_json,
                        nombre_estado, perdidas_estimadas, tabla_flujos, texto_plan)

CARPETA = Path(__file__).resolve().parent


# <<modelo_minlp
def construir_minlp(sis, env, theta_max=None, entero=True):
    """Modelo MINLP con el producto bilineal n_ij * B_ij * (theta_i - theta_j)."""
    theta_max = float(theta_max or sis.p("theta_max_rad", np.pi))
    m = gp.Model("TNEP_MINLP_bilineal", env=env)

    theta = m.addVars(sis.nb, lb=-theta_max, ub=theta_max, name="theta")
    theta[sis.ref].lb = theta[sis.ref].ub = 0.0
    tipo_n = GRB.INTEGER if entero else GRB.CONTINUOUS
    n = m.addVars(sis.nc, lb=0, ub=sis.c_nmax.astype(float).tolist(), vtype=tipo_n, name="n")
    # apertura angular de cada corredor y flujo total del corredor
    dth = m.addVars(sis.nc, lb=-2 * theta_max, ub=2 * theta_max, name="dtheta")
    p_c = m.addVars(sis.nc, lb=(-sis.c_nmax * sis.c_pmax).tolist(),
                    ub=(sis.c_nmax * sis.c_pmax).tolist(), name="Pij")
    # flujos de la red existente (27) con su limite (29) como cota de la variable
    p_e = m.addVars(sis.nl, lb=(-sis.l_n0 * sis.l_pmax).tolist(),
                    ub=(sis.l_n0 * sis.l_pmax).tolist(), name="Pa")

    for l in range(sis.nl):                                              # (27)
        m.addConstr(p_e[l] == sis.l_n0[l] / sis.l_x[l] * (theta[sis.l_de[l]] - theta[sis.l_a[l]]),
                    name=f"flujo_existente_{sis.etiqueta_linea(l)}_{l}")
    for k in range(sis.nc):
        cid = sis.c_id[k]
        m.addConstr(dth[k] == theta[sis.c_de[k]] - theta[sis.c_a[k]], name=f"apertura_{cid}")
        m.addConstr(p_c[k] == (1.0 / sis.c_x[k]) * n[k] * dth[k], name=f"bilineal_{cid}")  # (28)
        m.addConstr(p_c[k] <= sis.c_pmax[k] * n[k], name=f"cap_sup_{cid}")                 # (30)
        m.addConstr(p_c[k] >= -sis.c_pmax[k] * n[k], name=f"cap_inf_{cid}")

    # (25) balance nodal  B^a(n) theta = PG - PL  escrito con flujos
    salida = [gp.LinExpr() for _ in range(sis.nb)]
    for l in range(sis.nl):
        salida[sis.l_de[l]] += p_e[l]
        salida[sis.l_a[l]] -= p_e[l]
    for k in range(sis.nc):
        salida[sis.c_de[k]] += p_c[k]
        salida[sis.c_a[k]] -= p_c[k]
    for i in range(sis.nb):
        m.addConstr(salida[i] == sis.pg[i] - sis.pl[i], name=f"balance_{sis.barras[i]}")

    m.setObjective(gp.quicksum(sis.c_costo[k] * n[k] for k in range(sis.nc)), GRB.MINIMIZE)  # (24)
    m.Params.NonConvex = 2              # B&B espacial global para la restriccion bilineal
    return m, dict(theta=theta, n=n, dth=dth, p_c=p_c, p_e=p_e, theta_max=theta_max)
# fin_modelo_minlp>>


def resolver(ruta_datos, carpeta_salida=None, verbose=True, limite_tiempo=None, theta_max=None,
             nmax=None, etiqueta=""):
    sis = cargar_sistema(ruta_datos)
    if nmax:                                     # sensibilidad: n_max modificado
        for cid, valor in nmax.items():
            sis.c_nmax[sis.c_id.index(cid)] = valor
    salida = Path(carpeta_salida or CARPETA / "resultados")
    nombre = Path(ruta_datos).stem + etiqueta
    env = entorno_gurobi(salida / "logs" / f"minlp_{nombre}.log")
    if verbose:
        print(encabezado("METODO MINLP BILINEAL (TNEP.pdf, sec. 7) - Gurobi " +
                         ".".join(map(str, gp.gurobi.version()))))
        print(sis.resumen())

    m, v = construir_minlp(sis, env, theta_max)
    m.Params.MIPGap = float(sis.p("mip_gap", 0.0))
    m.Params.TimeLimit = float(limite_tiempo or sis.p("limite_tiempo_s", 3600))
    exportar_modelo(m, salida / "modelos" / f"minlp_{nombre}.lp")
    registro = RegistroConvergencia()
    m.optimize(registro)

    res = dict(metodo="MINLP", sistema=sis.nombre, archivo=str(ruta_datos), estado=nombre_estado(m.Status),
               estadisticas=estadisticas(m), convergencia=registro.puntos, corredores=sis.c_id,
               unidad=sis.unidad_costo, theta_max=v["theta_max"], nmax=sis.c_nmax.tolist())
    if m.SolCount == 0:
        if verbose:
            print("Gurobi no encontro solucion factible:", res["estado"])
        guardar_json(res, salida / f"minlp_{nombre}.json")
        env.dispose()
        return res

    n = np.array([round(v["n"][k].X) for k in range(sis.nc)], dtype=int)
    theta = np.array([v["theta"][i].X for i in range(sis.nb)])
    dc = flujo_dc(sis, n)
    # La cota |theta| <= theta_max solo importa en barras conectadas electricamente
    # a la referencia; en barras aisladas sin inyeccion el angulo es arbitrario.
    isla_ref = dc["islas"][sis.ref]
    cota_activa = [sis.barras[i] for i in range(sis.nb)
                   if abs(abs(theta[i]) - v["theta_max"]) < 1e-6 and i != sis.ref
                   and dc["islas"][i] == isla_ref]
    res.update(plan=n.tolist(), plan_texto=texto_plan(sis, n), costo=costo_plan(sis, n),
               objetivo=m.ObjVal, cota=m.ObjBound, brecha=m.MIPGap, theta=theta.tolist(),
               flujo_corredor_MW=[v["p_c"][k].X * sis.sbase for k in range(sis.nc)],
               factible_dc=dc["factible"], mensajes_dc=dc["mensajes"], theta_dc=dc["theta"].tolist(),
               flujos_dc=[dict(etiqueta=f["etiqueta"], tipo=f["tipo"], n=f["n"],
                               flujo_MW=f["flujo_MW"], carga=f["carga"]) for f in dc["flujos"]],
               perdidas_MW=perdidas_estimadas(sis, n, dc["theta"]),
               barras_con_cota_theta_activa=cota_activa)
    if verbose:
        e = res["estadisticas"]
        print(f"Estado Gurobi: {res['estado']}   tiempo {e['tiempo_s']:.3f} s   nodos {e.get('nodos', 0):.0f}"
              f"   brecha {100 * res['brecha']:.4f} %")
        print(f"Variables: {e['variables']} ({e['enteras']} enteras)   restricciones lineales: "
              f"{e['restricciones']}   bilineales: {e['restr_cuadraticas']}")
        print(f"\nPlan MINLP: {res['plan_texto']}")
        print(f"Costo de inversion: {res['costo']:.3f} {sis.unidad_costo}   (cota inferior {m.ObjBound:.3f})")
        ang = ", ".join(f"{a:.3f}" for a in theta - theta[sis.ref])
        print(f"Angulos (rad, ref. barra {sis.barras[sis.ref]}): [{ang}]")
        if cota_activa:
            print(f"ADVERTENCIA: cota |theta| <= {v['theta_max']} activa en barras {cota_activa}")
        print("Verificacion por flujo DC: " + ("FACTIBLE" if dc["factible"] else
                                                "INFACTIBLE: " + "; ".join(dc["mensajes"])))
        print(tabla_flujos(sis, dc))
    guardar_json(res, salida / f"minlp_{nombre}.json")
    env.dispose()
    return res


def main():
    ap = argparse.ArgumentParser(description="TNEP - modelo MINLP bilineal (Gurobi, optimo global)")
    ap.add_argument("--datos", default=str(CARPETA / "datos" / "garver6_tnep.xlsx"))
    ap.add_argument("--salida", default=None, help="carpeta de resultados")
    ap.add_argument("--tiempo", type=float, default=None, help="limite de tiempo (s)")
    ap.add_argument("--theta-max", type=float, default=None, help="cota de los angulos (rad)")
    args = ap.parse_args()
    resolver(args.datos, args.salida, limite_tiempo=args.tiempo, theta_max=args.theta_max)


if __name__ == "__main__":
    main()
