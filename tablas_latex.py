# -*- coding: utf-8 -*-
"""
tablas_latex.py - Escribe en ../tablas/*.tex las tablas del informe a partir de
resultados/resumen.json y de las bases de datos, de modo que cada numero del
informe proviene directamente de la ejecucion de los scripts.

Uso:  python tablas_latex.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

from tnep_comun import cargar_sistema

CARPETA = Path(__file__).resolve().parent
RESULTADOS = CARPETA / "resultados"
TABLAS = CARPETA.parent / "tablas"
NOMBRE = {"lp": "LP iterativo", "minlp": "MINLP bilineal", "milp": "MILP big-M"}


def esc(texto) -> str:
    return (str(texto).replace("\\", r"\textbackslash{}").replace("_", r"\_").replace("%", r"\%")
            .replace("$", r"\$").replace("&", r"\&").replace("#", r"\#"))


def num(valor, dec=3) -> str:
    if valor is None or (isinstance(valor, float) and (math.isnan(valor) or math.isinf(valor))):
        return "--"
    return f"{valor:.{dec}f}"


def plan_latex(texto: str) -> str:
    """'n62=4, n64=2' -> '$n_{62}{=}4$, $n_{64}{=}2$' (compacto para tablas)."""
    partes = []
    for p in texto.split(", "):
        nombre, valor = p.split("=")
        partes.append(f"{nombre[1:]}:{valor}")
    return ", ".join(partes)


def escribir(nombre: str, contenido: str) -> None:
    TABLAS.mkdir(parents=True, exist_ok=True)
    (TABLAS / f"{nombre}.tex").write_text(contenido.strip() + "\n", encoding="utf-8")


def tabla(entorno, titulo, etiqueta, columnas, encabezado, filas, nota=None, tamano=r"\footnotesize",
          separacion="3.2pt"):
    cuerpo = "\n".join(" & ".join(f) + r" \\" for f in filas)
    texto = (f"\\begin{{{entorno}}}[!t]\n\\centering\n\\caption{{{titulo}}}\n\\label{{{etiqueta}}}\n"
             f"{tamano}\n\\setlength{{\\tabcolsep}}{{{separacion}}}\n\\begin{{tabular}}{{{columnas}}}\n\\toprule\n"
             f"{encabezado} \\\\\n\\midrule\n{cuerpo}\n\\bottomrule\n\\end{{tabular}}\n")
    if nota:
        texto += f"\n\\vspace{{2pt}}\\parbox{{0.97\\linewidth}}{{\\scriptsize {nota}}}\n"
    return texto + f"\\end{{{entorno}}}\n"


# ---------------------------------------------------------------------------
def t_datos_garver():
    sis = cargar_sistema(CARPETA / "datos" / "garver6_tnep.xlsx")
    filas = []
    for i, b in enumerate(sis.barras):
        pg, pl = sis.pg[i] * sis.sbase, sis.pl[i] * sis.sbase
        filas.append([str(b), sis.tipo[i], f"{pg:.0f}", f"{pl:.0f}", f"{pg - pl:+.0f}"])
    filas.append([r"\textbf{Total}", "", f"{sis.pg.sum() * 100:.0f}", f"{sis.pl.sum() * 100:.0f}", "0"])
    escribir("tab_barras_garver", tabla(
        "table", "Despacho del año horizonte del sistema de Garver (Tabla~1 de TNEP.pdf)",
        "tab:barras", "ccrrr", r"Barra & Tipo & $P_G$ (MW) & $P_L$ (MW) & Neta (MW)", filas))
    filas = []
    for l in range(sis.nl):
        filas.append([sis.etiqueta_linea(l), "existente", num(sis.l_x[l], 2), f"{sis.l_pmax[l] * 100:.0f}",
                      "--", "--"])
    for k in range(sis.nc):
        filas.append([sis.c_id[k], "candidato", num(sis.c_x[k], 2), f"{sis.c_pmax[k] * 100:.0f}",
                      f"{sis.c_costo[k]:.0f}", str(sis.c_nmax[k])])
    escribir("tab_ramas_garver", tabla(
        "table", "Red existente y corredores candidatos (Tablas~2 y~3 de TNEP.pdf, sec.~6.2)",
        "tab:ramas", "cccccc",
        r"Rama & Tipo & $x$ (pu) & $P^{\max}$ (MW) & $c_{ij}$ (pu) & $n_{ij}^{\max}$", filas,
        nota=r"$x = 0.01$~pu/milla y $c_{ij}$ = número guía de Garver ($5\times$ millas); $S_b=100$~MVA."))


def t_lp_iteraciones(res):
    lp = res["casos"]["garver6_tnep"]["lp"]
    pdf = res["tnep_pdf_lp"]
    filas = []
    for h, obj_pdf, eleg_pdf in zip(lp["historia"], pdf["objetivo"], pdf["elegido"]):
        sob = h["sobrecarga_MW"]
        eleg = h.get("corredor_elegido") or "--"
        filas.append([str(h["iteracion"])] + [num(v, 2) for v in sob] +
                     [num(h["objetivo"], 4), num(obj_pdf, 3 if obj_pdf % 1 else 2), eleg])
    cor = " & ".join(f"{c}" for c in lp["corredores"])
    escribir("tab_lp_iteraciones", tabla(
        "table*", "Iteraciones del modelo LP de Villasana--Garver resuelto con Gurobi (sobrecarga "
                  r"$P^{+}_{Dk}+P^{-}_{Dk}$ en MW) y comparación con TNEP.pdf",
        "tab:lp_iter", "c" + "r" * len(lp["corredores"]) + "rrc",
        rf"Iter. & \multicolumn{{{len(lp['corredores'])}}}{{c}}{{Sobrecarga por corredor (MW)}} & "
        r"f.o. Gurobi & f.o. TNEP.pdf & Refuerzo \\ " + rf"\cmidrule(lr){{2-{1 + len(lp['corredores'])}}}"
        + f" & {cor} & (pu) & (pu) & ", filas,
        nota=(r"En la iteración~7 el libro de Excel del curso reporta 74.2495 con un flujo residual de "
              r"0.29~MW por el corredor 6-5 (costo 305); Gurobi certifica el óptimo exacto 73.7473 "
              r"($P^{+}_{62}=49.16$~MW). La secuencia de refuerzos y el plan final son idénticos.")))


def t_comparacion_garver(res):
    caso = res["casos"]["garver6_tnep"]
    filas = []
    for m in ("lp", "minlp", "milp"):
        r = caso[m]
        if m == "lp":
            hist = r["historia"]
            vars_ = hist[0]["estadisticas"]["variables"]
            restr = hist[0]["estadisticas"]["restricciones"]
            filas.append([NOMBRE[m], plan_latex(r["plan_texto"]), num(r["costo"], 1),
                          f"{r['n_lp_resueltos']} LP", f"{vars_} / 0", str(restr), "--",
                          num(1000 * r["tiempo_total_s"], 1)])
        else:
            e = r["estadisticas"]
            ent = e["binarias"] if m == "milp" else e["enteras"]
            restr = f"{e['restricciones']}" + (f" + {e['restr_cuadraticas']}q" if e["restr_cuadraticas"] else "")
            filas.append([NOMBRE[m], plan_latex(r["plan_texto"]), num(r["costo"], 1),
                          f"{100 * r['brecha']:.2f}\\%", f"{e['variables'] - ent} / {ent}", restr,
                          f"{e.get('nodos', 0):.0f}", num(1000 * e["tiempo_s"], 1)])
    fb = res["fuerza_bruta"]
    filas.append(["Fuerza bruta", plan_latex(fb["optimo"]["plan_texto"]), num(fb["optimo"]["costo"], 1),
                  f"{fb['combinaciones']} planes", "--", "--", "--", num(1000 * fb["tiempo_s"], 1)])
    escribir("tab_comparacion_garver", tabla(
        "table*", "Comparación de los tres métodos en el sistema de Garver (Gurobi~13.0.3, Intel i7-14650HX)",
        "tab:comparacion", "llrcrcrr",
        r"Método & Plan (corredor:líneas) & Costo (pu) & Brecha / iter. & Var. cont./ent. & "
        r"Restricciones & Nodos B\&B & Tiempo (ms)", filas,
        nota=r"``q'': restricciones cuadráticas (bilineales). Para el LP se informa el tamaño del primer "
             r"programa lineal y el tiempo total de las iteraciones."))


def t_solucion_detalle(res):
    caso = res["casos"]["garver6_tnep"]
    milp, minlp = caso["milp"], caso["minlp"]
    ref = 4  # barra 5 (indice 4) es la referencia
    th_milp = np.array(milp["theta"]) - milp["theta"][ref]
    th_minlp = np.array(minlp["theta"]) - minlp["theta"][ref]
    pdf_theta = [0.106, 0.311, 0.187, 0.296, 0.000, 0.579]
    filas = []
    for i in range(6):
        filas.append([rf"$\theta_{{{i + 1}}}$ (rad)", num(th_milp[i]), num(th_minlp[i]), num(pdf_theta[i])])
    for clave, pdf in (("6-2_4", 0.268), ("6-4_2", 0.282), ("3-5_1", 0.187)):
        c, k = clave.split("_")
        filas.append([rf"$\Delta\theta_{{{c.replace('-', '')}{k}}}$ (rad)", num(milp["dtheta"][clave]),
                      "--", num(pdf)])
    activas = sorted(milp["w_activas"])
    filas.append([r"Binarias $=1$", "$" + ",".join(w.replace("w", "w_{") + "}" for w in activas) + "$",
                  "--", "ídem"])
    filas.append([r"$n_{62}, n_{64}, n_{65}, n_{35}$", ", ".join(map(str, milp["plan"])),
                  ", ".join(map(str, minlp["plan"])), "4, 2, 0, 1"])
    filas.append(["Costo (pu)", num(milp["costo"], 1), num(minlp["costo"], 1), "1000"])
    filas.append(["Pérdidas estimadas (MW)", num(milp["perdidas_MW"], 2), num(minlp["perdidas_MW"], 2), "--"])
    escribir("tab_detalle_milp_minlp", tabla(
        "table", "Solución detallada de los modelos MILP big-M ($M=1$~rad) y MINLP frente a TNEP.pdf",
        "tab:detalle", "lccc", r"Variable & MILP big-M & MINLP & TNEP.pdf", filas, separacion="2.6pt",
        nota=r"Ángulos referidos a la barra~5. Las pérdidas se estiman como "
             r"$\sum 2g(1-\cos\Delta\theta)$ con $r=0.0025$~pu/milla (Garver, 1970)."))


def t_fuerza_bruta(res):
    fb = res["fuerza_bruta"]
    df = pd.read_csv(RESULTADOS / "fuerza_bruta_garver6_tnep.csv", dtype={"codigo": str})
    filas = []
    for r in fb["top10_factibles"][:6]:
        filas.append([str(r["fila"]), str(r["codigo"]).zfill(4), num(r["costo"], 0),
                      f"{100 * r['carga_max']:.1f}", "factible"])
    for r in fb["empatados_en_costo"]:
        if not r["factible"]:
            causa = r["causa"].split("(")[0].replace("rama ", "").strip()
            filas.append([str(r["fila"]), str(r["codigo"]).zfill(4), num(r["costo"], 0),
                          f"{100 * r['carga_max']:.1f}", f"infactible ({causa})"])
    escribir("tab_fuerza_bruta", tabla(
        "table", rf"Enumeración exhaustiva de los {fb['combinaciones']} planes "
                 r"(orden $n_{64}n_{62}n_{65}n_{35}$ de TNEP.pdf, sec.~4.1)",
        "tab:fuerza_bruta", "ccrrl", r"Fila & Código & Costo & Carga máx. (\%) & Estado", filas,
        nota=rf"{fb['factibles']} de {fb['combinaciones']} planes son factibles; "
             rf"{int((df.causa.fillna('').str.contains('isla')).sum())} dejan aislada la barra~6."))


def t_relajaciones(res):
    filas = []
    for caso, d in res["casos"].items():
        rel = d["relajaciones"]
        u = d["milp"]["unidad"]
        filas.append([esc(d["titulo"]), u.replace("$", r"\$")] +
                      [f"{num(rel[k]['valor'], 3)} ({rel[k]['brecha_pct']:.1f}\\%)"
                       for k in ("lp_iter1", "relajacion_milp", "relajacion_minlp")] +
                      [num(rel["optimo"]["valor"], 3)])
    escribir("tab_relajaciones", tabla(
        "table*", "Cotas inferiores que ofrece cada formulación (entre paréntesis, brecha respecto al óptimo)",
        "tab:relajaciones", "llrrrr",
        r"Sistema & Unidad & LP Villasana (iter.~1) & Relajación lineal MILP & Relajación continua MINLP & "
        r"Óptimo entero", filas,
        nota=r"La relajación continua del MINLP sigue siendo un problema no convexo; se resolvió con "
             r"ramificación espacial (límite de 120~s, se informa la cota global certificada)."))


def t_bigM(res):
    filas = []
    for r in res["bigM_garver"]:
        filas.append([num(r["M"], 2), plan_latex(r["plan"]), num(r["costo"], 0), num(r["relajacion"], 2),
                      f"{r['nodos']:.0f}", num(1000 * r["tiempo_s"], 1)])
    escribir("tab_bigM_garver", tabla(
        "table", "Sensibilidad del MILP de Villasana a la constante big-M (Garver)",
        "tab:bigM", "clrrrr", r"$M$ (rad) & Plan & Costo & Relaj. LP & Nodos & $t$ (ms)", filas,
        nota=rf"Valor crítico obtenido por bisección: $M^*={res['bigM_critico_garver']:.4f}$~rad; "
             r"con $M<M^*$ la banda~\eqref{eq:milp_bigm} prohíbe la apertura angular $\theta_6-\theta_5=0.579$~rad del "
             r"plan óptimo y el MILP converge, sin advertencia, a un plan más costoso."))
    filas = []
    for r in res["bigM_46"]:
        etiqueta = "auto" if r["modo"] == "auto" else num(r["M"], 2)
        marca = "" if r["estado"] == "OPTIMO" else r"$^\dagger$"
        filas.append([etiqueta, num(r["costo"], 3) + marca, num(r["relajacion"], 3), f"{r['nodos']:.0f}",
                      num(r["tiempo_s"], 2)])
    limitados = [r for r in res["bigM_46"] if r["estado"] != "OPTIMO"]
    nota_limite = "".join(rf" $^\dagger$Límite de 120~s alcanzado con brecha de {100 * r['brecha']:.1f}\,\%."
                          for r in limitados[:1])
    escribir("tab_bigM_46", tabla(
        "table", "Sensibilidad a big-M en el sistema de 46 barras (óptimo publicado: 154.420~MUS\\$)",
        "tab:bigM46", "crrrr", r"$M$ (rad) & Costo (MUS\$) & Relaj. LP & Nodos & $t$ (s)", filas,
        nota=r"``auto'': $M_{ij}$ = camino mínimo angular $\sum x_l P_l^{\max}$ en la red existente "
             r"(respaldo $M=10$~rad para corredores con extremos sin conexión previa)." + nota_limite))


def t_escalabilidad(res):
    filas = []
    for caso, d in res["casos"].items():
        opt = d["milp"]["costo"]
        for m in ("lp", "minlp", "milp"):
            r = d[m]
            if m == "lp":
                e = r["historia"][0]["estadisticas"]
                tam = f"{e['variables']} / 0 / {e['restricciones']}"
                t = r["tiempo_total_s"]
                extra = f"{r['n_lp_resueltos']} LP"
            else:
                e = r["estadisticas"]
                ent = e["binarias"] if m == "milp" else e["enteras"]
                tam = f"{e['variables'] - ent} / {ent} / {e['restricciones'] + e['restr_cuadraticas']}"
                t = e["tiempo_s"]
                extra = f"{e.get('nodos', 0):.0f}"
            filas.append([esc(d["titulo"]) if m == "lp" else "", NOMBRE[m], num(r["costo"], 3),
                          f"{100 * (r['costo'] - opt) / opt:.2f}", tam, extra, num(t, 3)])
        filas[-1][-1] += r" \\[-1pt] \midrule" if caso != list(res["casos"])[-1] else ""
    contenido = tabla(
        "table*", "Desempeño y escalabilidad de los tres métodos en los tres sistemas de prueba",
        "tab:escalabilidad", "llrrcrr",
        r"Sistema & Método & Costo & Sobrecosto (\%) & Var. cont./ent./restr. & Nodos / LP & Tiempo (s)", filas,
        nota=r"Garver: costo en pu; 46 barras: MUS\$ (óptimo publicado 154.420 \cite{romero1994,binato2001}). "
             r"Para el LP se reporta el tamaño de cada programa lineal.")
    contenido = contenido.replace(r" \\[-1pt] \midrule \\", r" \\ \midrule")
    escribir("tab_escalabilidad", contenido)


def t_planes46(res):
    caso = res["casos"]["sur46_sin_redespacho"]
    cor = caso["milp"]["corredores"]
    lp, opt, minlp = caso["lp"]["plan"], caso["milp"]["plan"], caso["minlp"]["plan"]
    sis = cargar_sistema(CARPETA / "datos" / "sur46_sin_redespacho.xlsx")
    lit = {"20-21": 1, "42-43": 2, "46-6": 1, "19-25": 1, "31-32": 1, "28-30": 1, "26-29": 3,
           "24-25": 2, "29-30": 2, "5-6": 2}
    usados = [k for k in range(len(cor)) if lp[k] or opt[k] or minlp[k]]
    usados.sort(key=lambda k: (-(opt[k] > 0), cor[k]))
    filas = []
    for k in usados:
        filas.append([cor[k], num(sis.c_costo[k], 3), str(lp[k] or "--"), str(minlp[k] or "--"),
                      str(opt[k] or "--"), str(lit.get(cor[k], "--"))])
    filas.append([r"\textbf{Costo}", "", num(caso["lp"]["costo"], 3), num(caso["minlp"]["costo"], 3),
                  num(caso["milp"]["costo"], 3), "154.420"])
    escribir("tab_planes46", tabla(
        "table", "Planes de expansión del sistema Sur de Brasil de 46 barras (sin redespacho)",
        "tab:planes46", "lrcccc", r"Corredor & $c$ (MUS\$) & LP & MINLP & MILP & Literatura", filas,
        nota=r"Literatura: plan óptimo publicado por Romero y Monticelli \cite{romero1994}, con optimalidad "
             r"probada por Binato \emph{et al.} \cite{binato2001}; plan tomado de \cite{taglialenha2008}."))


def t_ac(res):
    ac = res["validacion_ac"]
    filas = []
    def sin_menos_cero(texto):
        return "0.0" if texto == "-0.0" else texto

    for b in ac["barras"]:
        filas.append([str(b["barra"]), b["tipo"].replace("Vtheta", r"V$\theta$"), num(b["V"], 3),
                      num(b["ang_grados"], 2), num(b["V_garver"], 2), num(b["ang_garver"], 1),
                      sin_menos_cero(num(b["P_MW"], 1)), sin_menos_cero(num(b["Q_MVAr"], 1))])
    escribir("tab_ac", tabla(
        "table", "Flujo de carga AC (Newton--Raphson) del plan óptimo frente a la Fig.~10 de Garver (1970)",
        "tab:ac", "cccrcrrr",
        r"Barra & Tipo & $|V|$ & $\theta$ ($^\circ$) & $|V|_{G}$ & $\theta_{G}$ ($^\circ$) & $P$ (MW) & $Q$ (MVAr)",
        filas, nota=rf"Convergencia en {ac['iteraciones']} iteraciones; pérdidas {ac['perdidas_MW']:.2f}~MW; "
                    r"subíndice $G$: valores publicados por Garver."))


CORTO = {"garver6_tnep": "Garver (4 corr.)", "garver6_15corredores": "Garver (15 corr.)",
         "sur46_sin_redespacho": "Sur 46 barras"}
CORTO_METODO = {"lp": "LP", "minlp": "MINLP", "milp": "MILP"}


def t_nmax_criterio(res):
    filas = []
    for f in res["nmax"]:
        sistema = "Garver" if f["sistema"].startswith("garver") else "46 barras"
        nmax = "5 (6-2, 6-4)" if f["sistema"].startswith("garver") else f"{f['nmax']} (todos)"
        ent = f["binarias"] if f["metodo"] == "milp" else f["enteras"]
        filas.append([sistema, nmax, CORTO_METODO[f["metodo"]], num(f["costo"], 3), str(ent),
                      f"{f['nodos']:.0f}", num(f["tiempo_s"], 2)])
    escribir("tab_nmax", tabla(
        "table", r"Sensibilidad a $n^{\max}$ (enteras: binarias en el MILP)",
        "tab:nmax", "lllrrrr", r"Sistema & $n^{\max}$ & Mét. & Costo & Enteras & Nodos & $t$ (s)", filas,
        separacion="2.6pt",
        nota="Garver: variante del libro Excel MILP del curso (TNEP.pdf fija 4 en 6-2 y 6-4)."))
    filas = []
    for f in res["criterio_lp"]:
        filas.append([CORTO[f["caso"]], f["criterio"], num(f["costo"], 3),
                      str(f["lp_resueltos"]), "sí" if f["factible"] else "no"])
    escribir("tab_criterio_lp", tabla(
        "table", "Efecto de la regla de selección del corredor en el LP iterativo",
        "tab:criterio", "llrcc", r"Sistema & Criterio & Costo & LP & Factible", filas,
        nota=r"flujo: mayor $(P^{+}+P^{-})/P^{\max}$ (TNEP.pdf); costo: mayor $c_k(P^{+}+P^{-})/P^{\max}$."))


def frase_relajacion(rel: dict) -> str:
    """Redacta el resultado de la relajacion continua del MINLP segun su estado real."""
    nodos = rel["nodos"] / 1e6
    if rel["estado"] == 2:   # GRB.OPTIMAL
        return (rf"requiere {rel['tiempo_s']:.0f}~s y {nodos:.2f}~millones de nodos de ramificación "
                rf"espacial para cerrarse en {rel['valor']:.2f}~MUS\$")
    incumbente = rel.get("incumbente")
    extra = rf" y mejor solución {incumbente:.2f}" if incumbente is not None else ""
    return (rf"no se cierra en {rel['tiempo_s']:.0f}~s ({nodos:.2f}~millones de nodos; cota "
            rf"{rel['valor']:.2f}{extra}~MUS\$)")


def potencia10(valor: float) -> str:
    """1.2e-13 -> '1\\times10^{-13}' (modo matematico); valores ~0 -> '0'."""
    if abs(valor) < 1e-15:
        return "0"
    mantisa, exponente = f"{valor:.0e}".split("e")
    return rf"{mantisa}\times10^{{{int(exponente)}}}"


def desviacion_theta(res) -> float:
    """Maxima diferencia entre los angulos del LP (redondeados a 2 decimales, ref. barra 5)
    y los publicados en TNEP.pdf, en todas las iteraciones."""
    hist = res["casos"]["garver6_tnep"]["lp"]["historia"]
    peor = 0.0
    for h, publicado in zip(hist, res["tnep_pdf_lp"]["theta"]):
        th = np.array(h["theta"]) - h["theta"][4]
        for calculado, ref in zip(th, publicado):
            if ref is not None:
                peor = max(peor, abs(round(calculado, 2) - ref))
    return peor


def t_highs():
    """Tabla de la validacion cruzada con HiGHS (si se ejecuto validacion_highs.py)."""
    ruta = RESULTADOS / "validacion_highs.json"
    if not ruta.exists():
        escribir("tab_highs", "% validacion_highs.py no se ejecuto")
        return None
    v = json.loads(ruta.read_text(encoding="utf-8"))
    filas = []
    for f in v["milp"]:
        lps = [g for g in v["lp"] if g["caso"] == f["caso"]]
        breve = {"garver6_tnep": "Garver-4", "garver6_15corredores": "Garver-15",
                 "sur46_sin_redespacho": "Sur-46"}[f["caso"]]
        filas.append([breve, num(f["gurobi"], 3), num(f["highs"], 3), num(f["tiempo_gurobi_s"], 2),
                      num(f["tiempo_highs_s"], 2), "sí" if f.get("mismo_plan") else "no",
                      f"{sum(g.get('mismo_refuerzo', False) for g in lps)}/{len(lps)}",
                      "$" + potencia10(max(g["diferencia"] for g in lps)) + "$"])
    escribir("tab_highs", tabla(
        "table", rf"Validación cruzada con HiGHS~{v['version_highs']}: MILP big-M y programas lineales del LP iterativo",
        "tab:highs", "lrrrrccc",
        r"Sistema & $z_G$ & $z_H$ & $t_G$ (s) & $t_H$ (s) & Plan & Ref. & máx.\,$|\Delta|$", filas,
        nota=r"Garver-4/15: Garver con 4 o 15 corredores; Sur-46: sistema de 46 barras. "
             r"$z_G$, $z_H$: óptimo del MILP big-M con \gurobi{} y con HiGHS (modelo exportado en MPS); "
             r"$t$: tiempo de solución; Plan: HiGHS elige las mismas líneas por corredor. Ref.: iteraciones "
             r"del LP iterativo en que ambos solvers indican el mismo corredor a reforzar; máx.\,$|\Delta|$: "
             r"mayor diferencia entre los valores óptimos de esos programas lineales.",
        separacion="2.2pt"))
    return v


def valores(res):
    """Macros \\VAL... con los numeros citados en el texto del informe."""
    g, q, s = (res["casos"][c] for c in ("garver6_tnep", "garver6_15corredores", "sur46_sin_redespacho"))
    fb, ac = res["fuerza_bruta"], res["validacion_ac"]
    flujos_ac = {f["rama"]: f for f in ac["flujos"] if f["tipo"] == "nueva"}
    nm = {(f["sistema"], str(f["nmax"]), f["metodo"]): f for f in res["nmax"]}
    bm46 = {("auto" if f["modo"] == "auto" else f["M"]): f for f in res["bigM_46"]}
    bmg = {f["M"]: f for f in res["bigM_garver"]}
    lp7 = g["lp"]["historia"][6]

    def e(caso, metodo):
        return caso[metodo]["estadisticas"]

    v = {
        "lpGarverTiempo": num(1000 * g["lp"]["tiempo_total_s"], 1),
        "lpGarverIterSiete": num(lp7["objetivo"], 4),
        "lpGarverIterSieteMW": num(lp7["sobrecarga_MW"][0], 2),
        "lpUnoGarver": num(g["lp"]["historia"][0]["objetivo"], 2),
        "minlpGarverTiempo": num(1000 * e(g, "minlp")["tiempo_s"], 1),
        "minlpGarverNodos": f"{e(g, 'minlp')['nodos']:.0f}",
        "milpGarverTiempo": num(1000 * e(g, "milp")["tiempo_s"], 1),
        "milpGarverNodos": f"{e(g, 'milp')['nodos']:.0f}",
        "milpGarverVars": str(e(g, "milp")["variables"]),
        "milpGarverBin": str(e(g, "milp")["binarias"]),
        "milpGarverRestr": str(e(g, "milp")["restricciones"]),
        "minlpGarverVars": str(e(g, "minlp")["variables"]),
        "minlpGarverRestr": str(e(g, "minlp")["restricciones"]),
        "milpQuinceTiempo": num(1000 * e(q, "milp")["tiempo_s"], 1),
        "milpQuinceBin": str(e(q, "milp")["binarias"]),
        "minlpQuinceTiempo": num(1000 * e(q, "minlp")["tiempo_s"], 1),
        "fbTotal": str(fb["combinaciones"]),
        "fbFactibles": str(fb["factibles"]),
        "fbTiempo": num(fb["tiempo_s"], 2),
        "acIter": str(ac["iteraciones"]),
        "acPerdidas": num(ac["perdidas_MW"], 2),
        "acSlack": num(ac["generacion_compensadora_MW"], 1),
        "acEnvioSeisDos": num(flujos_ac["6-2"]["P_envio_MW"], 1),
        "acCargaSeisDos": num(flujos_ac["6-2"]["carga_pct"], 1),
        "acEnvioSeisCuatro": num(flujos_ac["6-4"]["P_envio_MW"], 1),
        "acCargaSeisCuatro": num(flujos_ac["6-4"]["carga_pct"], 1),
        "bigMcritico": num(res["bigM_critico_garver"], 4),
        "bigMgarverRelaxUno": num(bmg[1.0]["relajacion"], 2),
        "bigMgarverRelaxMil": num(bmg[1000.0]["relajacion"], 2),
        "lpSurCosto": num(s["lp"]["costo"], 3),
        "lpSurSobrecosto": f"{100 * (s['lp']['costo'] - s['milp']['costo']) / s['milp']['costo']:.1f}",
        "lpSurIter": str(s["lp"]["n_lp_resueltos"]),
        "lpSurTiempo": num(1000 * s["lp"]["tiempo_total_s"], 0),
        "lpUnoSur": num(s["lp"]["historia"][0]["objetivo"], 2),
        "minlpSurTiempo": num(e(s, "minlp")["tiempo_s"], 2),
        "minlpSurNodos": f"{e(s, 'minlp')['nodos']:.0f}",
        "minlpSurVars": str(e(s, "minlp")["variables"]),
        "minlpSurEnt": str(e(s, "minlp")["enteras"]),
        "milpSurTiempo": num(e(s, "milp")["tiempo_s"], 2),
        "milpSurNodos": f"{e(s, 'milp')['nodos']:.0f}",
        "milpSurVars": str(e(s, "milp")["variables"]),
        "milpSurBin": str(e(s, "milp")["binarias"]),
        "milpSurRestr": str(e(s, "milp")["restricciones"]),
        "relaxMilpSur": num(s["relajaciones"]["relajacion_milp"]["valor"], 2),
        "relaxMinlpSur": num(s["relajaciones"]["relajacion_minlp"]["valor"], 2),
        "relaxMinlpSurTiempo": num(s["relajaciones"]["relajacion_minlp"]["tiempo_s"], 0),
        "relaxMinlpSurNodos": f"{s['relajaciones']['relajacion_minlp']['nodos'] / 1e6:.2f}",
        "relaxMilpGarver": num(g["relajaciones"]["relajacion_milp"]["valor"], 2),
        "relaxMinlpGarver": num(g["relajaciones"]["relajacion_minlp"]["valor"], 2),
        "bigMsurAutoTiempo": num(bm46["auto"]["tiempo_s"], 2),
        "bigMsurAutoNodos": f"{bm46['auto']['nodos']:.0f}",
        "bigMsurUnoNodos": f"{bm46[1.0]['nodos']:.0f}",
        "bigMsurUnoTiempo": num(bm46[1.0]["tiempo_s"], 2),
        "bigMsurMilNodos": f"{bm46[1000.0]['nodos']:.0f}",
        "bigMsurMilTiempo": num(bm46[1000.0]["tiempo_s"], 2),
        "bigMsurRelax": num(bm46[1.0]["relajacion"], 2),
        "bigMcamino": str(sum(1 for o in s["milp"]["bigM_origen"] if o == "camino")),
        "bigMrazon": num(1.0 / res["bigM_critico_garver"], 2),
        "tiempoArbolMin": num(min(e(s, "milp")["tiempo_s"], bm46["auto"]["tiempo_s"],
                                  nm[("sur46_sin_redespacho", "3", "milp")]["tiempo_s"]), 1),
        "tiempoArbolMax": num(max(e(s, "milp")["tiempo_s"], bm46["auto"]["tiempo_s"],
                                  nm[("sur46_sin_redespacho", "3", "milp")]["tiempo_s"]), 1),
        "relaxMinlpSurInc": num(s["relajaciones"]["relajacion_minlp"]["incumbente"], 2),
        "minlpRelaxGarverBrecha": f"{g['relajaciones']['relajacion_minlp']['brecha_pct']:.1f}",
        "bigMsurUnoCosto": num(bm46[1.0]["costo"], 3),
        "bigMsurMedioCosto": num(bm46[0.5]["costo"], 3),
        "bigMsurCuartoCosto": num(bm46[0.25]["costo"], 3),
        "bigMsurCuartoEstado": "límite de tiempo" if bm46[0.25]["estado"] != "OPTIMO" else "óptimo",
        "bigMsurCuartoBrecha": num(100 * (bm46[0.25]["brecha"] or 0), 1),
        "nmaxDiezMilpT": num(nm[("sur46_sin_redespacho", "10", "milp")]["tiempo_s"], 2),
        "nmaxDiezMinlpT": num(nm[("sur46_sin_redespacho", "10", "minlp")]["tiempo_s"], 2),
        "nmaxDiezBin": str(nm[("sur46_sin_redespacho", "10", "milp")]["binarias"]),
        "tiempoTotal": num(res["tiempo_total_s"] / 60, 1),
        "lpThetaDesv": num(desviacion_theta(res), 3),
        "relaxMinlpSurTexto": frase_relajacion(s["relajaciones"]["relajacion_minlp"]),
    }
    hv = t_highs()
    if hv:
        s46 = next(f for f in hv["milp"] if f["caso"] == "sur46_sin_redespacho")
        v.update(highsVersion=hv["version_highs"], highsNumLP=str(len(hv["lp"])),
                 highsSurTiempo=num(s46["tiempo_highs_s"], 1), highsSurGurobi=num(s46["tiempo_gurobi_s"], 2),
                 highsMaxDif=potencia10(max(f["diferencia"] for f in hv["lp"] + hv["milp"])),
                 highsPlanes=f"{sum(f.get('mismo_plan', False) for f in hv['milp'])}/{len(hv['milp'])}",
                 highsRefuerzos=f"{sum(f.get('mismo_refuerzo', False) for f in hv['lp'])}/{len(hv['lp'])}")
    texto = "% Generado automaticamente por codigo/tablas_latex.py -- no editar a mano\n"
    texto += "\n".join(f"\\newcommand{{\\VAL{k}}}{{{val}}}" for k, val in v.items())
    escribir("valores", texto)


def extraer_fragmentos():
    """Copia a ../listados/ los bloques de codigo marcados con '# <<nombre' ... '# fin_nombre>>'."""
    destino = CARPETA.parent / "listados"
    destino.mkdir(exist_ok=True)
    for archivo, marca in (("tnep_lp.py", "modelo_lp"), ("tnep_lp.py", "iteraciones_lp"),
                           ("tnep_minlp.py", "modelo_minlp"), ("tnep_milp_bigm.py", "modelo_milp")):
        lineas = (CARPETA / archivo).read_text(encoding="utf-8").splitlines()
        inicio = lineas.index(f"# <<{marca}") + 1
        fin = lineas.index(f"# fin_{marca}>>")
        bloque = "\n".join(lineas[inicio:fin]).rstrip() + "\n"
        if any(ord(ch) > 127 for ch in bloque):
            raise ValueError(f"El fragmento {marca} contiene caracteres no ASCII (problema para listings)")
        (destino / f"{marca}.py").write_text(bloque, encoding="utf-8")


def main():
    res = json.loads((RESULTADOS / "resumen.json").read_text(encoding="utf-8"))
    valores(res)
    extraer_fragmentos()
    t_datos_garver()
    t_lp_iteraciones(res)
    t_comparacion_garver(res)
    t_solucion_detalle(res)
    t_fuerza_bruta(res)
    t_relajaciones(res)
    t_bigM(res)
    t_escalabilidad(res)
    t_planes46(res)
    t_ac(res)
    t_nmax_criterio(res)
    print(f"Tablas escritas en {TABLAS}")


if __name__ == "__main__":
    main()
