#!/bin/bash

# Atualizar os pacotes
apt-get update

# Instalar dependências do Python
apt-get install -y python3 python3-pip

# Instalar pacotes Python necessários
pip3 install pandas numpy

# Executar o gerador de dados
python3 /vagrant/gerador_dados.py

echo "Instalação e execução do gerador de dados concluídas!"
