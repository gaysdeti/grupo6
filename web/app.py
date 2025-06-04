from flask import Flask, render_template, send_from_directory, jsonify, make_response
import os

app = Flask(__name__)

@app.route("/")
def exibir_graficos():
    return render_template("index.html")

@app.route("/dados/<path:filename>")
def servir_imagem(filename):
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)