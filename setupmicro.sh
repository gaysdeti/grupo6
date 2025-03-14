#!/bin/bash

# Atualiza pacotes e instala dependências necessárias
sudo apt update && sudo apt install -y python3 python3-pip

# Verifica se as dependências já estão instaladas
type flask >/dev/null 2>&1 || pip3 install flask
type psycopg2 >/dev/null 2>&1 || pip3 install psycopg2-binary

# Define variáveis de ambiente para o banco de dados
export DB_NAME=dados
export DB_USER=postgres
export DB_HOST=192.168.56.20
export DB_PORT=5432

# Inicia o microserviço no background e redireciona logs
nohup python3 /vagrant/microservico.py > /vagrant/microservico.log 2>&1 &

# Aguarda um tempo para o serviço iniciar
sleep 5

# Verifica se o microserviço está rodando
if curl -s http://localhost:5000/health | grep -q 'OK'; then
    echo "Microserviço iniciado com sucesso!"
else
    echo "Erro ao iniciar o microserviço. Verifique os logs em /vagrant/microservico.log"
fi
