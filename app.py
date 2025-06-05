from flask import Flask, request, render_template, redirect
import pandas as pd
import os
from modelo import prever_gasto

app = Flask(__name__)
DATA_FILE = 'data.csv'
PASSWORD = 'David'  # Altere isso

def check_auth(password):
    return password == PASSWORD

# Antes de qualquer requisição, verifica se a senha está presente e correta
@app.before_request
def restrict_access():
    # Permite acesso ao favicon sem senha
    if request.endpoint == 'static':
        return
    password = request.args.get('senha')
    if not check_auth(password):
        return Response('Acesso negado. Adicione ?senha=David na URL.', 401)

@app.route('/')
def index():
    df = pd.read_csv(DATA_FILE)
    previsao = prever_gasto(df)
    return render_template('index.html', dados=df.to_dict(orient='records'), previsao=previsao)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    novo = {
        "data": request.form['data'],
        "descricao": request.form['descricao'],
        "valor": float(request.form['valor'])
    }
    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, pd.DataFrame([novo])])
    df.to_csv(DATA_FILE, index=False)
    return redirect('/')

