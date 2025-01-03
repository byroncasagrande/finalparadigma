import streamlit as st
import numpy as np
import plotly.express as px
import cargaarchivo as ca
import generatestatistics as ge
from generateregression import realizar_regresion 
from generatereport import generar_reporte

# Inicializar resultados_regresion en la sesión de Streamlit
# Utilizado para no perder los datos calculados enla regresion
if 'resultados_regresion' not in st.session_state:
    st.session_state.resultados_regresion = []

#--------TITULOS Y LOGOS
st.sidebar.image("data/images.jpg", width=50)
st.title("Herramienta de Análisis de Datos Interactiva en Streamlit")
st.sidebar.title("Modulos")

#--------MODULOS
modulo = st.sidebar.selectbox("--Seleccione un modulo--",["Herramienta de Análisis de Datos"],index=None)
# Ejecucion principal
if modulo == "Herramienta de Análisis de Datos":
    st.write("Powered by UCG (Alumno BC)")
    df = ca.cargaFile()
    #Si se realiza la carga del archivo se continua
    if df is not None:
       #Genero las estadisticas y analis EDA
       ge.generateStatistics(df)
       #Procedo a las regresiones
       st.subheader("Modelado de Regresión")
       variables_numericas = df.select_dtypes(include=['number']).columns.tolist()
       if len(variables_numericas) < 2:
           st.warning("Se necesitan al menos dos columnas numéricas para realizar una regresión.")
       else:
            variable_objetivo = st.selectbox("Variable Objetivo (Y):", variables_numericas)
            variables_predictoras = st.multiselect("Variables Predictoras (X):", variables_numericas, default=[col for col in variables_numericas if col != variable_objetivo])

            if not variables_predictoras:
                st.warning("Selecciona al menos una variable predictora.")
            else:
                tipo_regresion = st.selectbox("Tipo de Regresión:", ["Lineal", "Ridge", "Lasso", "Polinomial"])

                # Usar st.form para agrupar los elementos del formulario de regresión
                with st.form(key='regression_form'):
                    if st.form_submit_button("Ejecutar Regresión"):
                        resultado_regresion = realizar_regresion(df, variable_objetivo, variables_predictoras, tipo_regresion)
                        if resultado_regresion:
                            mse, r2 = resultado_regresion
                            st.session_state.resultados_regresion.append(f"Regresión {tipo_regresion}: MSE = {mse:.2f}, R^2 = {r2:.2f}")
                        else:
                            st.error("No se pudo realizar la regresión. Revisa las variables seleccionadas.")
        #Finalmente genero un Excel con un analisis estadistico y resultados de la regresion
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