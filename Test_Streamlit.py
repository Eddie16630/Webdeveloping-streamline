import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Título del dashboard
st.title("Panel de Datos de Vendedores")

# Subida de archivo CSV
uploaded_file = st.file_uploader("Sube un archivo CSV con los datos de los vendedores", type="csv")

if uploaded_file is not None:
    # Carga del DataFrame
    df = pd.read_csv(uploaded_file)

    # Vista previa de los datos
    st.subheader("Vista Previa de los Datos")
    st.dataframe(df.head())

    # Asegurarse de que las columnas numéricas estén en el tipo correcto
    df['UNIDADES VENDIDAS'] = pd.to_numeric(df['UNIDADES VENDIDAS'], errors='coerce')
    df['VENTAS TOTALES'] = pd.to_numeric(df['VENTAS TOTALES'], errors='coerce')

    # Filtrado por Región
    st.subheader("Filtrar por Región")
    regiones = df['REGION'].unique()
    region_seleccionada = st.selectbox("Selecciona una región:", regiones)
    df_region = df[df['REGION'] == region_seleccionada]
    st.dataframe(df_region)

    # Gráficos con Matplotlib
    st.subheader("Gráficos de Ventas y Unidades")

    # Crear dos columnas para mostrar las gráficas
    col1, col2 = st.columns(2)

    # Gráfico de Unidades Vendidas
    with col1:
        fig1, ax1 = plt.subplots()
        ax1.bar(df_region['NOMBRE'], df_region['UNIDADES VENDIDAS'], color='skyblue')
        ax1.set_xlabel("Nombre")
        ax1.set_ylabel("Unidades Vendidas")
        ax1.set_title("Unidades Vendidas por Vendedor")
        plt.xticks(rotation=90)
        st.pyplot(fig1)

    # Gráfico de Ventas Totales
    with col2:
        fig2, ax2 = plt.subplots()
        ax2.bar(df_region['NOMBRE'], df_region['VENTAS TOTALES'], color='orange')
        ax2.set_xlabel("Nombre")
        ax2.set_ylabel("Ventas Totales")
        ax2.set_title("Ventas Totales por Vendedor")
        plt.xticks(rotation=90)
        st.pyplot(fig2)

    # Mostrar promedio de ventas totales
    promedio = df_region['VENTAS TOTALES'].mean()
    st.markdown("### Promedio de Ventas Totales")
    st.write(f"${promedio:,.2f}")

    # Buscar vendedor por nombre
    st.subheader("Buscar Vendedor")
    nombres = df['NOMBRE'].unique()
    nombre_seleccionado = st.selectbox("Selecciona un nombre:", nombres)
    vendedor_df = df[df['NOMBRE'] == nombre_seleccionado]
    st.write("Información del vendedor:")
    st.dataframe(vendedor_df)

    # Mostrar gráfico del vendedor
    if st.button("Mostrar gráfico del vendedor"):
        fig3, ax3 = plt.subplots()
        bar_labels = ['Unidades Vendidas', 'Ventas Totales']
        bar_values = [
            vendedor_df['UNIDADES VENDIDAS'].values[0],
            vendedor_df['VENTAS TOTALES'].values[0]
        ]
        ax3.bar(bar_labels, bar_values, color=["#E65151", "#5B941A"])
        ax3.set_title(f"Desempeño de {nombre_seleccionado}")
        st.pyplot(fig3)

else:
    st.info("Por favor, sube un archivo CSV para comenzar.")

