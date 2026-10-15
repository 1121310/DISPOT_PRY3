# -*- coding: utf-8 -*-
"""
tnep_milp_bigm.py - METODO 3: modelo M(0-1)LP de Villasana (1984) con
linealizacion big-M (seccion 6 de TNEP.pdf), resuelto con Gurobi
(branch-and-cut).

Variables: w_ijk binaria (= 1 si se instalan exactamente k lineas en el
corredor i-j), dtheta_ijk continua, theta_j continua.

    min   sum_{ij in Omega} sum_{k=1}^{n_ij} k c_ij w_ijk                     (13)
    s.a.  sum_m B^a_jm theta_m = PG_j - PL_j + sum_{Omega} sum_k P_ijk        (14)
          -Pmax_jm <= P^a_jm <= Pmax_jm                 red existente        (15)
          -k Pmax_ij w_ijk <= P_ijk <= k Pmax_ij w_ijk                        (16)
          P^a_jm = B^a_jm (theta_j - theta_m)                                 (17)
          P_ijk  = k B_ij dtheta_ijk                                          (18)
          M (sum_k w_ijk - 1) <= theta_i - theta_j - sum_k dtheta_ijk
                              <= M (1 - sum_k w_ijk)                          (19)
          sum_k w_ijk <= 1                                                    (20)

La restriccion (19) es la linealizacion big-M del producto binaria x
continua: si el corredor se construye (sum_k w = 1) la banda colapsa y
sum_k dtheta_ijk = theta_i - theta_j (segunda ley de Kirchhoff); si no se
construye, la banda se abre a [-M, M] y (16) anula el flujo. Villasana usa
M = 1 rad. Como mejora opcional (bigM_modo = 'auto'), M_ij se calcula como
el camino minimo angular en la red existente (cota valida y mas ajustada).

Uso:
    python tnep_milp_bigm.py --datos datos/garver6_tnep.xlsx
    python tnep_milp_bigm.py --datos datos/garver6_tnep.xlsx --bigM 0.5
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from tnep_comun import (GRB, RegistroConvergencia, big_m_corredores, cargar_sistema, costo_plan,
                        encabezado, entorno_gurobi, estadisticas, exportar_modelo, flujo_dc, gp,
                        guardar_json, nombre_estado, perdidas_estimadas, tabla_flujos, texto_plan)

CARPETA = Path(__file__).resolve().parent


# <<modelo_milp
def construir_milp(sis, env, M):
    """Modelo M(0-1)LP disyuntivo de Villasana (1984) con constantes big-M `M[k]`."""
    m = gp.Model("TNEP_MILP_bigM_Villasana", env=env)
    theta = m.addVars(sis.nb, lb=-GRB.INFINITY, ub=GRB.INFINITY, name="theta")
    theta[sis.ref].lb = theta[sis.ref].ub = 0.0
    idx = [(k, j) for k in range(sis.nc) for j in range(1, int(sis.c_nmax[k]) + 1)]
    w = m.addVars(idx, vtype=GRB.BINARY, name="w")
    dth = m.addVars(idx, lb=-GRB.INFINITY, ub=GRB.INFINITY, name="dtheta")
    # (15),(17) red existente: flujo con su limite como cota de la variable
    p_e = m.addVars(sis.nl, lb=(-sis.l_n0 * sis.l_pmax).tolist(),
                    ub=(sis.l_n0 * sis.l_pmax).tolist(), name="Pa")
    for l in range(sis.nl):
        m.addConstr(p_e[l] == sis.l_n0[l] / sis.l_x[l] * (theta[sis.l_de[l]] - theta[sis.l_a[l]]),
                    name=f"flujo_existente_{sis.etiqueta_linea(l)}_{l}")

    salida = [gp.LinExpr() for _ in range(sis.nb)]
    for l in range(sis.nl):
        salida[sis.l_de[l]] += p_e[l]
        salida[sis.l_a[l]] -= p_e[l]

    for c in range(sis.nc):
        cid, b = sis.c_id[c], 1.0 / sis.c_x[c]
        ks = range(1, int(sis.c_nmax[c]) + 1)
        if not ks:
            continue
        for k in ks:
            flujo = k * b * dth[c, k]                                         # (18)
            m.addConstr(flujo <= k * sis.c_pmax[c] * w[c, k], name=f"cap_sup_{cid}_{k}")   # (16)
            m.addConstr(flujo >= -k * sis.c_pmax[c] * w[c, k], name=f"cap_inf_{cid}_{k}")
            salida[sis.c_de[c]] += flujo
            salida[sis.c_a[c]] -= flujo
        suma_w = gp.quicksum(w[c, k] for k in ks)
        holgura = theta[sis.c_de[c]] - theta[sis.c_a[c]] - gp.quicksum(dth[c, k] for k in ks)
        m.addConstr(holgura <= M[c] * (1 - suma_w), name=f"bigM_sup_{cid}")         # (19)
        m.addConstr(holgura >= M[c] * (suma_w - 1), name=f"bigM_inf_{cid}")
        m.addConstr(suma_w <= 1, name=f"unicidad_{cid}")                           # (20)

    for i in range(sis.nb):                                                         # (14)
        m.addConstr(salida[i] == sis.pg[i] - sis.pl[i], name=f"balance_{sis.barras[i]}")

    m.setObjective(gp.quicksum(k * sis.c_costo[c] * w[c, k] for c, k in idx), GRB.MINIMIZE)  # (13)
    return m, dict(theta=theta, w=w, dth=dth, p_e=p_e, idx=idx)
# fin_modelo_milp>>


def resolver(ruta_datos, carpeta_salida=None, verbose=True, M_fijo=None, modo=None,
             limite_tiempo=None, nmax=None, etiqueta="", exportar=True):
    sis = cargar_sistema(ruta_datos)
    if M_fijo is not None:
        sis.param["bigM_rad"] = float(M_fijo)
    if modo is not None:
        sis.param["bigM_modo"] = modo
    if nmax:                                     # sensibilidad: n_max modificado
        for cid, valor in nmax.items():
            sis.c_nmax[sis.c_id.index(cid)] = valor
    M, origen_M = big_m_corredores(sis)
    salida = Path(carpeta_salida or CARPETA / "resultados")
    nombre = Path(ruta_datos).stem + etiqueta
    env = entorno_gurobi(salida / "logs" / f"milp_{nombre}.log")
    if verbose:
        print(encabezado("METODO MILP BIG-M M(0-1)LP (Villasana 1984) - Gurobi " +
                         ".".join(map(str, gp.gurobi.version()))))
        print(sis.resumen())
        print(f"Big-M: modo '{sis.p('bigM_modo', 'fijo')}', M en [{M.min():.4f}, {M.max():.4f}] rad")

    m, v = construir_milp(sis, env, M)
    m.Params.MIPGap = float(sis.p("mip_gap", 0.0))
    m.Params.TimeLimit = float(limite_tiempo or sis.p("limite_tiempo_s", 3600))
    if exportar:
        exportar_modelo(m, salida / "modelos" / f"milp_{nombre}.lp")
    registro = RegistroConvergencia()
    m.optimize(registro)

    res = dict(metodo="MILP_bigM", sistema=sis.nombre, archivo=str(ruta_datos),
               estado=nombre_estado(m.Status), estadisticas=estadisticas(m),
               convergencia=registro.puntos, corredores=sis.c_id, unidad=sis.unidad_costo,
               bigM=M.tolist(), bigM_origen=origen_M, bigM_modo=sis.p("bigM_modo", "fijo"),
               nmax=sis.c_nmax.tolist())
    if m.SolCount == 0:
        if verbose:
            print("Gurobi no encontro solucion factible:", res["estado"])
        guardar_json(res, salida / f"milp_{nombre}.json")
        env.dispose()
        return res

    n = np.zeros(sis.nc, dtype=int)
    w_activas = []
    for (c, k) in v["idx"]:
        if v["w"][c, k].X > 0.5:
            n[c] = k
            w_activas.append(f"w{sis.c_id[c].replace('-', '')}{k}")
    theta = np.array([v["theta"][i].X for i in range(sis.nb)])
    dtheta = {f"{sis.c_id[c]}_{k}": v["dth"][c, k].X for (c, k) in v["idx"]}
    dc = flujo_dc(sis, n)
    # Diagnostico de validez de M: apertura angular en corredores NO construidos
    # cuyos extremos quedan en la misma isla (si estan en islas distintas el
    # angulo relativo es arbitrario y la banda big-M no restringe nada).
    apertura = []
    for c in range(sis.nc):
        if n[c] == 0 and dc["islas"][sis.c_de[c]] == dc["islas"][sis.c_a[c]]:
            d = abs(theta[sis.c_de[c]] - theta[sis.c_a[c]])
            apertura.append(dict(corredor=sis.c_id[c], apertura=d, M=M[c], activa=d >= M[c] - 1e-6))
    res.update(plan=n.tolist(), plan_texto=texto_plan(sis, n), w_activas=w_activas,
               costo=costo_plan(sis, n), objetivo=m.ObjVal, cota=m.ObjBound, brecha=m.MIPGap,
               theta=theta.tolist(), dtheta=dtheta, apertura_no_construidos=apertura,
               M_activa=[a["corredor"] for a in apertura if a["activa"]],
               factible_dc=dc["factible"], mensajes_dc=dc["mensajes"], theta_dc=dc["theta"].tolist(),
               flujos_dc=[dict(etiqueta=f["etiqueta"], tipo=f["tipo"], n=f["n"],
                               flujo_MW=f["flujo_MW"], carga=f["carga"]) for f in dc["flujos"]],
               perdidas_MW=perdidas_estimadas(sis, n, dc["theta"]))
    if verbose:
        e = res["estadisticas"]
        print(f"Estado Gurobi: {res['estado']}   tiempo {e['tiempo_s']:.3f} s   nodos {e.get('nodos', 0):.0f}"
              f"   brecha {100 * res['brecha']:.4f} %")
        print(f"Variables: {e['variables']} ({e['binarias']} binarias)   restricciones: {e['restricciones']}")
        print(f"\nBinarias activas: {', '.join(w_activas)}")
        print(f"Plan MILP: {res['plan_texto']}")
        print(f"Costo de inversion: {res['costo']:.3f} {sis.unidad_costo}   (cota inferior {m.ObjBound:.3f})")
        ang = ", ".join(f"{a:.3f}" for a in theta - theta[sis.ref])
        print(f"Angulos (rad, ref. barra {sis.barras[sis.ref]}): [{ang}]")
        activos = {kk: round(vv, 3) for kk, vv in dtheta.items() if abs(vv) > 1e-9}
        print(f"dtheta_ijk no nulos: {activos}")
        if res["M_activa"]:
            print(f"ADVERTENCIA: la restriccion big-M esta activa en {res['M_activa']}: "
                  "M podria estar recortando la region factible")
        print("Verificacion por flujo DC: " + ("FACTIBLE" if dc["factible"] else
                                                "INFACTIBLE: " + "; ".join(dc["mensajes"])))
        print(tabla_flujos(sis, dc))
    guardar_json(res, salida / f"milp_{nombre}.json")
    env.dispose()
    return res


def main():
    ap = argparse.ArgumentParser(description="TNEP - modelo M(0-1)LP big-M de Villasana (Gurobi)")
    ap.add_argument("--datos", default=str(CARPETA / "datos" / "garver6_tnep.xlsx"))
    ap.add_argument("--salida", default=None, help="carpeta de resultados")
    ap.add_argument("--bigM", type=float, default=None, help="valor de M (rad); anula la base de datos")
    ap.add_argument("--modo", choices=["fijo", "auto"], default=None, help="calculo de M")
    ap.add_argument("--tiempo", type=float, default=None, help="limite de tiempo (s)")
    args = ap.parse_args()
    resolver(args.datos, args.salida, M_fijo=args.bigM, modo=args.modo, limite_tiempo=args.tiempo)


if __name__ == "__main__":
    main()
