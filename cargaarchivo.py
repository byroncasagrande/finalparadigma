import streamlit as st
import pandas as pd
#from io import StringIO
"""
Carga un archivo Excel y devuelve un DataFrame de pandas.
"""
def cargaFile():
    try:
        uploaded_file = st.file_uploader("Escoge un archivo Excel.", type=["xlsx","xls","csv"])
        if uploaded_file is not None:
            if uploaded_file.name.endswith("csv"):
                # To read file as csv:
                df=pd.read_csv(uploaded_file)
            else:
                # To read file as csv:
                df=pd.read_excel(uploaded_file)
            return(df)
            
        else:
            st.write("Por favor cargue un archivo soportado.")
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None