from flask import Flask, render_template, send_from_directory, jsonify
import os

app = Flask(__name__)

@app.route("/")
def exibir_graficos():
    return render_template("index.html")

@app.route("/dados/<path:filename>")
def servir_imagem(filename):
    from flask import make_response
    response = make_response(send_from_directory("/app/dados", filename))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/imagens")
def listar_imagens():
    arquivos = os.listdir("/app/dados")
    imagens = [f for f in arquivos if f.endswith(".png")]
    return jsonify(imagens)