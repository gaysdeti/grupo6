#!/bin/bash

# Criar o banco de dados
sudo -u postgres psql -c "CREATE DATABASE dados;"

# Criar tabelas no banco de dados 'dados'
sudo -u postgres psql -d dados -c "
CREATE TABLE denuncias (
    id_denuncia VARCHAR(50) PRIMARY KEY,
    tipo_de_denuncia VARCHAR(100) NOT NULL
);

CREATE TABLE vitimas (
    id_vitima VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    idade INTEGER NOT NULL,
    identidade_de_genero VARCHAR(50),
    orientacao_sexual VARCHAR(50),
    etnia VARCHAR(50),
    escolaridade VARCHAR(100),
    genero_biologico VARCHAR(20),
    id_denuncia VARCHAR(50) REFERENCES denuncias(id_denuncia) ON DELETE CASCADE
);

CREATE TABLE violencias (
    id_violencia SERIAL PRIMARY KEY,
    tipo_de_violencia VARCHAR(50) NOT NULL,
    periodo_do_dia VARCHAR(20) NOT NULL,
    endereco VARCHAR(255) NOT NULL,
    id_vitima VARCHAR(50) REFERENCES vitimas(id_vitima) ON DELETE CASCADE
);
"
