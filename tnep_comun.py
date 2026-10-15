# -*- coding: utf-8 -*-
"""
tnep_comun.py - Utilidades compartidas por los tres metodos de expansion de
transmision (TNEP): LP iterativo de Villasana-Garver, MINLP bilineal y
MILP M(0-1)LP con linealizacion big-M.

Contiene:
  * Lectura de la base de datos (libro Excel con hojas Parametros, Barras,
    Lineas y Corredores) en la estructura `Sistema`.
  * Flujo de potencia DC de verificacion para un plan de expansion dado
    (identifica islas, sobrecargas y factibilidad).
  * Camino minimo angular (para el calculo automatico de big-M).
  * Utilidades para Gurobi: entorno con bitacora, estadisticas y registro de
    convergencia (incumbente / cota) mediante callback.

Todas las magnitudes electricas internas estan en por unidad (pu) sobre la
base `Sbase_MVA` de la base de datos; los angulos en radianes.
"""
from __future__ import annotations

import heapq
import json
import math
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

try:  # gurobipy solo es necesario para resolver los modelos
    import gurobipy as gp
    from gurobipy import GRB
except ImportError:  # pragma: no cover - permite usar el flujo DC sin Gurobi
    gp = None
    GRB = None


# ==========================================================================
# 1. Estructura de datos del sistema
# ==========================================================================
@dataclass
class Sistema:
    """Red existente + corredores candidatos leidos de la base de datos."""

    nombre: str
    archivo: str
    sbase: float
    barras: list            # etiquetas de barra (enteros)
    tipo: list              # 'existente' | 'futura' | 'nueva'
    pg: np.ndarray          # generacion despachada (pu)
    pl: np.ndarray          # demanda (pu)
    ref: int                # indice (0..nb-1) de la barra de referencia
    # --- red existente (por circuito) ---
    l_de: np.ndarray
    l_a: np.ndarray
    l_n0: np.ndarray        # numero de circuitos existentes en paralelo
    l_x: np.ndarray
    l_r: np.ndarray
    l_pmax: np.ndarray      # pu por circuito
    # --- corredores candidatos (por linea nueva) ---
    c_id: list
    c_de: np.ndarray
    c_a: np.ndarray
    c_x: np.ndarray
    c_r: np.ndarray
    c_pmax: np.ndarray      # pu por linea
    c_costo: np.ndarray     # costo de una linea nueva
    c_nmax: np.ndarray
    param: dict = field(default_factory=dict)

    # ---------------- propiedades de conveniencia ----------------
    @property
    def nb(self) -> int:
        return len(self.barras)

    @property
    def nl(self) -> int:
        return len(self.l_de)

    @property
    def nc(self) -> int:
        return len(self.c_id)

    @property
    def unidad_costo(self) -> str:
        return str(self.param.get("unidad_costo", "pu"))

    def etiqueta_linea(self, l: int) -> str:
        return f"{self.barras[self.l_de[l]]}-{self.barras[self.l_a[l]]}"

    def p(self, nombre: str, defecto=None):
        """Parametro de la hoja 'Parametros' con valor por defecto."""
        valor = self.param.get(nombre, defecto)
        if valor is None or (isinstance(valor, float) and math.isnan(valor)):
            return defecto
        return valor

    def resumen(self) -> str:
        circuitos = int(self.l_n0.sum())
        return (f"{self.nombre}: {self.nb} barras, {self.nl} ramas existentes "
                f"({circuitos} circuitos), {self.nc} corredores candidatos, "
                f"{int(self.c_nmax.sum())} lineas candidatas como maximo, "
                f"demanda {self.pl.sum() * self.sbase:.1f} MW")


def _valor(texto):
    """Convierte el contenido de una celda de 'Parametros' a numero si se puede."""
    if isinstance(texto, (int, float, np.integer, np.floating)):
        return float(texto) if not float(texto).is_integer() else int(texto)
    try:
        numero = float(str(texto).replace(",", "."))
        return int(numero) if numero.is_integer() else numero
    except ValueError:
        return str(texto).strip()


def cargar_sistema(ruta: str | Path) -> Sistema:
    """Lee la base de datos (Excel) y construye la estructura `Sistema`."""
    ruta = Path(ruta)
    hojas = pd.read_excel(ruta, sheet_name=None)
    for requerida in ("Parametros", "Barras", "Lineas", "Corredores"):
        if requerida not in hojas:
            raise ValueError(f"La base de datos {ruta.name} no tiene la hoja '{requerida}'")

    param = {str(f.Parametro).strip(): _valor(f.Valor)
             for f in hojas["Parametros"].itertuples() if pd.notna(f.Parametro)}
    sbase = float(param.get("Sbase_MVA", 100.0))

    def col(df, nombre, tipo=float, relleno=None):
        """Columna como arreglo numpy escribible (pandas 3 entrega vistas de solo lectura)."""
        serie = df[nombre] if relleno is None else df[nombre].fillna(relleno)
        return np.array(serie.to_numpy(tipo), dtype=tipo, copy=True)

    df_b = hojas["Barras"].sort_values("Barra").reset_index(drop=True)
    barras = [int(b) for b in df_b["Barra"]]
    idx = {b: i for i, b in enumerate(barras)}
    tipo = [str(t) for t in df_b.get("Tipo", ["existente"] * len(barras))]
    pg = col(df_b, "PG_MW", relleno=0) / sbase
    pl = col(df_b, "PL_MW", relleno=0) / sbase

    df_l = hojas["Lineas"]
    df_c = hojas["Corredores"]
    if "Circuitos" not in df_l:
        df_l["Circuitos"] = 1
    if "r_pu" not in df_l:
        df_l["r_pu"] = 0.0
    if "r_pu" not in df_c:
        df_c["r_pu"] = 0.0
    if "Corredor" not in df_c:
        df_c["Corredor"] = [f"{int(d)}-{int(h)}" for d, h in zip(df_c.Desde, df_c.Hasta)]

    ref_etiqueta = int(param.get("barra_referencia", barras[0]))
    if ref_etiqueta not in idx:
        raise ValueError(f"La barra de referencia {ref_etiqueta} no existe")

    sis = Sistema(
        nombre=str(param.get("nombre_sistema", ruta.stem)),
        archivo=str(ruta),
        sbase=sbase,
        barras=barras,
        tipo=tipo,
        pg=pg,
        pl=pl,
        ref=idx[ref_etiqueta],
        l_de=np.array([idx[int(b)] for b in df_l["Desde"]], dtype=int),
        l_a=np.array([idx[int(b)] for b in df_l["Hasta"]], dtype=int),
        l_n0=col(df_l, "Circuitos", int, relleno=1),
        l_x=col(df_l, "x_pu"),
        l_r=col(df_l, "r_pu", relleno=0),
        l_pmax=col(df_l, "Pmax_MW") / sbase,
        c_id=[str(c) for c in df_c["Corredor"]],
        c_de=np.array([idx[int(b)] for b in df_c["Desde"]], dtype=int),
        c_a=np.array([idx[int(b)] for b in df_c["Hasta"]], dtype=int),
        c_x=col(df_c, "x_pu"),
        c_r=col(df_c, "r_pu", relleno=0),
        c_pmax=col(df_c, "Pmax_MW") / sbase,
        c_costo=col(df_c, "Costo"),
        c_nmax=col(df_c, "n_max", int),
        param=param,
    )
    validar_sistema(sis)
    return sis


def validar_sistema(sis: Sistema) -> None:
    """Comprobaciones basicas de consistencia de la base de datos."""
    desbalance = (sis.pg.sum() - sis.pl.sum()) * sis.sbase
    if abs(desbalance) > 1e-6:
        raise ValueError(f"Generacion y demanda no balancean ({desbalance:+.3f} MW): "
                         "el modelo sin redespacho exige sum(PG) = sum(PL)")
    if np.any(sis.l_x <= 0) or np.any(sis.c_x <= 0):
        raise ValueError("Todas las reactancias deben ser positivas")
    if np.any(sis.c_nmax < 0):
        raise ValueError("n_max no puede ser negativo")


# ==========================================================================
# 2. Topologia, islas y flujo de potencia DC de verificacion
# ==========================================================================
def ramas_activas(sis: Sistema, n_adic) -> list[dict]:
    """Lista de ramas equivalentes de la red (existente + lineas agregadas).

    Cada rama agrupa los circuitos paralelos de un mismo tipo:
    susceptancia total b = n/x y capacidad total n*Pmax.
    """
    ramas = []
    for l in range(sis.nl):
        n0 = int(sis.l_n0[l])
        if n0 > 0:
            ramas.append(dict(de=int(sis.l_de[l]), a=int(sis.l_a[l]), n=n0,
                              b=n0 / sis.l_x[l], pmax=n0 * sis.l_pmax[l],
                              tipo="existente", indice=l, etiqueta=sis.etiqueta_linea(l)))
    for k in range(sis.nc):
        n = int(round(n_adic[k]))
        if n > 0:
            ramas.append(dict(de=int(sis.c_de[k]), a=int(sis.c_a[k]), n=n,
                              b=n / sis.c_x[k], pmax=n * sis.c_pmax[k],
                              tipo="nueva", indice=k, etiqueta=sis.c_id[k]))
    return ramas


def componentes_conexas(nb: int, aristas) -> list[int]:
    """Etiqueta de isla de cada barra (union-find)."""
    padre = list(range(nb))

    def raiz(i):
        while padre[i] != i:
            padre[i] = padre[padre[i]]
            i = padre[i]
        return i

    for i, j in aristas:
        ri, rj = raiz(i), raiz(j)
        if ri != rj:
            padre[rj] = ri
    return [raiz(i) for i in range(nb)]


def matriz_b(sis: Sistema, ramas: list[dict]) -> np.ndarray:
    """Matriz de susceptancias nodal B (densa) para la lista de ramas."""
    B = np.zeros((sis.nb, sis.nb))
    for r in ramas:
        i, j, b = r["de"], r["a"], r["b"]
        B[i, i] += b
        B[j, j] += b
        B[i, j] -= b
        B[j, i] -= b
    return B


def flujo_dc(sis: Sistema, n_adic, tol: float = 1e-6) -> dict:
    """Flujo de potencia DC de la red expandida con `n_adic` lineas nuevas.

    Devuelve angulos, flujos por rama, cargabilidad y un diagnostico de
    factibilidad (islas con desbalance o ramas sobrecargadas).
    """
    n_adic = np.asarray(n_adic, dtype=float)
    ramas = ramas_activas(sis, n_adic)
    B = matriz_b(sis, ramas)
    p_neta = sis.pg - sis.pl
    isla = componentes_conexas(sis.nb, [(r["de"], r["a"]) for r in ramas])

    mensajes = []
    fijas = []
    for etiqueta in sorted(set(isla)):
        miembros = [i for i in range(sis.nb) if isla[i] == etiqueta]
        desbalance = p_neta[miembros].sum()
        if abs(desbalance) > tol:
            mensajes.append("isla " + str([sis.barras[i] for i in miembros])
                            + f" con desbalance {desbalance * sis.sbase:+.1f} MW")
        fijas.append(sis.ref if sis.ref in miembros else miembros[0])

    libres = [i for i in range(sis.nb) if i not in fijas]
    theta = np.zeros(sis.nb)
    if libres and not mensajes:
        theta[libres] = np.linalg.solve(B[np.ix_(libres, libres)], p_neta[libres])

    flujos = []
    for r in ramas:
        f = r["b"] * (theta[r["de"]] - theta[r["a"]])
        flujos.append(dict(r, flujo_pu=f, flujo_MW=f * sis.sbase,
                           carga=abs(f) / r["pmax"] if r["pmax"] > 0 else 0.0))
    sobrecargas = [f for f in flujos if f["carga"] > 1 + 1e-6]
    for f in sobrecargas:
        mensajes.append(f"rama {f['etiqueta']} ({f['tipo']}) al {100 * f['carga']:.1f}% "
                        f"({abs(f['flujo_MW']):.1f}/{f['pmax'] * sis.sbase:.0f} MW)")
    carga_max = max((f["carga"] for f in flujos), default=0.0)
    return dict(theta=theta, flujos=flujos, factible=not mensajes, mensajes=mensajes,
                carga_max=carga_max, islas=isla)


def perdidas_estimadas(sis: Sistema, n_adic, theta) -> float:
    """Perdidas activas aproximadas (MW) con los angulos DC:
    P_loss = sum_c 2*g_c*(1 - cos(dtheta)), g = r/(r^2 + x^2) por circuito
    (misma expresion del libro Excel MILP/MINLP del curso)."""
    total = 0.0
    for l in range(sis.nl):
        r, x = sis.l_r[l], sis.l_x[l]
        g = r / (r * r + x * x)
        dth = theta[sis.l_de[l]] - theta[sis.l_a[l]]
        total += sis.l_n0[l] * 2 * g * (1 - math.cos(dth))
    for k in range(sis.nc):
        r, x = sis.c_r[k], sis.c_x[k]
        g = r / (r * r + x * x)
        dth = theta[sis.c_de[k]] - theta[sis.c_a[k]]
        total += n_adic[k] * 2 * g * (1 - math.cos(dth))
    return total * sis.sbase


def costo_plan(sis: Sistema, n_adic) -> float:
    return float(np.dot(sis.c_costo, np.asarray(n_adic, dtype=float)))


def texto_plan(sis: Sistema, n_adic) -> str:
    partes = [f"n{sis.c_id[k].replace('-', '')}={int(round(n_adic[k]))}"
              for k in range(sis.nc) if round(n_adic[k]) > 0]
    return ", ".join(partes) if partes else "(sin lineas nuevas)"


def tabla_flujos(sis: Sistema, resultado_dc: dict) -> str:
    """Tabla de texto con el flujo DC de verificacion."""
    filas = [f"{'Rama':>8} {'Tipo':>10} {'n':>3} {'Flujo MW':>10} {'Cap. MW':>9} {'Carga %':>8}"]
    for f in resultado_dc["flujos"]:
        filas.append(f"{f['etiqueta']:>8} {f['tipo']:>10} {f['n']:>3d} "
                     f"{f['flujo_MW']:>10.2f} {f['pmax'] * sis.sbase:>9.0f} {100 * f['carga']:>8.1f}")
    return "\n".join(filas)


# ==========================================================================
# 3. Camino minimo angular (big-M automatico)
# ==========================================================================
def big_m_corredores(sis: Sistema) -> tuple[np.ndarray, list[str]]:
    """Constante big-M (rad) de cada corredor.

    Modo 'fijo': M_k = bigM_rad (Villasana 1984 usa 1 rad).
    Modo 'auto': M_k = longitud del camino minimo entre los extremos del
    corredor en la red EXISTENTE, con peso x_l*Pmax_l por rama (maxima
    apertura angular que puede sostener cada circuito existente). Es una cota
    valida de |theta_i - theta_j| para cualquier plan, pues la red existente
    siempre esta presente (Binato et al., 2001). Si los extremos no estan
    conectados por la red existente se usa bigM_rad.
    """
    m_fijo = float(sis.p("bigM_rad", 1.0))
    modo = str(sis.p("bigM_modo", "fijo")).lower()
    M = np.full(sis.nc, m_fijo)
    origen = ["fijo"] * sis.nc
    if modo != "auto":
        return M, origen
    ady = [[] for _ in range(sis.nb)]
    for l in range(sis.nl):
        peso = sis.l_x[l] * sis.l_pmax[l]
        ady[sis.l_de[l]].append((sis.l_a[l], peso))
        ady[sis.l_a[l]].append((sis.l_de[l], peso))
    for k in range(sis.nc):
        distancia = _dijkstra(ady, int(sis.c_de[k]), int(sis.c_a[k]))
        if math.isfinite(distancia):
            M[k] = distancia
            origen[k] = "camino"
    return M, origen


def _dijkstra(ady, origen: int, destino: int) -> float:
    dist = {origen: 0.0}
    cola = [(0.0, origen)]
    while cola:
        d, u = heapq.heappop(cola)
        if u == destino:
            return d
        if d > dist.get(u, math.inf):
            continue
        for v, w in ady[u]:
            nd = d + w
            if nd < dist.get(v, math.inf):
                dist[v] = nd
                heapq.heappush(cola, (nd, v))
    return math.inf


# ==========================================================================
# 4. Utilidades de Gurobi
# ==========================================================================
def entorno_gurobi(ruta_log: str | Path | None = None, verbose: bool = False):
    """Entorno Gurobi silencioso que escribe la bitacora en `ruta_log`."""
    if gp is None:
        raise ImportError("Se requiere gurobipy (pip install gurobipy) y una licencia valida")
    env = gp.Env(empty=True)
    env.setParam("OutputFlag", 1 if (verbose or ruta_log) else 0)
    env.setParam("LogToConsole", 1 if verbose else 0)
    if ruta_log:
        Path(ruta_log).parent.mkdir(parents=True, exist_ok=True)
        env.setParam("LogFile", str(ruta_log))
    env.start()
    return env


def estadisticas(modelo) -> dict:
    """Tamano del modelo y desempeno del solver."""
    est = dict(variables=modelo.NumVars, enteras=modelo.NumIntVars,
               binarias=modelo.NumBinVars, restricciones=modelo.NumConstrs,
               restr_cuadraticas=modelo.NumQConstrs, no_ceros=modelo.NumNZs,
               tiempo_s=modelo.Runtime, estado=int(modelo.Status),
               iteraciones_simplex=float(modelo.IterCount))
    if modelo.IsMIP:
        est.update(nodos=float(modelo.NodeCount))
        if modelo.SolCount > 0:
            est.update(brecha=float(modelo.MIPGap), cota=float(modelo.ObjBound))
    return est


class RegistroConvergencia:
    """Callback que registra la evolucion del incumbente y de la cota inferior."""

    def __init__(self):
        self.puntos = []  # (tiempo, incumbente, cota, nodos)
        self._t0 = time.perf_counter()

    def __call__(self, modelo, donde):
        if donde == GRB.Callback.MIP:
            inc = modelo.cbGet(GRB.Callback.MIP_OBJBST)
            cota = modelo.cbGet(GRB.Callback.MIP_OBJBND)
            nodos = modelo.cbGet(GRB.Callback.MIP_NODCNT)
            t = modelo.cbGet(GRB.Callback.RUNTIME)
            if not self.puntos or (inc, cota) != self.puntos[-1][1:3]:
                self.puntos.append((t, inc if inc < GRB.INFINITY / 2 else None,
                                    cota if abs(cota) < GRB.INFINITY / 2 else None, nodos))


def nombre_estado(codigo: int) -> str:
    if GRB is None:
        return str(codigo)
    nombres = {GRB.OPTIMAL: "OPTIMO", GRB.INFEASIBLE: "INFACTIBLE",
               GRB.INF_OR_UNBD: "INFACTIBLE_O_NO_ACOTADO", GRB.UNBOUNDED: "NO_ACOTADO",
               GRB.TIME_LIMIT: "LIMITE_DE_TIEMPO", GRB.SUBOPTIMAL: "SUBOPTIMO"}
    return nombres.get(codigo, f"ESTADO_{codigo}")


# ==========================================================================
# 5. Entrada/salida
# ==========================================================================
def _a_json(obj):
    if isinstance(obj, dict):
        return {str(k): _a_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_a_json(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return [_a_json(v) for v in obj.tolist()]
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating, float)):
        valor = float(obj)
        return None if math.isnan(valor) or math.isinf(valor) else valor
    return obj


def exportar_modelo(modelo, ruta: str | Path) -> None:
    """Escribe el modelo en formato estandar (.lp / .mps) para otros solvers."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    modelo.write(str(ruta))


def guardar_json(datos: dict, ruta: str | Path) -> None:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(_a_json(datos), indent=2, ensure_ascii=False), encoding="utf-8")


def encabezado(titulo: str) -> str:
    linea = "=" * 78
    return f"{linea}\n{titulo}\n{linea}"
