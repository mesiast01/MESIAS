import streamlit as st
import pandas as pd

st.set_page_config(page_title="Traductor Awajún/Wampis", layout="centered")

st.title("📘 Traductor INKAJU: Awajún / Wampis – Español")

# Cargar el archivo CSV y limpiar
@st.cache_data
def cargar_diccionario():
    df = pd.read_csv("diccionario.csv", encoding="utf-8")
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.dropna(subset=["espanol"])  # Asegura que la columna 'espanol' no esté vacía
    df = df.drop_duplicates(subset=["espanol", "awajun", "wampis"], keep="last")
    return df

df = cargar_diccionario()

# Selección de idioma
idioma = st.selectbox("Selecciona el idioma de destino:", ["Awajún", "Wampis"])
modo = st.radio("Modo de traducción:", ["Español → Lengua originaria", "Lengua originaria → Español"])

texto = st.text_input("🔤 Ingresa una palabra:")

# Determinar columnas según idioma y modo
if idioma == "Awajún":
    origen, destino = ("espanol", "awajun") if modo == "Español → Lengua originaria" else ("awajun", "espanol")
else:
    origen, destino = ("espanol", "wampis") if modo == "Español → Lengua originaria" else ("wampis", "espanol")

# Buscar traducción
if texto:
    coincidencias = df[df[origen].str.lower() == texto.lower()]
    # Filtrar si el resultado está vacío o es NaN
    coincidencias = coincidencias[coincidencias[destino].notnull()]
    
    if not coincidencias.empty:
        resultado = coincidencias.iloc[0][destino]
        st.success(f'**{texto}** → **{resultado}**')
    else:
        st.error("❌ Palabra no encontrada en el diccionario o traducción incompleta.")