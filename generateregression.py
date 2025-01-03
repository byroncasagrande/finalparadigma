import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score

def realizar_regresion(df, variable_objetivo, variables_predictoras, tipo_regresion):
    """
    Realiza un modelo de regresión y muestra los resultados. Retorna MSE y R^2 o None si hay error.
    """
    try:
        if not variables_predictoras:
            st.warning("Selecciona al menos una variable predictora.")
            return None, None  # Retorna None, None si no hay predictoras

        if not pd.api.types.is_numeric_dtype(df[variable_objetivo]):
            st.error("La variable objetivo debe ser numérica.")
            return None, None

        for predictor in variables_predictoras:
            if not pd.api.types.is_numeric_dtype(df[predictor]):
                st.error(f"La variable predictora '{predictor}' debe ser numérica.")
                return None, None

        X = df[variables_predictoras]
        y = df[variable_objetivo]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        if tipo_regresion == "Lineal":
            modelo = LinearRegression()
        elif tipo_regresion == "Ridge":
            modelo = Ridge()
        elif tipo_regresion == "Lasso":
            modelo = Lasso()
        elif tipo_regresion == "Polinomial":
          poly = PolynomialFeatures(degree=2)
          X_train = poly.fit_transform(X_train)
          X_test = poly.transform(X_test)
          modelo = LinearRegression()
        else:
            st.error("Tipo de regresión no válido.")
            return None, None

        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        st.write(f"MSE: {mse}")
        st.write(f"R^2: {r2}")

        # Visualización
        fig, ax = plt.subplots()
        ax.scatter(y_test, y_pred)
        ax.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=3)
        ax.set_xlabel('Valores Reales')
        ax.set_ylabel('Predicciones')
        ax.set_title('Valores Reales vs. Predicciones')
        st.pyplot(fig)
        

        return mse, r2  # Retorna los valores calculados
    except Exception as e:
        st.error(f"Error durante la regresión: {e}")
        return None, None