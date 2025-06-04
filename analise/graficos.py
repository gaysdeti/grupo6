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
plt.savefig("/app/dados/grafico_tipo_violencia.png")
plt.close()

# Gráfico 2: Identidade de Gênero
plt.figure(figsize=(10, 6))
sns.countplot(y="IdentidadeGenero", data=df, order=df["IdentidadeGenero"].value_counts().index)
plt.title("Distribuição por Identidade de Gênero")
plt.tight_layout()
plt.savefig("/app/dados/grafico_identidade_genero.png")
plt.close()

# Gráfico 3: Orientação Sexual
plt.figure(figsize=(10, 6))
sns.countplot(y="OrientacaoSexual", data=df, order=df["OrientacaoSexual"].value_counts().index)
plt.title("Distribuição por Orientação Sexual")
plt.tight_layout()
plt.savefig("/app/dados/grafico_orientacao_sexual.png")
plt.close()

# Conversão de Idade para inteiro
df["Idade"] = pd.to_numeric(df["Idade"], errors="coerce")
df = df.dropna(subset=["Idade"])
df["Idade"] = df["Idade"].astype(int)

# Gráfico 4: Linha da quantidade de denúncias por idade
plt.figure(figsize=(10, 6))
df['Idade'] = pd.to_numeric(df['Idade'], errors='coerce')
df_idade = df.groupby('Idade')['TipoDenuncia'].count().reset_index()
df_idade.columns = ['Idade', 'Quantidade']

sns.lineplot(data=df_idade, x='Idade', y='Quantidade')
plt.title("Quantidade de Denúncias por Idade")
plt.xlabel("Idade")
plt.ylabel("Quantidade de Denúncias")
plt.tight_layout()
plt.savefig("/app/dados/grafico_denuncias_por_idade.png")
plt.close()

# Gráfico 5: Tipo de Violência por Identidade de Gênero
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x="TipoViolencia", hue="IdentidadeGenero", order=df["TipoViolencia"].value_counts().index)
plt.title("Tipo de Violência por Identidade de Gênero")
plt.xlabel("Tipo de Violência")
plt.ylabel("Frequência")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("/app/dados/grafico_violencia_identidade_genero.png")
plt.close()

# Gráfico 6: Tipo de Violência por Orientação Sexual
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x="TipoViolencia", hue="OrientacaoSexual", order=df["TipoViolencia"].value_counts().index)
plt.title("Tipo de Violência por Orientação Sexual")
plt.xlabel("Tipo de Violência")
plt.ylabel("Frequência")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("/app/dados/grafico_violencia_orientacao_sexual.png")
plt.close()

# Gráfico 7: Heatmap de Tipo de Violência por Identidade de Gênero
plt.figure(figsize=(12, 6))
heatmap_data = df.groupby(['TipoViolencia', 'IdentidadeGenero']).size().unstack(fill_value=0)

sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu")
plt.title("Heatmap: Tipo de Violência por Identidade de Gênero")
plt.xlabel("Identidade de Gênero")
plt.ylabel("Tipo de Violência")
plt.tight_layout()
plt.savefig("/app/dados/grafico_heatmap_violencia_genero.png")
plt.close()

print("Todos os gráficos foram gerados com sucesso!")