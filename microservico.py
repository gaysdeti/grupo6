from flask import Flask, request, jsonify
import psycopg2
import os
from psycopg2 import pool

app = Flask(__name__)

# Configurações do banco via variáveis de ambiente
DB_NAME = os.getenv("DB_NAME", "dados")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")  # Senha opcional
DB_HOST = os.getenv("DB_HOST", "192.168.56.20")
DB_PORT = os.getenv("DB_PORT", "5432")

# Criando um pool de conexões
try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
except Exception as e:
    print(f"Erro ao conectar ao banco: {e}")
    connection_pool = None

# Função para obter conexão do pool
def get_db_connection():
    if connection_pool:
        return connection_pool.getconn()
    return None

# Endpoint de Health Check
@app.route('/health', methods=['GET'])
def health_check():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"status": "Banco OFFLINE"}), 500
    connection_pool.putconn(conn)
    return jsonify({"status": "OK"}), 200

# Endpoint para buscar todas as denúncias com paginação
@app.route('/denuncias', methods=['GET'])
def get_denuncias():
    page = int(request.args.get('page', 1))
    limit = 50
    offset = (page - 1) * limit

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com o banco"}), 500

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM denuncias LIMIT %s OFFSET %s;", (limit, offset))
        rows = cur.fetchall()
        cur.close()
        connection_pool.putconn(conn)
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar os dados: {e}"}), 500

# Endpoint para buscar denúncia específica por ID
@app.route('/denuncias/<id_denuncia>', methods=['GET'])
def get_denuncia(id_denuncia):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com o banco"}), 500

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM denuncias WHERE id_denuncia = %s;", (id_denuncia,))
        row = cur.fetchone()
        cur.close()
        connection_pool.putconn(conn)
        return jsonify(row) if row else (jsonify({"error": "Denúncia não encontrada"}), 404)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar denúncia: {e}"}), 500

# Endpoint para buscar vítimas de uma denúncia
@app.route('/denuncias/<id_denuncia>/vitimas', methods=['GET'])
def get_vitimas_por_denuncia(id_denuncia):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com o banco"}), 500

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM vitimas WHERE id_denuncia = %s;", (id_denuncia,))
        rows = cur.fetchall()
        cur.close()
        connection_pool.putconn(conn)
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar vítimas: {e}"}), 500

# Endpoint para inserir uma nova denúncia
@app.route('/denuncias', methods=['POST'])
def criar_denuncia():
    data = request.get_json()
    if not data or 'tipo_de_denuncia' not in data or 'id_denuncia' not in data:
        return jsonify({"error": "Campos obrigatórios: tipo_de_denuncia, id_denuncia"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com o banco"}), 500

    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO denuncias (tipo_de_denuncia, id_denuncia) VALUES (%s, %s);", 
                    (data['tipo_de_denuncia'], data['id_denuncia']))
        conn.commit()
        cur.close()
        connection_pool.putconn(conn)
        return jsonify({"message": "Denúncia adicionada com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": f"Erro ao inserir denúncia: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)