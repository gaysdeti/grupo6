import pandas as pd
from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

def carregar_csv(nome_arquivo):
    """Tenta carregar um arquivo CSV, retornando um DataFrame vazio se não existir."""
    if os.path.exists(nome_arquivo):
        return pd.read_csv(nome_arquivo)
    return pd.DataFrame()

# Carrega os dados de forma segura
df_denuncias = carregar_csv('denuncias.csv')
df_vitimas = carregar_csv('vitimas.csv')
df_violencias = carregar_csv('violencias.csv')

@app.route('/')
def index():
    denuncias = df_denuncias.to_dict('records')
    vitimas = df_vitimas.to_dict('records')
    violencias = df_violencias.to_dict('records')
    return render_template('index.html', denuncias=denuncias, vitimas=vitimas, violencias=violencias)

@app.route('/health')
def health_check():
    """Verifica se o serviço está rodando corretamente."""
    return jsonify(status='OK')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
