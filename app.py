import streamlit as st
import pandas as pd
import cargaarchivo as ca
import generatestatistics as ge
from generateregression import realizar_regresion
from generatereport import generar_reporte

# Inicializar resultados_regresion en la sesión de Streamlit
if 'resultados_regresion' not in st.session_state:
    st.session_state.resultados_regresion = []

# --------TITULOS Y LOGOS
st.sidebar.image("data/images.jpg", width=50)
st.title("Herramienta de Análisis de Datos Interactiva en Streamlit")
st.sidebar.title("Módulos")

# --------MÓDULOS
modulo = st.sidebar.selectbox("--Seleccione un módulo--", ["Herramienta de Análisis de Datos"],index=None)

# Ejecución principal
if modulo == "Herramienta de Análisis de Datos":
    st.write("Powered by UCG (Alumno BC)")
    df = ca.cargaFile()

    # Si se realiza la carga del archivo se continúa
    if df is not None:
        ge.generateStatistics(df)
        st.subheader("Modelado de Regresión")

        # Filtrar columnas numéricas
        variables_numericas = df.select_dtypes(include=['number']).columns.tolist()

        if len(variables_numericas) < 2:
            st.warning("Se necesitan al menos dos columnas numéricas para realizar una regresión.")
        else:
            variable_objetivo = st.selectbox("Variable Objetivo (Y):", variables_numericas)
            variables_predictoras = st.selectbox(
                "Variable Predictora (X):",
                [col for col in variables_numericas if col != variable_objetivo]
            )

            if st.button("Ejecutar Regresión"):
                with st.spinner("Ejecutando regresiones..."):
                    try:
                        resultado_regresion, df_resultados = realizar_regresion(df.copy(), variable_objetivo, variables_predictoras)
                        if resultado_regresion:
                            # Mostrar métricas
                            st.markdown("### Resultados de la Regresión")
                            st.write(f"**Regresión Lineal:** MSE = {resultado_regresion['lineal']['mse']:.2f}, R² = {resultado_regresion['lineal']['r2']:.2f}")
                            st.write(f"**Random Forest:** MSE = {resultado_regresion['random_forest']['mse']:.2f}, R² = {resultado_regresion['random_forest']['r2']:.2f}")

                            # Mostrar gráfico
                            st.markdown("### Gráfico de Regresión")
                            st.plotly_chart(resultado_regresion['fig'])

                            # Agregar resultados a la sesión para el reporte
                            st.session_state.resultados_regresion.append(
                                f"Regresión Lineal: MSE = {resultado_regresion['lineal']['mse']:.2f}, R² = {resultado_regresion['lineal']['r2']:.2f}\n"
                                f"Random Forest: MSE = {resultado_regresion['random_forest']['mse']:.2f}, R² = {resultado_regresion['random_forest']['r2']:.2f}"
                            )
                        else:
                            st.error("No se pudo realizar la regresión. Revisa las variables seleccionadas y los tipos de datos.")
                    except Exception as e:
                        st.error(f"Ocurrió un error inesperado: {e}")


        if st.button("Generar Reporte"):
            buffer = generar_reporte(df, st.session_state.resultados_regresion)
            if buffer:
                st.download_button(
                    label="Descargar Reporte",
                    data=buffer,
                    file_name="reporte_analisis.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("Error al generar el reporte.")
