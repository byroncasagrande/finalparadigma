import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import io

def generateStatistics(df):
    """
    Realiza un análisis exploratorio de datos básico
    """
    st.subheader("Análisis Exploratorio de Datos")

    st.write("Primeras filas:")
    st.dataframe(df.head())

    st.write("Información del DataFrame:")
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

    st.write("Estadísticas Descriptivas:")
    st.write(df.describe())

    st.subheader("Visualizaciones")

    for col in df.select_dtypes(include=['number']):
        fig, ax = plt.subplots()
        sns.histplot(df[col], ax=ax, kde=True)
        st.pyplot(fig)

    num_cols = df.select_dtypes(include=['number']).columns
    if len(num_cols) >= 2:
      fig, ax = plt.subplots()
      sns.scatterplot(x=num_cols[0], y=num_cols[1], data=df, ax=ax)
      st.pyplot(fig)