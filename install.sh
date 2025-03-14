#!/bin/bash

# Definir o arquivo de log
LOGFILE="/var/log/install_script.log"

# Função para log
log() {
    echo "$(date) - $1" >> $LOGFILE
}

# Log de início
log "Iniciando o script de instalação."

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

# Instalar pacotes adicionais com pip
echo "Instalando pandas e numpy..."
log "Instalando pandas e numpy..."
pip3 install pandas numpy

# Limpar pacotes não necessários
echo "Limpando pacotes não necessários..."
log "Limpando pacotes não necessários..."
apt-get autoremove -y
apt-get clean

# Verificar se as instalações foram bem-sucedidas
if python3 -c "import pandas, numpy" &>/dev/null; then
    echo "Instalação concluída com sucesso!"
    log "Instalação concluída com sucesso!"
else
    echo "Houve um problema na instalação dos pacotes."
    log "Erro: Falha ao instalar pandas ou numpy."
    exit 1
fi

# Notificação de sucesso (caso esteja em um ambiente gráfico)
notify-send "Instalação Concluída" "O script foi executado com sucesso."

# Log de finalização
log "Script de instalação concluído."
