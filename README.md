# Proyecto 3 — Expansión de transmisión (TNEP) con LP, MINLP y MILP big-M en Gurobi

Jaime Rueda Perez – Fabio Silva Galvis – Andrés Méndez Martínez
Planeamiento de Sistemas de Potencia — Universidad de los Andes, Bogotá, Colombia.

## Contenido de la entrega

```
Informe_Proyecto3_TNEP.pdf   Informe técnico (formato IEEE)
codigo/
  datos/                     Bases de datos Excel (Garver 4 y 15 corredores, Sur de Brasil 46 barras)
                             y construir_bases_de_datos.py, que las genera
  tnep_comun.py              Lectura de la base de datos, flujo DC de verificación, big-M, utilidades Gurobi
  tnep_lp.py                 Método 1: LP iterativo de Villasana–Garver
  tnep_minlp.py              Método 2: MINLP bilineal (óptimo global, NonConvex=2)
  tnep_milp_bigm.py          Método 3: M(0-1)LP con big-M (fijo o automático por camino mínimo)
  fuerza_bruta.py            Enumeración exhaustiva con flujo DC (validación)
  validacion_ac.py           Flujo de carga AC Newton–Raphson (prueba de Garver 1970)
  validacion_highs.py        Validación cruzada con un segundo solver (HiGHS)
  ejecutar_todo.py           Reproduce todos los experimentos del informe
  graficas.py, tablas_latex.py  Figuras y tablas del informe
  requirements.txt           Dependencias de Python
  resultados/                Resultados (.json, .csv), bitácoras de Gurobi y modelos (.lp, .mps)
```

## Ejecutar los códigos

Requisitos: Python ≥ 3.10 y `pip install -r codigo/requirements.txt`.
gurobipy requiere licencia (la académica gratuita sirve; la licencia restringida que
trae pip alcanza para los casos base de los tres sistemas).

```bash
cd codigo
python tnep_lp.py        --datos datos/garver6_tnep.xlsx
python tnep_minlp.py     --datos datos/garver6_tnep.xlsx
python tnep_milp_bigm.py --datos datos/garver6_tnep.xlsx            # M = 1 rad (Villasana)
python tnep_milp_bigm.py --datos datos/garver6_tnep.xlsx --bigM 0.5 # sensibilidad a M
python tnep_milp_bigm.py --datos datos/sur46_sin_redespacho.xlsx    # escalabilidad
python fuerza_bruta.py   --datos datos/garver6_tnep.xlsx --orden 6-4,6-2,6-5,3-5
python validacion_ac.py  --plan 6-2=4,6-4=2,3-5=1

python ejecutar_todo.py && python graficas.py && python tablas_latex.py   # todo el informe (~5 min)
```

## Usar otro sistema

Copie cualquiera de los libros de `codigo/datos/` y llene sus hojas:

| Hoja | Columnas |
|------|----------|
| `Parametros` | `Parametro`, `Valor` (Sbase_MVA, barra_referencia, unidad_costo, bigM_rad, bigM_modo, theta_max_rad, criterio_lp, tolerancia, mip_gap, limite_tiempo_s) |
| `Barras` | `Barra`, `Tipo`, `PG_MW`, `PL_MW` (con ΣPG = ΣPL) |
| `Lineas` | `Desde`, `Hasta`, `Circuitos`, `x_pu`, `r_pu`, `Pmax_MW` (por circuito), `Longitud` |
| `Corredores` | `Corredor`, `Desde`, `Hasta`, `x_pu`, `r_pu`, `Pmax_MW`, `Costo` (por línea), `n_max`, `Longitud` |

Los tres métodos leen exactamente la misma base de datos y construyen los modelos
recorriendo ramas y corredores (estructuras dispersas), por lo que no requieren cambios
para sistemas de mayor tamaño.

## Resultados principales

| Sistema | LP iterativo | MINLP | MILP big-M |
|---|---|---|---|
| Garver, 4 corredores | 1000 pu | 1000 pu (óptimo global) | 1000 pu |
| Garver, 15 corredores | 1000 pu | 1000 pu | 1000 pu |
| Sur de Brasil, 46 barras | 166.041 MUS$ (+7.5 %) | 154.420 MUS$ | 154.420 MUS$ (óptimo publicado) |

Plan óptimo de Garver: n62 = 4, n64 = 2, n35 = 1 (confirmado por fuerza bruta: combinación
2401, fila 226 de TNEP.pdf). Con big-M fijo menor que M* = 0.5787 rad el MILP entrega planes
subóptimos (1100–1155 pu) sin ninguna advertencia. HiGHS reproduce los óptimos del MILP y de
todos los LP. Óptimo de 46 barras: Romero y Monticelli (1994), optimalidad probada por Binato
et al. (2001); datos verificados contra Taglialenha (2008), con corrección del costo 23-24 (5.308).
