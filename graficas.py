# -*- coding: utf-8 -*-
"""
graficas.py - Genera las figuras del informe (PDF vectorial) a partir de
resultados/resumen.json (producido por ejecutar_todo.py).

Convenciones de color (fijas en todo el informe; el color sigue a la entidad):
  LP = azul, MINLP = naranja, MILP big-M = aqua, valores de TNEP.pdf = gris;
  en los diagramas unifilares: red existente = gris oscuro, lineas nuevas =
  verde (como en las figuras de TNEP.pdf), corredores candidatos = trazos.

Uso:  python graficas.py [--png carpeta_vista_previa]
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

CARPETA = Path(__file__).resolve().parent
RESULTADOS = CARPETA / "resultados"
FIGURAS = CARPETA.parent / "figuras"

# ---------------- paleta y estilo ----------------
TINTA, TINTA2, TENUE = "#0b0b0b", "#52514e", "#898781"
REJILLA, EJE = "#e1e0d9", "#c3c2b7"
C_LP, C_MINLP, C_MILP, C_REF = "#2a78d6", "#eb6834", "#1baf7a", "#898781"
C_NUEVA, C_CRITICO = "#008300", "#d03b3b"
COLOR_METODO = {"lp": C_LP, "minlp": C_MINLP, "milp": C_MILP}
NOMBRE_METODO = {"lp": "LP iterativo", "minlp": "MINLP bilineal", "milp": "MILP big-M"}
UNA_COL, DOS_COL = 3.5, 7.16   # pulgadas (IEEEtran)

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Arial"],
    "font.size": 7.5, "axes.titlesize": 8, "axes.labelsize": 7.5,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 6.8,
    "axes.edgecolor": EJE, "axes.linewidth": 0.6, "axes.labelcolor": TINTA2,
    "xtick.color": TINTA2, "ytick.color": TINTA2, "xtick.major.width": 0.6,
    "ytick.major.width": 0.6, "axes.grid": True, "grid.color": REJILLA,
    "grid.linewidth": 0.5, "grid.linestyle": "-", "axes.axisbelow": True,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
    "lines.linewidth": 1.4, "lines.solid_capstyle": "round", "pdf.fonttype": 42,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.02, "figure.dpi": 150,
    "axes.titleweight": "bold", "axes.titlecolor": TINTA, "text.color": TINTA,
})


def guardar(fig, nombre, png=None):
    FIGURAS.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURAS / f"{nombre}.pdf")
    if png:
        Path(png).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(png) / f"{nombre}.png", dpi=220)
    plt.close(fig)


# =====================================================================
# Diagramas unifilares de Garver
# =====================================================================
POS = {1: (0.88, 1.00), 2: (0.44, 0.56), 3: (0.10, 0.80), 4: (0.88, 0.04),
       5: (0.47, 1.00), 6: (0.30, 0.04)}
DATOS_BARRA = {1: (50, 80), 2: (0, 240), 3: (165, 40), 4: (0, 160), 5: (0, 240), 6: (545, 0)}


def _paralelas(ax, p, q, n, color, lw, ls="-", sep=0.012, desplazar=0.0, z=2):
    p, q = np.array(p, float), np.array(q, float)
    d = q - p
    normal = np.array([-d[1], d[0]]) / np.linalg.norm(d)
    for i in range(n):
        o = normal * (sep * (i - (n - 1) / 2) + desplazar)
        ax.plot(*zip(p + o, q + o), color=color, lw=lw, ls=ls, zorder=z, solid_capstyle="butt")
    return normal


def _barras(ax, mostrar_datos=True):
    for b, (x, y) in POS.items():
        ax.plot([x - 0.045, x + 0.045], [y, y], color=TINTA, lw=3.2, zorder=5, solid_capstyle="butt")
        dx = -0.075 if b in (3, 6) else 0.07
        ax.text(x + dx * 0.55, y + 0.035, f"{b}", ha="center", va="bottom", fontsize=8,
                fontweight="bold", color=TINTA, zorder=6)
        if mostrar_datos:
            pg, pl = DATOS_BARRA[b]
            texto = (f"G {pg}" if pg else "") + ("\n" if pg and pl else "") + (f"D {pl}" if pl else "")
            ha = "right" if b in (3, 6) else "left"
            # la barra 2 tiene lineas por debajo: su rotulo va a la derecha, a la altura de la barra
            dy = 0.005 if b == 2 else -0.03
            ax.text(x + (-0.06 if ha == "right" else 0.06), y + dy, texto + " MW", ha=ha, va="top",
                    fontsize=6.3, color=TINTA2, zorder=6, linespacing=1.1,
                    bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))


def _leyenda_inferior(ax, elementos):
    ax.legend(handles=elementos, loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=len(elementos),
              handlelength=2.2, columnspacing=1.6)


def figura_red_garver(png=None):
    fig, ax = plt.subplots(figsize=(UNA_COL, 3.0))
    existentes = [(1, 2), (1, 4), (1, 5), (2, 3), (2, 4), (3, 5)]
    candidatos = [(6, 2), (6, 4), (6, 5), (3, 5)]
    for i, j in existentes:
        _paralelas(ax, POS[i], POS[j], 1, TINTA2, 1.1)
    for i, j in candidatos:
        _paralelas(ax, POS[i], POS[j], 1, C_NUEVA, 0.9, ls=(0, (3, 2)),
                   desplazar=0.022 if (i, j) == (3, 5) else 0.0)
    etiquetas = {(6, 2): "6-2: c=150, n≤ 4", (6, 4): "6-4: c=150, n≤ 4",
                 (6, 5): "6-5: c=305, n≤ 3", (3, 5): "3-5: c=100, n≤ 3"}
    # (texto x, texto y, fraccion del corredor a la que apunta la guia; None = sin guia)
    lugares = {(6, 2): (0.0, 0.30, 0.45), (6, 4): (0.60, 0.075, None), (6, 5): (0.53, 0.875, 0.86),
               (3, 5): (0.10, 0.93, None)}
    for (i, j), (x, y, t) in lugares.items():
        caja = dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9)
        if t is None:
            ax.text(x, y, etiquetas[(i, j)], fontsize=6.2, color=TINTA, ha="center", bbox=caja, zorder=7)
        else:
            p, q = np.array(POS[i]), np.array(POS[j])
            punto = p + (q - p) * t
            ax.annotate(etiquetas[(i, j)], xy=punto, xytext=(x, y), fontsize=6.2, color=TINTA,
                        ha="left", va="center", bbox=caja, zorder=7,
                        arrowprops=dict(arrowstyle="-", color=C_NUEVA, lw=0.6, shrinkA=0, shrinkB=1))
    _barras(ax)
    _leyenda_inferior(ax, [Line2D([], [], color=TINTA2, lw=1.1, label="Línea existente"),
                           Line2D([], [], color=C_NUEVA, lw=0.9, ls=(0, (3, 2)), label="Corredor candidato")])
    ax.set_xlim(-0.08, 1.12)
    ax.set_ylim(-0.08, 1.12)
    ax.set_aspect("equal")
    ax.axis("off")
    guardar(fig, "fig_red_garver", png)


def figura_flujos_garver(resumen, png=None):
    milp = resumen["casos"]["garver6_tnep"]["milp"]
    flujos = milp["flujos_dc"]
    fig, ax = plt.subplots(figsize=(UNA_COL, 3.05))
    for f in flujos:
        i, j = map(int, f["etiqueta"].split("-"))
        nueva = f["tipo"] == "nueva"
        color = C_NUEVA if nueva else TINTA2
        desplazar = 0.022 if (i, j) == (3, 5) and nueva else 0.0
        _paralelas(ax, POS[i], POS[j], f["n"], color, 1.1 if not nueva else 1.0, sep=0.011,
                   desplazar=desplazar)
    # etiquetas de flujo con flecha en el sentido del flujo.
    # (posicion relativa a lo largo de la rama desde la barra 'Desde', lado: +1 a la
    #  izquierda del sentido Desde->Hasta de la etiqueta, -1 a la derecha)
    ubicacion = {("1-2", "existente"): (0.50, 1), ("1-4", "existente"): (0.50, -1),
                 ("1-5", "existente"): (0.50, -1), ("2-3", "existente"): (0.50, 1),
                 ("2-4", "existente"): (0.45, 1), ("3-5", "existente"): (0.55, -1),
                 ("3-5", "nueva"): (0.45, 1), ("6-2", "nueva"): (0.50, 1), ("6-4", "nueva"): (0.50, 1)}
    for f in flujos:
        i, j = map(int, f["etiqueta"].split("-"))
        p, q = np.array(POS[i], float), np.array(POS[j], float)
        t, lado = ubicacion[(f["etiqueta"], f["tipo"])]
        d = (q - p) / np.linalg.norm(q - p)
        normal = np.array([-d[1], d[0]]) * lado
        separacion = 0.045 + (0.012 * (f["n"] - 1) / 2) + (0.022 if f["etiqueta"] == "3-5" and lado > 0 else 0)
        base = p + (q - p) * t + normal * separacion
        sentido = d if f["flujo_MW"] >= 0 else -d
        ax.annotate("", xy=base + sentido * 0.035, xytext=base - sentido * 0.035,
                    arrowprops=dict(arrowstyle="-|>", color=TINTA, lw=0.7, mutation_scale=6), zorder=8)
        texto = f"{abs(f['flujo_MW']):.1f}"
        if f["tipo"] == "nueva":
            texto += f" ({100 * f['carga']:.0f}%)"
        # el texto es ancho: se aleja mas cuando la rama es casi vertical
        ax.text(*(base + normal * (0.065 + 0.075 * abs(normal[0]) * (len(texto) > 6))), texto,
                fontsize=6.0, ha="center", va="center",
                color=TINTA, zorder=9, linespacing=1.0,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))
    _barras(ax)
    _leyenda_inferior(ax, [Line2D([], [], color=TINTA2, lw=1.1, label="Existente"),
                           Line2D([], [], color=C_NUEVA, lw=1.0, label="Nueva (plan óptimo)")])
    ax.set_xlim(-0.08, 1.12)
    ax.set_ylim(-0.08, 1.12)
    ax.set_aspect("equal")
    ax.axis("off")
    guardar(fig, "fig_flujos_garver", png)


# =====================================================================
# LP iterativo
# =====================================================================
def figura_lp_iteraciones(resumen, png=None):
    lp = resumen["casos"]["garver6_tnep"]["lp"]
    hist = lp["historia"]
    pdf = resumen["tnep_pdf_lp"]
    it = np.arange(1, len(hist) + 1)
    obj = [h["objetivo"] for h in hist]
    fig = plt.figure(figsize=(DOS_COL, 2.35), constrained_layout=True)
    gs = fig.add_gridspec(2, 5, width_ratios=[1.55, 1, 1, 1, 1])
    ax = fig.add_subplot(gs[:, 0])
    ax.plot(it, obj, color=C_LP, marker="o", ms=4, label="Gurobi 13 (este trabajo)", zorder=3)
    ax.plot(np.arange(1, len(pdf["objetivo"]) + 1), pdf["objetivo"], ls="none", marker="s", ms=6,
            mfc="none", mec=C_REF, mew=1.0, label="TNEP.pdf (Solver de Excel)", zorder=2)
    for x, y in zip(it, obj):
        ax.text(x + 0.15, y + 18, f"{y:.3f}".rstrip("0").rstrip("."), fontsize=5.8, color=TINTA2)
    ax.set_xlabel("Iteración")
    ax.set_ylabel("Función objetivo (pu)")
    ax.set_title("(a) Costo de la sobrecarga por iteración", loc="left")
    ax.set_xticks(it)
    ax.set_xlim(0.5, 9.2)
    ax.set_ylim(-30, 960)
    ax.legend(loc="upper right")
    # (b) sobrecarga por corredor (pequenos multiplos), corredor elegido resaltado
    corredores = lp["corredores"]
    sob = np.array([h["sobrecarga_MW"] for h in hist])
    elegido = [h.get("corredor_elegido") for h in hist]
    ymax = sob.max() * 1.18
    ejes = [fig.add_subplot(gs[0, 1:3]), fig.add_subplot(gs[0, 3:5]),
            fig.add_subplot(gs[1, 1:3]), fig.add_subplot(gs[1, 3:5])]
    for k, (cid, a) in enumerate(zip(corredores, ejes)):
        colores = [C_LP if elegido[i] == cid else "#c3c2b7" for i in range(len(hist))]
        a.bar(it, sob[:, k], width=0.62, color=colores, zorder=3)
        a.set_ylim(0, ymax)
        a.set_xticks(it)
        a.text(0.98, 0.95, f"Corredor {cid}", transform=a.transAxes, fontsize=7, va="top", ha="right",
               fontweight="bold", color=TINTA)
        for i, v in enumerate(sob[:, k]):
            if elegido[i] == cid:
                a.text(it[i], v + ymax * 0.03, f"{v:.0f}", ha="center", fontsize=5.6, color=TINTA2)
        if k % 2 == 0:
            a.set_ylabel("MW")
        else:
            a.set_yticklabels([])
        if k < 2:
            a.set_xticklabels([])
        else:
            a.set_xlabel("Iteración")
    ejes[0].set_title("(b) Sobrecarga P⁺+P⁻ por corredor (azul: corredor reforzado)", loc="left")
    guardar(fig, "fig_lp_iteraciones", png)


# =====================================================================
# Fuerza bruta
# =====================================================================
def figura_fuerza_bruta(resumen, png=None):
    df = pd.read_csv(RESULTADOS / "fuerza_bruta_garver6_tnep.csv")
    aislada = df.causa.fillna("").str.contains("isla")
    fac = df[df.factible]
    inf = df[~df.factible & ~aislada]
    fig, ax = plt.subplots(figsize=(UNA_COL, 2.45))
    techo = 300
    ax.scatter(inf.costo, np.minimum(100 * inf.carga_max, techo), s=9, color="#c3c2b7", lw=0,
               label=f"Infactible por sobrecarga ({len(inf)})", zorder=2)
    ax.scatter(fac.costo, 100 * fac.carga_max, s=11, color=C_LP, lw=0,
               label=f"Factible ({len(fac)})", zorder=3)
    ax.axhline(100, color=C_CRITICO, lw=0.8, zorder=1)
    ax.text(2950, 104, "límite térmico", fontsize=6, color=TINTA2, ha="right", va="bottom")
    opt = resumen["fuerza_bruta"]["optimo"]
    ax.scatter([opt["costo"]], [100 * opt["carga_max"]], s=60, facecolor="none", edgecolor=TINTA, lw=1.0, zorder=4)
    ax.annotate(f"Óptimo {opt['codigo']} (fila {opt['fila']})\ncosto 1000, carga máx. {100 * opt['carga_max']:.1f}%",
                xy=(opt["costo"], 100 * opt["carga_max"]), xytext=(1250, 30), fontsize=6.2,
                arrowprops=dict(arrowstyle="-", color=TINTA2, lw=0.6, shrinkB=5), color=TINTA)
    for codigo, ytexto in (("4201", 78), ("3301", 56)):
        fila = df[df.codigo.astype(str).str.zfill(4) == codigo].iloc[0]
        ax.scatter([fila.costo], [100 * fila.carga_max], s=26, facecolor="none", edgecolor=TINTA2, lw=0.8, zorder=4)
        ax.annotate(f"{codigo} (fila {fila.fila}): 6-2 al {100 * fila.carga_max:.0f}%",
                    xy=(fila.costo, 100 * fila.carga_max), xytext=(40, ytexto), fontsize=6.0, va="center",
                    arrowprops=dict(arrowstyle="-", color=TINTA2, lw=0.6, shrinkB=3), color=TINTA)
    ax.set_xlabel("Costo de inversión (pu)")
    ax.set_ylabel("Cargabilidad máxima (%)")
    ax.set_ylim(0, techo + 10)
    ax.set_xlim(0, 3100)
    ax.text(3080, 8, f"{int(aislada.sum())} planes dejan aislada la barra 6; cargas > 300 % se dibujan en 300 %",
            fontsize=5.6, color=TENUE, ha="right")
    ax.legend(loc="upper right", markerscale=1.3)
    guardar(fig, "fig_fuerza_bruta", png)


# =====================================================================
# Sensibilidad a big-M
# =====================================================================
def figura_bigM(resumen, png=None):
    g = pd.DataFrame(resumen["bigM_garver"])
    s = pd.DataFrame(resumen["bigM_46"])
    s_fijo = s[s.modo == "fijo"]
    s_auto = s[s.modo == "auto"].iloc[0]
    mcrit = resumen["bigM_critico_garver"]
    fig, ejes = plt.subplots(1, 3, figsize=(DOS_COL, 2.15), constrained_layout=True)
    a = ejes[0]
    a.plot(g.M, g.costo, color=C_MILP, marker="o", ms=3.5, label="Costo del plan MILP", zorder=3)
    a.plot(g.M, g.relajacion, color=TINTA2, marker="v", ms=3.5, lw=1.0, label="Relajación lineal (cota)")
    a.axvline(mcrit, color=C_CRITICO, lw=0.8)
    a.text(mcrit * 1.1, 1128, f"M* = {mcrit:.3f} rad\n(= θ₆ − θ₅)", fontsize=6, color=TINTA2)
    a.axvline(1.0, color=TENUE, lw=0.6)
    a.text(1.12, 925, "M = 1 (Villasana)", fontsize=6, color=TENUE)
    a.set_xscale("log")
    a.set_xlabel("M (rad)")
    a.set_ylabel("Costo (pu)")
    a.set_ylim(860, 1190)
    a.set_title("(a) Garver: costo y cota vs. M", loc="left")
    a.legend(loc="center right", bbox_to_anchor=(1.0, 0.52))
    b = ejes[1]
    limite = s_fijo.estado != "OPTIMO"
    b.plot(s_fijo.M, s_fijo.costo, color=C_MILP, marker="o", ms=3.5, label="Costo del plan MILP", zorder=3)
    b.scatter(s_fijo.M[limite], s_fijo.costo[limite], s=28, facecolor="white", edgecolor=C_MILP, lw=1.2, zorder=4)
    for _, fila in s_fijo[limite].iterrows():
        b.annotate(f"límite de 120 s\n(brecha {100 * fila.brecha:.0f}%)", xy=(fila.M, fila.costo),
                   xytext=(fila.M * 1.7, fila.costo - 12), fontsize=5.8, color=TINTA2, va="top")
    b.plot(s_fijo.M, s_fijo.relajacion, color=TINTA2, marker="v", ms=3.5, lw=1.0, label="Relajación lineal (cota)")
    b.axhline(resumen["literatura_46"], color=TENUE, lw=0.6)
    b.text(300, resumen["literatura_46"] + 4, "óptimo publicado", fontsize=6, color=TENUE, ha="center")
    b.set_xscale("log")
    b.set_xlabel("M (rad)")
    b.set_ylabel("Costo (MUS$)")
    b.set_title("(b) 46 barras: costo y cota vs. M", loc="left")
    b.legend(loc="lower right", bbox_to_anchor=(1.0, 0.12))
    c = ejes[2]
    c.plot(s_fijo.M, s_fijo.tiempo_s, color=C_MILP, marker="o", ms=3.5, label="M fijo")
    c.axhline(s_auto.tiempo_s, color=C_MINLP, lw=0.9, label="M automático (camino mínimo)")
    c.set_xscale("log")
    c.set_yscale("log")
    c.set_xlabel("M (rad)")
    c.set_ylabel("Tiempo Gurobi (s)")
    c.set_title("(c) 46 barras: tiempo de solución", loc="left")
    c.legend(loc="upper right")
    guardar(fig, "fig_bigM", png)


# =====================================================================
# Convergencia MILP vs MINLP (46 barras)
# =====================================================================
def figura_convergencia(resumen, png=None):
    caso = resumen["casos"]["sur46_sin_redespacho"]
    fig, ax = plt.subplots(figsize=(UNA_COL, 2.35))
    for metodo in ("milp", "minlp"):
        pts = [p for p in caso[metodo]["convergencia"]]
        t = [max(p[0], 1e-3) for p in pts]
        inc = [p[1] for p in pts]
        cot = [p[2] for p in pts]
        tt = [x for x, y in zip(t, inc) if y is not None]
        yy = [y for y in inc if y is not None]
        tfin = caso[metodo]["estadisticas"]["tiempo_s"]
        ax.step(tt + [tfin], yy + [yy[-1]], where="post", color=COLOR_METODO[metodo], lw=1.4,
                label=f"{NOMBRE_METODO[metodo]}: incumbente")
        tc = [x for x, y in zip(t, cot) if y is not None]
        yc = [y for y in cot if y is not None]
        ax.step(tc + [tfin], yc + [caso[metodo]["cota"]], where="post", color=COLOR_METODO[metodo], lw=0.9,
                alpha=0.75, ls=(0, (1, 1)), label=f"{NOMBRE_METODO[metodo]}: cota inferior")
    ax.axhline(caso["lp"]["costo"], color=C_LP, lw=0.9)
    ax.text(0.0012, caso["lp"]["costo"] + 2, f"plan LP iterativo: {caso['lp']['costo']:.3f}", fontsize=6,
            color=TINTA2)
    ax.axhline(resumen["literatura_46"], color=TENUE, lw=0.6)
    ax.text(0.0012, resumen["literatura_46"] - 9, "óptimo publicado: 154.420", fontsize=6, color=TINTA2)
    ax.set_xscale("log")
    ax.set_xlim(1e-3, None)
    ax.set_ylim(60, 260)
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Costo (MUS$)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2, fontsize=6)
    guardar(fig, "fig_convergencia46", png)


# =====================================================================
# Comparacion y escalabilidad
# =====================================================================
def figura_escalabilidad(resumen, png=None):
    casos = list(resumen["casos"].keys())
    etiquetas = ["Garver\n4 corredores", "Garver\n15 corredores", "Sur 46 barras\n79 corredores"]
    fig, ejes = plt.subplots(1, 3, figsize=(DOS_COL, 2.2), constrained_layout=True)
    x = np.arange(len(casos))
    ancho = 0.24
    for j, metodo in enumerate(("lp", "minlp", "milp")):
        sobre, tiempo = [], []
        for caso in casos:
            r = resumen["casos"][caso][metodo]
            opt = resumen["casos"][caso]["milp"]["costo"]
            sobre.append(100 * (r["costo"] - opt) / opt)
            tiempo.append(r["tiempo_total_s"] if metodo == "lp" else r["estadisticas"]["tiempo_s"])
        ejes[0].bar(x + (j - 1) * ancho, sobre, width=ancho * 0.88, color=COLOR_METODO[metodo],
                    label=NOMBRE_METODO[metodo], zorder=3)
        for xi, v in zip(x + (j - 1) * ancho, sobre):
            ejes[0].text(xi, v + 0.15, f"{v:.1f}", ha="center", fontsize=5.6, color=TINTA2)
        ejes[1].bar(x + (j - 1) * ancho, tiempo, width=ancho * 0.88, color=COLOR_METODO[metodo], zorder=3)
        for xi, v in zip(x + (j - 1) * ancho, tiempo):
            ejes[1].text(xi, v * 1.15, f"{v:.3f}" if v < 1 else f"{v:.2f}", ha="center", fontsize=5.2,
                         color=TINTA2, rotation=90, va="bottom")
    ejes[0].set_xticks(x, etiquetas)
    ejes[0].set_ylabel("Sobrecosto vs. óptimo (%)")
    ejes[0].set_title("(a) Calidad de la solución", loc="left")
    ejes[0].set_ylim(0, 9.5)
    ejes[0].legend(loc="upper left")
    ejes[1].set_xticks(x, etiquetas)
    ejes[1].set_yscale("log")
    ejes[1].set_ylim(3e-3, 60)
    ejes[1].set_ylabel("Tiempo de cómputo (s)")
    ejes[1].set_title("(b) Tiempo (Gurobi)", loc="left")
    # (c) escalamiento con n_max en el sistema de 46 barras
    nm = pd.DataFrame([f for f in resumen["nmax"] if f["sistema"] == "sur46_sin_redespacho"])
    for metodo in ("milp", "minlp"):
        d = nm[nm.metodo == metodo].sort_values("nmax")
        lineas = d.nmax * 79
        ejes[2].plot(lineas, d.tiempo_s, color=COLOR_METODO[metodo], marker="o", ms=3.5,
                     label=NOMBRE_METODO[metodo])
        # MILP: rotulos por encima del punto; MINLP: por debajo (evita que se encimen)
        arriba = metodo == "milp"
        desfase = nm.tiempo_s.max() * (0.05 if arriba else -0.05)
        for lx, t, nod in zip(lineas, d.tiempo_s, d.nodos):
            ejes[2].text(lx, t + desfase, f"{nod / 1000:.1f}k nodos", fontsize=5.4, color=TINTA2,
                         ha="center", va="bottom" if arriba else "top")
    ejes[2].set_xlabel("Líneas candidatas  Σ nᵐᵃˣ (46 barras)")
    ejes[2].set_ylabel("Tiempo (s)")
    ejes[2].set_ylim(-nm.tiempo_s.max() * 0.08, nm.tiempo_s.max() * 1.22)
    ejes[2].set_xlim(150, 870)
    ejes[2].set_title("(c) Escalamiento con nᵐᵃˣ = 3, 5, 10", loc="left")
    ejes[2].legend(loc="upper left")
    guardar(fig, "fig_escalabilidad", png)


def figura_planes46(resumen, png=None):
    caso = resumen["casos"]["sur46_sin_redespacho"]
    cor = caso["milp"]["corredores"]
    lp = np.array(caso["lp"]["plan"])
    opt = np.array(caso["milp"]["plan"])
    usados = [k for k in range(len(cor)) if lp[k] > 0 or opt[k] > 0]
    usados.sort(key=lambda k: (-int(opt[k] > 0), -int(opt[k]), -int(lp[k])))
    fig, ax = plt.subplots(figsize=(UNA_COL, 2.55))
    y = np.arange(len(usados))
    ax.barh(y - 0.19, [opt[k] for k in usados], height=0.36, color=C_MILP,
            label=f"MILP = MINLP (óptimo, {caso['milp']['costo']:.3f} MUS$)", zorder=3)
    ax.barh(y + 0.19, [lp[k] for k in usados], height=0.36, color=C_LP,
            label=f"LP iterativo ({caso['lp']['costo']:.3f} MUS$)", zorder=3)
    ax.set_yticks(y, [cor[k] for k in usados])
    ax.invert_yaxis()
    ax.set_xlabel("Líneas nuevas en el corredor")
    ax.set_xticks([0, 1, 2, 3])
    ax.grid(axis="y", visible=False)
    ax.legend(loc="lower center", bbox_to_anchor=(0.45, 1.0), ncol=1)
    guardar(fig, "fig_planes46", png)


def main():
    ap = argparse.ArgumentParser(description="Figuras del informe")
    ap.add_argument("--png", default=None, help="carpeta opcional para vistas previas PNG")
    args = ap.parse_args()
    resumen = json.loads((RESULTADOS / "resumen.json").read_text(encoding="utf-8"))
    figura_red_garver(args.png)
    figura_flujos_garver(resumen, args.png)
    figura_lp_iteraciones(resumen, args.png)
    figura_fuerza_bruta(resumen, args.png)
    figura_bigM(resumen, args.png)
    figura_convergencia(resumen, args.png)
    figura_escalabilidad(resumen, args.png)
    figura_planes46(resumen, args.png)
    print(f"Figuras escritas en {FIGURAS}")


if __name__ == "__main__":
    main()
