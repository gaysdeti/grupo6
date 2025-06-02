from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route("/")
def exibir_graficos():
    arquivos = os.listdir("/app/dados")  # Caminho certo montado via volume
    imagens = [f for f in arquivos if f.endswith(".png")]
    print("Imagens encontradas:", imagens)
    return render_template("index.html", imagens=imagens)

@app.route("/dados/<path:filename>")
def servir_imagem(filename):
    return send_from_directory("/app/dados", filename) #mostrar imagens no html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) #porta de exibicao
