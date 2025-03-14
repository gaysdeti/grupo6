#!/bin/bash

# Definir o arquivo de log
LOGFILE="/var/log/microservico_install_script.log"

# Função para log
log() {
    echo "$(date) - $1" >> $LOGFILE
}

# Log de início
log "Iniciando o script de instalação do microserviço."

# Verificar se o script está sendo executado como root
if [ "$(id -u)" -ne 0 ]; then
    echo "Este script precisa ser executado como root. Tente novamente com sudo."
    log "Erro: O script não foi executado como root."
    exit 1
fi

# Atualizar os pacotes
echo "Atualizando os pacotes..."
log "Atualizando os pacotes..."
apt-get update -y

# Verificar se o Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python 3 não encontrado, instalando..."
    log "Python 3 não encontrado, iniciando instalação."
    apt-get install -y python3
else
    echo "Python 3 já está instalado."
    log "Python 3 já está instalado."
fi

# Verificar se o pip3 está instalado
if ! command -v pip3 &> /dev/null; then
    echo "pip3 não encontrado, instalando..."
    log "pip3 não encontrado, iniciando instalação."
    apt-get install -y python3-pip
else
    echo "pip3 já está instalado."
    log "pip3 já está instalado."
fi

# Verificar se o arquivo requirements.txt existe
if [ -f "requirements.txt" ]; then
    echo "Instalando pacotes listados em requirements.txt..."
    log "Instalando pacotes listados em requirements.txt..."
    pip3 install -r requirements.txt
else
    echo "Arquivo requirements.txt não encontrado. Instalando Flask e psycopg2-binary."
    log "Arquivo requirements.txt não encontrado. Instalando Flask e psycopg2-binary."
    pip3 install flask psycopg2-binary
fi

# Limpar pacotes não necessários
echo "Limpando pacotes não necessários..."
log "Limpando pacotes não necessários..."
apt-get autoremove -y
apt-get clean

# Verificar se as instalações foram bem-sucedidas
if python3 -c "import flask, psycopg2" &>/dev/null; then
    echo "Instalação concluída com sucesso!"
    log "Instalação concluída com sucesso!"
else
    echo "Houve um problema na instalação dos pacotes."
    log "Erro: Falha ao instalar Flask ou psycopg2-binary."
    exit 1
fi

# Verificar conexão com o banco de dados (opcional)
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="seubanco"
DB_USER="seuusuario"
DB_PASS="suasenha"

echo "Verificando conexão com o banco de dados..."
log "Verificando conexão com o banco de dados..."
python3 -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='$DB_HOST', port='$DB_PORT', dbname='$DB_NAME', user='$DB_USER', password='$DB_PASS')
    print('Conexão com o banco de dados bem-sucedida!')
except Exception as e:
    print('Erro ao conectar no banco de dados:', e)
    exit(1)
"

# Notificação de sucesso (caso esteja em um ambiente gráfico)
notify-send "Instalação Concluída" "O script do microserviço foi executado com sucesso."

# Log de finalização
log "Script de instalação do microserviço concluído."
