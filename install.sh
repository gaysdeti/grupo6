#!/bin/bash

# Atualiza pacotes
apt-get update

# Verifica se o PostgreSQL já está instalado
if ! command -v psql &> /dev/null; then
    echo "Instalando PostgreSQL..."
    apt-get install -y postgresql postgresql-contrib
else
    echo "PostgreSQL já está instalado."
fi

# Habilita e inicia o serviço do PostgreSQL
systemctl enable postgresql
systemctl start postgresql

# Configura o PostgreSQL para aceitar conexões remotas (opcional)
echo "Configurando PostgreSQL para conexões remotas..."
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/*/main/postgresql.conf
echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/*/main/pg_hba.conf
systemctl restart postgresql

echo "Instalação e configuração do PostgreSQL concluídas!"
