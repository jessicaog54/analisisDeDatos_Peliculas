# ============================================================
# FASE 3 – ETL → Data Warehouse de Películas
# Versión adaptada para Google Colab
# ============================================================
# INSTRUCCIONES:
#   1. Ejecuta la Celda 0 para subir tu archivo CSV
#   2. Luego ejecuta las demás celdas en orden
# ============================================================

# ─── CELDA 0: Subir el archivo CSV ───────────────────────────
from google.colab import files
import io

print("Selecciona el archivo movies_metadata.csv desde tu computador:")
uploaded = files.upload()

# Obtener el nombre del archivo subido
nombre_archivo = list(uploaded.keys())[0]
print(f"\n✓ Archivo cargado: {nombre_archivo}")


# ─── CELDA 1: Imports y configuración ────────────────────────
import os
import ast
import sqlite3
import warnings
import pandas as pd
import numpy as np

warnings.filterwarnings("ignore")

# Rutas de salida (en el entorno de Colab)
OUTPUT_DB      = "/content/movies_datawarehouse.db"
OUTPUT_CSV_DIR = "/content/dw_tables"
os.makedirs(OUTPUT_CSV_DIR, exist_ok=True)

print("✓ Librerías cargadas")
print(f"✓ Carpeta de salida: {OUTPUT_CSV_DIR}")


# ─── CELDA 2: Helpers ────────────────────────────────────────
def safe_parse_list(value):
    if pd.isna(value) or str(value).strip() in ("", "[]", "nan"):
        return []
    try:
        parsed = ast.literal_eval(str(value))
        return parsed if isinstance(parsed, list) else []
    except Exception:
        return []

def safe_parse_dict(value):
    if pd.isna(value) or str(value).strip() in ("", "{}", "nan"):
        return {}
    try:
        parsed = ast.literal_eval(str(value))
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}

def to_float(value, default=np.nan):
    try:
        v = float(str(value).replace(",", ".").strip())
        return v if np.isfinite(v) else default
    except Exception:
        return default

def to_int(value, default=0):
    f = to_float(value, default=np.nan)
    return default if np.isnan(f) else int(f)

print("✓ Funciones auxiliares definidas")


# ─── CELDA 3: Extracción ─────────────────────────────────────
df_raw = pd.read_csv(
    io.BytesIO(uploaded[nombre_archivo]),
    sep=";",
    on_bad_lines="skip",
    low_memory=False
)

# Eliminar columnas basura sin nombre
df_raw = df_raw.drop(
    columns=[c for c in df_raw.columns if c.startswith("Unnamed")],
    errors="ignore"
)

print(f"✓ Filas extraídas : {len(df_raw):,}")
print(f"✓ Columnas        : {df_raw.columns.tolist()}")


# ─── CELDA 4: Limpieza base ───────────────────────────────────
df = df_raw.copy()

# Duplicados
antes = len(df)
df = df.drop_duplicates()
print(f"Duplicados eliminados: {antes - len(df):,}")

# ID numérico
df = df[pd.to_numeric(df["id"], errors="coerce").notna()].copy()
df["id"] = pd.to_numeric(df["id"], errors="coerce").astype(int)

# Eliminar sin id o title
df = df.dropna(subset=["id", "title"])

# Numéricas
df["budget"]       = df["budget"].apply(lambda x: to_float(x, 0))
df["revenue"]      = df["revenue"].apply(lambda x: to_float(x, 0))
df["runtime"]      = df["runtime"].apply(lambda x: to_float(x, np.nan))
df["popularity"]   = df["popularity"].apply(lambda x: to_float(x, np.nan))
df["vote_average"] = df["vote_average"].apply(lambda x: to_float(x, np.nan))
df["vote_count"]   = df["vote_count"].apply(lambda x: to_int(x, 0))

# Valores irreales → 0
df.loc[df["budget"]  < 1000, "budget"]  = 0.0
df.loc[df["revenue"] < 1000, "revenue"] = 0.0

# Fechas
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
df = df[df["release_date"].notna()].copy()

# Status
STATUS_VALIDOS = {"Released", "Rumored", "Post Production",
                  "In Production", "Planned", "Canceled"}
df["status"] = df["status"].where(df["status"].isin(STATUS_VALIDOS), other="Unknown")
df["status"] = df["status"].fillna("Unknown")

# Idioma
df["original_language"] = df["original_language"].fillna("unknown").str.lower().str.strip()

# Adult → booleano
df["adult"] = df["adult"].astype(str).str.lower().isin(["true", "1", "yes"])

print(f"✓ Dataset limpio: {len(df):,} filas")


# ─── CELDA 5: Métricas derivadas ─────────────────────────────
df["profit"] = df["revenue"] - df["budget"]
df["roi"]    = np.where(df["budget"] > 0, (df["profit"] / df["budget"]) * 100, np.nan)

df["tiene_presupuesto"]    = (df["budget"] > 0).astype(int)
df["tiene_recaudacion"]    = (df["revenue"] > 0).astype(int)
df["es_rentable"]          = ((df["profit"] > 0) & (df["budget"] > 0)).astype(int)
df["pertenece_a_coleccion"]= df["belongs_to_collection"].apply(
    lambda x: 0 if (pd.isna(x) or str(x).strip() in ("", "nan")) else 1
)
df["decada"] = (df["release_date"].dt.year // 10 * 10).astype("Int64")

def cat_budget(b):
    if b == 0:       return "Sin dato"
    elif b < 5e6:    return "Bajo (<5M)"
    elif b < 30e6:   return "Medio (5-30M)"
    elif b < 100e6:  return "Alto (30-100M)"
    else:             return "Blockbuster (>100M)"

df["categoria_presupuesto"] = df["budget"].apply(cat_budget)

print("✓ Métricas derivadas: profit, roi, es_rentable, categoria_presupuesto, decada")


# ─── CELDA 6: Dimensiones ────────────────────────────────────

## DIM_FECHA
df["fecha_id"] = df["release_date"].dt.strftime("%Y%m%d").astype(int)
dim_fecha = df[["fecha_id", "release_date"]].drop_duplicates("fecha_id").copy()
dim_fecha["anio"]       = dim_fecha["release_date"].dt.year
dim_fecha["mes"]        = dim_fecha["release_date"].dt.month
dim_fecha["dia"]        = dim_fecha["release_date"].dt.day
dim_fecha["trimestre"]  = dim_fecha["release_date"].dt.quarter
dim_fecha["dia_semana"] = dim_fecha["release_date"].dt.day_name()
dim_fecha["decada"]     = (dim_fecha["anio"] // 10 * 10)
dim_fecha["nombre_mes"] = dim_fecha["release_date"].dt.month_name()
dim_fecha = dim_fecha.drop(columns=["release_date"])
print(f"✓ DIM_FECHA        : {len(dim_fecha):,} registros")

## DIM_IDIOMA
idiomas_unicos = df["original_language"].unique()
dim_idioma = pd.DataFrame({"idioma_id": range(1, len(idiomas_unicos)+1), "codigo_iso": idiomas_unicos})
NOMBRES = {"en":"Inglés","fr":"Francés","es":"Español","de":"Alemán","it":"Italiano",
           "ja":"Japonés","ko":"Coreano","zh":"Chino","pt":"Portugués","ru":"Ruso",
           "hi":"Hindi","ar":"Árabe","sv":"Sueco","nl":"Neerlandés","pl":"Polaco",
           "tr":"Turco","da":"Danés","fi":"Finlandés","nb":"Noruego","unknown":"Desconocido"}
dim_idioma["nombre_idioma"] = dim_idioma["codigo_iso"].map(NOMBRES).fillna("Otro")
idioma_map = dict(zip(dim_idioma["codigo_iso"], dim_idioma["idioma_id"]))
df["idioma_id"] = df["original_language"].map(idioma_map)
print(f"✓ DIM_IDIOMA       : {len(dim_idioma):,} registros")

## DIM_ESTADO
estados = sorted(df["status"].unique())
dim_estado = pd.DataFrame({"estado_id": range(1, len(estados)+1), "nombre_estado": estados})
dim_estado["en_produccion"] = dim_estado["nombre_estado"].map(
    {"In Production": 1, "Post Production": 1}).fillna(0).astype(int)
estado_map = dict(zip(dim_estado["nombre_estado"], dim_estado["estado_id"]))
df["estado_id"] = df["status"].map(estado_map)
print(f"✓ DIM_ESTADO       : {len(dim_estado):,} registros")

## DIM_GENERO + BRIDGE
all_genres = []
for _, row in df.iterrows():
    for g in safe_parse_list(row["genres"]):
        if isinstance(g, dict) and "id" in g:
            all_genres.append({"genero_id": int(g["id"]), "nombre_genero": str(g["name"])})

dim_genero = pd.DataFrame(all_genres).drop_duplicates("genero_id").sort_values("genero_id").reset_index(drop=True)

bridge_rows = []
for _, row in df.iterrows():
    for g in safe_parse_list(row["genres"]):
        if isinstance(g, dict) and "id" in g:
            bridge_rows.append({"pelicula_id": row["id"], "genero_id": int(g["id"])})
bridge_pelicula_genero = pd.DataFrame(bridge_rows).drop_duplicates()
print(f"✓ DIM_GENERO       : {len(dim_genero):,} | BRIDGE: {len(bridge_pelicula_genero):,}")

## DIM_PAIS + BRIDGE
all_paises = []
for _, row in df.iterrows():
    for p in safe_parse_list(row["production_countries"]):
        if isinstance(p, dict) and "iso_3166_1" in p:
            all_paises.append({"pais_id": str(p["iso_3166_1"]), "nombre_pais": str(p.get("name",""))})

dim_pais = pd.DataFrame(all_paises).drop_duplicates("pais_id").sort_values("pais_id").reset_index(drop=True)

bridge_pais_rows = []
for _, row in df.iterrows():
    for p in safe_parse_list(row["production_countries"]):
        if isinstance(p, dict) and "iso_3166_1" in p:
            bridge_pais_rows.append({"pelicula_id": row["id"], "pais_id": str(p["iso_3166_1"])})
bridge_pelicula_pais = pd.DataFrame(bridge_pais_rows).drop_duplicates()
print(f"✓ DIM_PAIS         : {len(dim_pais):,} | BRIDGE: {len(bridge_pelicula_pais):,}")

## DIM_PRODUCTORA + BRIDGE
all_prod = []
for _, row in df.iterrows():
    for c in safe_parse_list(row["production_companies"]):
        if isinstance(c, dict) and "id" in c:
            all_prod.append({"productora_id": int(c["id"]), "nombre_productora": str(c.get("name",""))})

dim_productora = pd.DataFrame(all_prod).drop_duplicates("productora_id").sort_values("productora_id").reset_index(drop=True)

bridge_prod_rows = []
for _, row in df.iterrows():
    for c in safe_parse_list(row["production_companies"]):
        if isinstance(c, dict) and "id" in c:
            bridge_prod_rows.append({"pelicula_id": row["id"], "productora_id": int(c["id"])})
bridge_pelicula_productora = pd.DataFrame(bridge_prod_rows).drop_duplicates()
print(f"✓ DIM_PRODUCTORA   : {len(dim_productora):,} | BRIDGE: {len(bridge_pelicula_productora):,}")


# ─── CELDA 7: Tabla de Hechos ────────────────────────────────
fact_cols = [
    "id", "imdb_id", "title", "original_title",
    "fecha_id", "idioma_id", "estado_id",
    "budget", "revenue", "profit", "roi",
    "runtime", "popularity", "vote_average", "vote_count",
    "tiene_presupuesto", "tiene_recaudacion", "es_rentable",
    "pertenece_a_coleccion", "adult",
    "categoria_presupuesto", "decada",
    "overview", "tagline"
]

fact_peliculas = df[fact_cols].copy().rename(columns={"id": "pelicula_id"})
fact_peliculas = fact_peliculas.drop_duplicates("pelicula_id")

for col in ["roi", "popularity", "vote_average"]:
    fact_peliculas[col] = fact_peliculas[col].round(4)

print(f"✓ FACT_PELICULAS   : {len(fact_peliculas):,} registros")


# ─── CELDA 8: Carga en SQLite ────────────────────────────────
conn = sqlite3.connect(OUTPUT_DB)

TABLAS = {
    "dim_fecha":                  dim_fecha,
    "dim_idioma":                 dim_idioma,
    "dim_estado":                 dim_estado,
    "dim_genero":                 dim_genero,
    "dim_pais_produccion":        dim_pais,
    "dim_productora":             dim_productora,
    "fact_peliculas":             fact_peliculas,
    "bridge_pelicula_genero":     bridge_pelicula_genero,
    "bridge_pelicula_pais":       bridge_pelicula_pais,
    "bridge_pelicula_productora": bridge_pelicula_productora,
}

for nombre, tabla in TABLAS.items():
    tabla.to_sql(nombre, conn, if_exists="replace", index=False)
    print(f"  ✓ {nombre}: {len(tabla):,} registros")

conn.close()
print(f"\n✓ Base de datos guardada en: {OUTPUT_DB}")


# ─── CELDA 9: Exportar CSVs ──────────────────────────────────
for nombre, tabla in TABLAS.items():
    ruta = os.path.join(OUTPUT_CSV_DIR, f"{nombre}.csv")
    tabla.to_csv(ruta, index=False, encoding="utf-8-sig")
    print(f"  ✓ {ruta}")


# ─── CELDA 10: Descargar archivos desde Colab ────────────────
from google.colab import files

# Descarga la base de datos SQLite
files.download(OUTPUT_DB)

# Descarga cada CSV individualmente
for nombre in TABLAS.keys():
    files.download(os.path.join(OUTPUT_CSV_DIR, f"{nombre}.csv"))

print("\n✓ ¡Todos los archivos descargados!")


# ─── CELDA 11: Resumen final ─────────────────────────────────
total        = len(fact_peliculas)
con_budget   = fact_peliculas["tiene_presupuesto"].sum()
con_revenue  = fact_peliculas["tiene_recaudacion"].sum()
rentables    = fact_peliculas["es_rentable"].sum()
en_coleccion = fact_peliculas["pertenece_a_coleccion"].sum()

print(f"""
╔══════════════════════════════════════════════════╗
║       RESUMEN DEL DATA WAREHOUSE — PELÍCULAS     ║
╠══════════════════════════════════════════════════╣
║  Películas cargadas     : {total:>8,}             ║
║  Géneros únicos         : {len(dim_genero):>8,}             ║
║  Países de producción   : {len(dim_pais):>8,}             ║
║  Productoras únicas     : {len(dim_productora):>8,}             ║
║  Idiomas                : {len(dim_idioma):>8,}             ║
╠══════════════════════════════════════════════════╣
║  Con presupuesto        : {con_budget:>8,} ({con_budget/total*100:.1f}%)  ║
║  Con recaudación        : {con_revenue:>8,} ({con_revenue/total*100:.1f}%)  ║
║  Películas rentables    : {rentables:>8,} ({rentables/total*100:.1f}%)   ║
║  En colección/saga      : {en_coleccion:>8,} ({en_coleccion/total*100:.1f}%)   ║
╚══════════════════════════════════════════════════╝
""")
