from flask import Flask, request, render_template, redirect
import pandas as pd
import os
from modelo import prever_gasto

app = Flask(__name__)
DATA_FILE = 'data.csv'

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render define a variável PORT
    app.run(host='0.0.0.0', port=port)
