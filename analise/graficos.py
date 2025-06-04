import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os

# Remove imagens antigas
for file in os.listdir("/app/dados"):
    if file.endswith(".png"):
        os.remove(f"/app/dados/{file}")

# Caminho do arquivo CSV (ajustado para o volume Docker)
caminho_arquivo = "/app/dados/dados_tratados.csv"

# Verifica se o arquivo existe
if not os.path.exists(caminho_arquivo):
    print(f"Arquivo não encontrado: {caminho_arquivo}")
    exit(1)

# Leitura do CSV
df = pd.read_csv(caminho_arquivo, sep=";", na_values=[""])
df = df.astype(str)

# Gráfico 1: Tipo de Violência
plt.figure(figsize=(10, 6))
sns.countplot(y="TipoViolencia", data=df, order=df["TipoViolencia"].value_counts().index)
plt.title("Distribuição por Tipo de Violência")
plt.tight_layout()
plt.savefig(f"/app/dados/grafico_tipo_violencia.png")
plt.close()

# Gráfico 2: Identidade de Gênero
plt.figure(figsize=(10, 6))
sns.countplot(y="IdentidadeGenero", data=df, order=df["IdentidadeGenero"].value_counts().index)
plt.title("Distribuição por Identidade de Gênero")
plt.tight_layout()
plt.savefig(f"/app/dados/grafico_identidade_genero.png")
plt.close()

# Gráfico 3: Orientação Sexual
plt.figure(figsize=(10, 6))
sns.countplot(y="OrientacaoSexual", data=df, order=df["OrientacaoSexual"].value_counts().index)
plt.title("Distribuição por Orientação Sexual")
plt.tight_layout()
plt.savefig(f"/app/dados/grafico_orientacao_sexual.png")
plt.close()

print("Gráficos gerados com sucesso!")