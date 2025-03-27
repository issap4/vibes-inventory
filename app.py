import streamlit as st
import pandas as pd

# Cargar datos de Excel
@st.cache_data
def load_data():
    df = pd.read_excel("Lab_Material.xlsx", engine="openpyxl")
    return df

df = load_data()

# Título de la app
st.title("🔬404 Material - VIBES🛰️")

# Barra de búsqueda
search_term = st.text_input("🔍Search material or keyword:", "")

# Filtros opcionales
location_filter = st.selectbox("📍 Filter by Location:", ["All"] + sorted(df["Location"].dropna().unique().tolist()))
shelf_filter = st.selectbox("🗄️ Filter by Shelf:", ["All"] + sorted(df["Shelf"].dropna().unique().tolist()))

# Filtrar datos según búsqueda y filtros
filtered_df = df[
    df.apply(lambda row: search_term.lower() in str(row.to_list()).lower(), axis=1)
]

if location_filter != "All":
    filtered_df = filtered_df[filtered_df["Location"] == location_filter]

if shelf_filter != "All":
    filtered_df = filtered_df[filtered_df["Shelf"] == shelf_filter]

# Mostrar resultados
st.write(f"📋 Material {len(filtered_df)} was found:")

if not filtered_df.empty:
    st.dataframe(filtered_df)  # Mostrar tabla interactiva
else:
    st.warning("⚠️ No Material was found.")

# Descargar resultados
if not filtered_df.empty:
    st.download_button(
        "📥 Save search results in a CSV file",
        filtered_df.to_csv(index=False).encode("utf-8"),
        "materiales_filtrados.csv",
        "text/csv"
    )
