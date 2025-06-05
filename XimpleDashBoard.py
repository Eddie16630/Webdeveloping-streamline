import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20
from bokeh.transform import factor_cmap

# Configuración de página
st.set_page_config(layout="wide")
st.title("Dashboard de Préstamos - Ximple")

# Carga de datos
@st.cache_data
def load_data():
    df = pd.read_csv("df_merged.csv")
    # Eliminar columna no deseada si existe
    if "efectividad de conversion telefonica" in df.columns:
        df.drop(columns=["efectividad de conversion telefonica"], inplace=True)
    return df

df = load_data()

# Filtros en la barra lateral
st.sidebar.header("Filtros")

# Filtro por Año
if "IssueYear" in df.columns:
    years = sorted(df["IssueYear"].dropna().unique())
    selected_years = st.sidebar.multiselect("Año(s):", years, default=years)
    df = df[df["IssueYear"].isin(selected_years)]

# Filtro por Región
if "customer_region" in df.columns:
    regiones = sorted(df["customer_region"].dropna().unique())
    selected_regions = st.sidebar.multiselect("Región(es):", regiones, default=regiones)
    df = df[df["customer_region"].isin(selected_regions)]

# Filtro por Canal
if "canal_ajustado" in df.columns:
    canales = sorted(df["canal_ajustado"].dropna().unique())
    selected_channels = st.sidebar.multiselect("Canal(es):", canales, default=canales)
    df = df[df["canal_ajustado"].isin(selected_channels)]

# Filtro por Clúster
if "cluster" in df.columns:
    cluster_types = df["cluster"].dropna().unique()
    selected_clusters = st.sidebar.multiselect("Tipo de Cluster:", cluster_types, default=cluster_types)
    df = df[df["cluster"].isin(selected_clusters)]

# Vista previa
st.subheader("Vista Previa de los Datos Filtrados")
st.dataframe(df.head())

# Función auxiliar para colores
def get_palette(n):
    return Category20[20][:n] if n <= 20 else Category20[20] + ["#ccc"] * (n - 20)

# Visualización 1: Préstamos por Canal
st.markdown("---")
st.subheader("Participación de Préstamos por Canal")
if "canal_ajustado" in df.columns:
    canal_counts = df["canal_ajustado"].value_counts().sort_values(ascending=False)
    source = ColumnDataSource(data=dict(canal=canal_counts.index.tolist(), counts=canal_counts.values))
    p1 = figure(x_range=canal_counts.index.tolist(), height=350, title="Número de Préstamos por Canal", toolbar_location=None, tools="")
    p1.vbar(x='canal', top='counts', width=0.8, source=source, legend_field="canal",
            fill_color=factor_cmap('canal', palette=get_palette(len(canal_counts)), factors=canal_counts.index.tolist()))
    p1.xaxis.major_label_orientation = 1
    st.bokeh_chart(p1, use_container_width=True)

# Visualización 2: Préstamos por Región (Pie)
st.markdown("---")
st.subheader("Participación de Préstamos por Región")
if "customer_region" in df.columns:
    region_counts = df["customer_region"].value_counts()
    source = ColumnDataSource(data=dict(
        region=region_counts.index.tolist(),
        value=region_counts.values,
        angle=[v/sum(region_counts.values)*2*3.14 for v in region_counts.values],
        color=get_palette(len(region_counts))
    ))

    from bokeh.plotting import figure
    from bokeh.transform import cumsum
    p2 = figure(height=400, title="Préstamos por Región", toolbar_location=None, tools="", x_range=(-0.5, 1.0))
    p2.wedge(x=0, y=1, radius=0.4,
             start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
             line_color="white", fill_color='color', legend_field='region', source=source)
    p2.axis.visible = False
    p2.grid.visible = False
    st.bokeh_chart(p2, use_container_width=True)

# Visualización 3: Distribución por Región (Barra horizontal)
st.markdown("---")
st.subheader("Distribución de Préstamos por Región")
region_sorted = region_counts.sort_values()
source = ColumnDataSource(data=dict(region=region_sorted.index.tolist(), counts=region_sorted.values))
p3 = figure(y_range=region_sorted.index.tolist(), height=350, title="Distribución por Región", toolbar_location=None)
p3.hbar(y='region', right='counts', height=0.5, source=source, color="skyblue")
st.bokeh_chart(p3, use_container_width=True)

# Visualización 4: Monto promedio por cliente y tipo de préstamo
st.markdown("---")
st.subheader("Monto Promedio por Cliente y Tipo de Préstamo")
if all(col in df.columns for col in ['LoanAmount', 'RecipientType', 'LoanType']):
    avg_df = df.groupby(['RecipientType', 'LoanType'])['LoanAmount'].mean().reset_index()
    recipient_types = avg_df['RecipientType'].unique().tolist()
    loan_types = avg_df['LoanType'].unique().tolist()
    colors = get_palette(len(loan_types))

    p4 = figure(x_range=recipient_types, height=400, title="Monto Promedio por Cliente y Tipo de Préstamo", toolbar_location=None)
    for i, loan_type in enumerate(loan_types):
        subset = avg_df[avg_df['LoanType'] == loan_type]
        p4.vbar(x=subset['RecipientType'], top=subset['LoanAmount'], width=0.7/(len(loan_types)), 
                legend_label=loan_type, line_color="white", fill_color=colors[i], muted_alpha=0.2,
                left=[i*0.15 for _ in subset['RecipientType']])
    p4.legend.title = "Tipo de Préstamo"
    st.bokeh_chart(p4, use_container_width=True)

else:
    st.info("No se encontraron columnas necesarias para esta visualización.")

