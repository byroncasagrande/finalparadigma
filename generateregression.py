import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

def realizar_regresion(df, variable_objetivo, variable_predictora):
    """
    Realiza regresión lineal y Random Forest, agrega las predicciones al DataFrame y genera un gráfico.
    """
    try:
        # Asegurar que las columnas sean numéricas
        for col in [variable_objetivo, variable_predictora]:
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise ValueError(f"La columna '{col}' no es numérica.")

        # Crear un DataFrame con las variables seleccionadas y eliminar filas con NaN
        df_regresion = df[[variable_objetivo, variable_predictora]].dropna()

        # Separar las variables predictora (X) y objetivo (y)
        X = df_regresion[[variable_predictora]]
        y = df_regresion[variable_objetivo]

        # Dividir los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Modelo Lineal
        modelo_lineal = LinearRegression()
        modelo_lineal.fit(X_train, y_train)
        y_pred_lineal = modelo_lineal.predict(X_test)

        # Modelo Random Forest (con menos estimadores para mejorar el rendimiento)
        modelo_rf = RandomForestRegressor(random_state=42, n_estimators=100, max_depth=10, n_jobs=-1)
        modelo_rf.fit(X_train, y_train)
        y_pred_rf = modelo_rf.predict(X_test)

        # Métricas para Regresión Lineal
        mse_lineal = mean_squared_error(y_test, y_pred_lineal)
        r2_lineal = r2_score(y_test, y_pred_lineal)

        # Métricas para Random Forest
        mse_rf = mean_squared_error(y_test, y_pred_rf)
        r2_rf = r2_score(y_test, y_pred_rf)

        # Crear un DataFrame para el conjunto de prueba con las predicciones
        df_test = X_test.copy()
        df_test[variable_objetivo] = y_test
        df_test['Regresión Lineal'] = y_pred_lineal
        df_test['Regresión Random Forest'] = y_pred_rf

        # Para mejorar el rendimiento, reducimos la cantidad de puntos en el gráfico
        # Tomamos una muestra del conjunto de prueba
        df_test_sample = df_test.sample(n=500, random_state=42)  # Muestra aleatoria de 500 puntos

        st.write("Conjunto de datos aleatorio con los valores de regresion")
        st.write(df_test_sample)
        # Gráfico interactivo con Plotly
        fig = px.scatter(
            df_test_sample,
            x=variable_predictora,
            y=variable_objetivo,
            title="Regresión Lineal y Random Forest",
            labels={variable_predictora: df_test_sample.columns[0], variable_objetivo: df_test_sample.columns[1]},
            template="plotly_white"
        )

        # Agregar línea de Regresión Lineal
        fig.add_scatter(
            x=df_test_sample[variable_predictora],
            y=df_test_sample['Regresión Lineal'],
            mode='lines',
            name='Regresión Lineal'
        )

        # Agregar línea de Regresión Random Forest
        fig.add_scatter(
            x=df_test_sample[variable_predictora],
            y=df_test_sample['Regresión Random Forest'],
            mode='lines',
            name='Regresión Random Forest'
        )

        # Actualizar layout para evitar solapamientos y activar la leyenda
        fig.update_layout(showlegend=True)

        # Devolver las métricas y el gráfico
        return {
            'lineal': {'mse': mse_lineal, 'r2': r2_lineal},
            'random_forest': {'mse': mse_rf, 'r2': r2_rf},
            'fig': fig
        }, df_test

    except ValueError as e:
        st.error(f"Error: {e}")
        return None, None
    except KeyError as e:
        st.error(f"Error: La columna {e} no existe en el DataFrame.")
        return None, None
