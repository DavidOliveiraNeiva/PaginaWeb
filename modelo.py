import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def prever_gasto(df):
    df['data'] = pd.to_datetime(df['data'])
    df['mes'] = df['data'].dt.month + 12 * df['data'].dt.year  # transforma ano + mês em número contínuo
    gastos_por_mes = df.groupby('mes')['valor'].sum().reset_index()

    if len(gastos_por_mes) < 2:
        return "Dados insuficientes"

    X = gastos_por_mes['mes'].values.reshape(-1, 1)
    y = gastos_por_mes['valor'].values

    modelo = LinearRegression()
    modelo.fit(X, y)

    proximo_mes = X.max() + 1
    previsao = modelo.predict([[proximo_mes]])
    return round(previsao[0], 2)
