from flask import Flask, request, render_template, redirect, session, url_for
import pandas as pd
import os
from modelo import prever_gasto

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'chave-super-secreta')

DATA_FILE = 'data.csv'
PASSWORD = 'David'  # senha definida

# Tela de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        senha = request.form.get('senha')
        if senha == PASSWORD:
            session['autenticado'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', erro='Senha incorreta')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Decorador que protege as rotas
def login_requerido(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('autenticado'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_requerido
def index():
    df = pd.read_csv(DATA_FILE)
    previsao = prever_gasto(df)
    return render_template('index.html', dados=df.to_dict(orient='records'), previsao=previsao)

@app.route('/adicionar', methods=['POST'])
@login_requerido
def adicionar():
    novo = {
        "data": request.form['data'],
        "descricao": request.form['descricao'],
        "valor": float(request.form['valor'])
    }
    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, pd.DataFrame([novo])])
    df.to_csv(DATA_FILE, index=False)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
