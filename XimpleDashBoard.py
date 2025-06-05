import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de página
st.set_page_config(layout="wide")
st.title("📊 Dashboard de Préstamos - Ximple")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("df_merged.csv")
    if "efectividad de conversion telefonica" in df.columns:
        df = df.drop(columns=["efectividad de conversion telefonica"])
    return df

df = load_data()

# === SIDEBAR ===
st.sidebar.header("🔍 Filtros")

# Filtro: Año
if "IssueYear" in df.columns:
    years = sorted(df["IssueYear"].dropna().unique())
    selected_years = st.sidebar.multiselect("Año(s):", years, default=years)
    df = df[df["IssueYear"].isin(selected_years)]

# Filtro: Canal
if "canal_ajustado" in df.columns:
    canales = sorted(df["canal_ajustado"].dropna().unique())
    selected_channels = st.sidebar.multiselect("Canal(es):", canales, default=canales)
    df = df[df["canal_ajustado"].isin(selected_channels)]

# Filtro: Clúster
if "cluster" in df.columns:
    clusters = sorted(df["cluster"].dropna().unique())
    selected_clusters = st.sidebar.multiselect("Tipo de Clúster:", clusters, default=clusters)
    df = df[df["cluster"].isin(selected_clusters)]

# Vista previa
st.subheader("👁 Vista Previa de los Datos Filtrados")
st.dataframe(df.head())

# === VISUALIZACIONES ===
gold = "#DAA520"

# Gráfica 1: Préstamos por Canal
st.markdown("### 📈 Participación de Préstamos por Canal")
if "canal_ajustado" in df.columns:
    counts = df["canal_ajustado"].value_counts()
    fig, ax = plt.subplots()
    counts.plot(kind='bar', color=gold, ax=ax)
    ax.set_title("Número de Préstamos por Canal")
    ax.set_xlabel("Canal")
    ax.set_ylabel("Cantidad")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# Gráfica 2: Distribución por Región (Pie)
st.markdown("### 🗺️ Distribución de Préstamos por Región")
if "customer_region" in df.columns:
    region_counts = df["customer_region"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(region_counts, labels=region_counts.index, autopct='%1.1f%%', startangle=90, colors=[gold]*len(region_counts))
    ax.set_title("Participación de Préstamos por Región")
    ax.axis('equal')
    st.pyplot(fig)

# Gráfica 3: Distribución por Región (Barra horizontal)
st.markdown("### 📊 Distribución de Préstamos por Región")
fig, ax = plt.subplots()
region_counts.sort_values().plot(kind='barh', color=gold, ax=ax)
ax.set_title("Distribución por Región")
ax.set_xlabel("Cantidad")
ax.set_ylabel("Región")
st.pyplot(fig)

# Gráfica 4: Monto promedio por tipo de cliente y tipo de préstamo
st.markdown("### 💰 Monto Promedio por Cliente y Tipo de Préstamo")
if all(col in df.columns for col in ['LoanAmount', 'RecipientType', 'LoanType']):
    avg = df.groupby(['RecipientType', 'LoanType'])['LoanAmount'].mean().unstack()
    fig, ax = plt.subplots(figsize=(10, 5))
    avg.plot(kind='bar', ax=ax, color=gold)
    ax.set_title("Monto Promedio por Cliente y Tipo de Préstamo")
    ax.set_ylabel("Monto Promedio ($)")
    ax.set_xlabel("Tipo de Cliente")
    ax.legend(title="Tipo de Préstamo")
    st.pyplot(fig)
else:
    st.info("No se encontraron las columnas necesarias para esta visualización.")
