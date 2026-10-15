# -*- coding: utf-8 -*-
"""
validacion_ac.py - Prueba de flujo de carga AC (Newton-Raphson) del plan
optimo de Garver, replicando la "AC Load Flow Test" de Garver (1970):
Tabla VI (datos de barra), Tabla VII (datos de linea) y Fig. 10 (resultados).

Garver incrementa la generacion un 2 % para cubrir perdidas (barra 1:
51 MW -> P = 51 - 80 = -29 MW; barra 3: 168.3 MW -> P = 128.3 MW), fija
|V| = 1.02 pu en la barra 1 y 1.04 pu en la barra 3 (PV), Q = 0 en las
barras 2 y 5 (compensacion local), Q = -40 MVAr en la barra 4 (PQ) y la
barra 6 es la compensadora (1.04 /0). Las lineas paralelas se agrupan en
una impedancia equivalente (R/n, X/n), sin efecto capacitivo.

Uso:
    python validacion_ac.py --datos datos/garver6_tnep.xlsx --plan 6-2=4,6-4=2,3-5=1
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np

from tnep_comun import cargar_sistema, encabezado, guardar_json

CARPETA = Path(__file__).resolve().parent

# Garver (1970), Tabla VI. tipo: 'PV', 'PQ' o 'Vtheta'
GARVER_TABLA_VI = {
    1: dict(tipo="PV", P=-29.0, V=1.02),
    2: dict(tipo="PQ", P=-240.0, Q=0.0),
    3: dict(tipo="PV", P=128.3, V=1.04),
    4: dict(tipo="PQ", P=-160.0, Q=-40.0),
    5: dict(tipo="PQ", P=-240.0, Q=0.0),
    6: dict(tipo="Vtheta", V=1.04),
}
# Garver (1970), Fig. 10: |V| (pu) y angulo (grados) del flujo AC publicado
GARVER_FIG10 = {1: (1.02, -31.4), 2: (0.96, -16.9), 3: (1.04, -26.6),
                4: (0.90, -17.3), 5: (0.98, -37.3), 6: (1.04, 0.0)}


def ybus(sis, n_adic):
    """Matriz de admitancias nodal con las lineas existentes y las agregadas."""
    Y = np.zeros((sis.nb, sis.nb), dtype=complex)
    ramas = []
    for l in range(sis.nl):
        ramas.append((sis.l_de[l], sis.l_a[l], sis.l_n0[l], sis.l_r[l], sis.l_x[l], sis.etiqueta_linea(l), "existente"))
    for k in range(sis.nc):
        if n_adic[k] > 0:
            ramas.append((sis.c_de[k], sis.c_a[k], n_adic[k], sis.c_r[k], sis.c_x[k], sis.c_id[k], "nueva"))
    for i, j, n, r, x, *_ in ramas:
        y = n / complex(r, x)
        Y[i, i] += y
        Y[j, j] += y
        Y[i, j] -= y
        Y[j, i] -= y
    return Y, ramas


def newton_raphson(Y, tipos, P_esp, Q_esp, V0, tol=1e-10, max_iter=30):
    """Flujo de carga AC en coordenadas polares (Jacobiano analitico)."""
    nb = len(tipos)
    V = V0.astype(complex)
    pv = [i for i in range(nb) if tipos[i] == "PV"]
    pq = [i for i in range(nb) if tipos[i] == "PQ"]
    pvpq = pv + pq
    historia = []
    for it in range(max_iter):
        S = V * np.conj(Y @ V)
        dP = P_esp[pvpq] - S.real[pvpq]
        dQ = Q_esp[pq] - S.imag[pq]
        error = np.concatenate([dP, dQ])
        historia.append(float(np.max(np.abs(error))))
        if historia[-1] < tol:
            return V, it, historia
        Ibus = Y @ V
        diagV = np.diag(V)
        diagIbus = np.diag(Ibus)
        diagVnorm = np.diag(V / np.abs(V))
        dS_dVa = 1j * diagV @ np.conj(diagIbus - Y @ diagV)
        dS_dVm = diagV @ np.conj(Y @ diagVnorm) + np.conj(diagIbus) @ diagVnorm
        J = np.block([[dS_dVa.real[np.ix_(pvpq, pvpq)], dS_dVm.real[np.ix_(pvpq, pq)]],
                      [dS_dVa.imag[np.ix_(pq, pvpq)], dS_dVm.imag[np.ix_(pq, pq)]]])
        dx = np.linalg.solve(J, error)
        Va = np.angle(V)
        Vm = np.abs(V)
        Va[pvpq] += dx[:len(pvpq)]
        Vm[pq] += dx[len(pvpq):]
        V = Vm * np.exp(1j * Va)
    raise RuntimeError("Newton-Raphson no convergio")


def resolver(ruta_datos, plan_txt, carpeta_salida=None, verbose=True):
    sis = cargar_sistema(ruta_datos)
    n_adic = np.zeros(sis.nc, dtype=int)
    for parte in plan_txt.split(","):
        cid, valor = parte.split("=")
        n_adic[sis.c_id.index(cid.strip())] = int(valor)
    Y, ramas = ybus(sis, n_adic)
    tipos, P, Q, V0 = [], np.zeros(sis.nb), np.zeros(sis.nb), np.ones(sis.nb)
    for i, b in enumerate(sis.barras):
        d = GARVER_TABLA_VI[b]
        tipos.append(d["tipo"])
        P[i] = d.get("P", 0.0) / sis.sbase
        Q[i] = d.get("Q", 0.0) / sis.sbase
        V0[i] = d.get("V", 1.0)
    V, iteraciones, historia = newton_raphson(Y, tipos, P, Q, V0)
    S = V * np.conj(Y @ V) * sis.sbase
    flujos = []
    for i, j, n, r, x, etiqueta, tipo in ramas:
        y = n / complex(r, x)
        sij = V[i] * np.conj((V[i] - V[j]) * y) * sis.sbase
        sji = V[j] * np.conj((V[j] - V[i]) * y) * sis.sbase
        # capacidad termica del grupo de circuitos (MW nominales)
        if tipo == "existente":
            cap = n * sis.l_pmax[[sis.etiqueta_linea(l) for l in range(sis.nl)].index(etiqueta)] * sis.sbase
        else:
            cap = n * sis.c_pmax[sis.c_id.index(etiqueta)] * sis.sbase
        flujos.append(dict(rama=etiqueta, tipo=tipo, n=int(n), P_envio_MW=sij.real, Q_envio_MVAr=sij.imag,
                           P_recibo_MW=-sji.real, perdidas_MW=(sij + sji).real, capacidad_MW=cap,
                           carga_pct=100 * max(abs(sij.real), abs(sji.real)) / cap))
    barras = []
    for i, b in enumerate(sis.barras):
        ref_V, ref_ang = GARVER_FIG10.get(b, (None, None))
        barras.append(dict(barra=b, tipo=tipos[i], V=abs(V[i]), ang_grados=math.degrees(np.angle(V[i])),
                           P_MW=S[i].real, Q_MVAr=S[i].imag, V_garver=ref_V, ang_garver=ref_ang))
    perdidas = float(sum(f["perdidas_MW"] for f in flujos))
    res = dict(plan=plan_txt, iteraciones=iteraciones, error_max=historia, barras=barras, flujos=flujos,
               perdidas_MW=perdidas, generacion_compensadora_MW=float(S[sis.barras.index(6)].real)
               if 6 in sis.barras else None)
    salida = Path(carpeta_salida or CARPETA / "resultados")
    guardar_json(res, salida / f"validacion_ac_{Path(ruta_datos).stem}.json")
    if verbose:
        print(encabezado("PRUEBA DE FLUJO DE CARGA AC (Newton-Raphson) - Garver (1970), Tablas VI y VII"))
        print(f"Plan evaluado: {plan_txt};  convergencia en {iteraciones} iteraciones "
              f"(error final {historia[-1]:.2e} pu)")
        print(f"{'Barra':>5} {'Tipo':>7} {'|V| pu':>8} {'ang (°)':>9} {'P MW':>9} {'Q MVAr':>9}"
              f" | {'|V| Garver':>10} {'ang Garver':>10}")
        for d in barras:
            print(f"{d['barra']:>5} {d['tipo']:>7} {d['V']:>8.3f} {d['ang_grados']:>9.2f} {d['P_MW']:>9.2f} "
                  f"{d['Q_MVAr']:>9.2f} | {d['V_garver']:>10.2f} {d['ang_garver']:>10.1f}")
        print(f"\n{'Rama':>6} {'Tipo':>10} {'n':>2} {'P envio':>9} {'P recibo':>9} {'Perdidas':>9} {'Carga %':>8}")
        for f in flujos:
            print(f"{f['rama']:>6} {f['tipo']:>10} {f['n']:>2} {f['P_envio_MW']:>9.2f} {f['P_recibo_MW']:>9.2f} "
                  f"{f['perdidas_MW']:>9.2f} {f['carga_pct']:>8.1f}")
        print(f"Perdidas totales: {perdidas:.2f} MW;  generacion de la barra compensadora: "
              f"{res['generacion_compensadora_MW']:.1f} MW")
    return res


def main():
    ap = argparse.ArgumentParser(description="Prueba de flujo de carga AC del plan de Garver")
    ap.add_argument("--datos", default=str(CARPETA / "datos" / "garver6_tnep.xlsx"))
    ap.add_argument("--plan", default="6-2=4,6-4=2,3-5=1", help="lineas nuevas por corredor")
    ap.add_argument("--salida", default=None)
    args = ap.parse_args()
    resolver(args.datos, args.plan, args.salida)


if __name__ == "__main__":
    main()
