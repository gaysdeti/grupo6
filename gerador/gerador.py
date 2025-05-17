import csv
import random
import faker
import os
import math

# Inicializa o gerador de dados falsos
fake = faker.Faker("pt_BR")

# Definição de valores possíveis para os campos
tipos_de_denuncia = ['Assedio', 'Discriminacao', 'Agressao', 'Violencia Domestica', 'Outros']
tipos_de_violencia = ['Fisica', 'Psicologica', 'Sexual', 'Patrimonial', 'Moral']
periodos_do_dia = ['Manha', 'Tarde', 'Noite', 'Madrugada']
estados = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
identidades_de_genero = ['Mulher Cisgenero', 'Mulher Transgenero', 'Homem Cisgenero', 'Homem Transgenero', 'Nao-Binario']
orientacoes_sexuais = ['Heterossexual', 'Homossexual', 'Bissexual', 'Assexual', 'Pansexual']
etnias = ['Branco', 'Negro', 'Pardo', 'Amarelo', 'Indigena']
escolaridades = ['Ensino Fundamental Incompleto', 'Ensino Fundamental Completo', 'Ensino Medio Incompleto', 'Ensino Medio Completo', 'Ensino Superior Incompleto', 'Ensino Superior Completo', 'Pos-graduacao']
generos_biologicos = ['Feminino', 'Masculino']

def gerar_idade(corromper=False):
    if not corromper:
        return random.randint(0, 110)
    else:
        return random.choice([float('nan'), random.randint(120, 200)])

def gerar_dados(qtd=1000):
    dados = []
    for i in range(qtd):
        # 20% de chance de erro na idade
        erro_idade = random.random() < 0.2
        # Outros erros aleatórios
        erro = random.choice([None, "erro_tipo", "erro_estado", "vazio"]) if not erro_idade else None

        tipo_de_denuncia = random.choice(tipos_de_denuncia if erro != "erro_tipo" else ["Invalido"]) if erro != "vazio" else ""
        id_denuncia = i + 1

        tipo_violencia = random.choice(tipos_de_violencia)
        periodo_dia = random.choice(periodos_do_dia)
        endereco = f"{fake.street_name()}, {random.randint(1, 1000)}" if erro != "vazio" else ""
        estado = random.choice(estados if erro != "erro_estado" else ["XX"]) if erro != "vazio" else ""
        id_violencia = i + 1

        nome = fake.name() if erro != "vazio" else ""
        idade = gerar_idade(erro_idade)
        identidade_de_genero = random.choice(identidades_de_genero) if erro != "vazio" else ""
        orientacao_sexual = random.choice(orientacoes_sexuais) if erro != "vazio" else ""
        etnia = random.choice(etnias) if erro != "vazio" else ""
        escolaridade = random.choice(escolaridades) if erro != "vazio" else ""
        genero_biologico = random.choice(generos_biologicos) if erro != "vazio" else ""

        dados.append([
            id_denuncia, tipo_de_denuncia,
            id_violencia, tipo_violencia, periodo_dia, endereco, estado,
            nome, idade, identidade_de_genero, orientacao_sexual, etnia, escolaridade, genero_biologico
        ])
    return dados

# Gerando os dados
dados = gerar_dados(1000)

# Nome fixo para sobrescrever o mesmo arquivo
arquivo_nome = "dados_denuncia.csv"

# Criando arquivo CSV
with open(arquivo_nome, "w", newline="", encoding="utf-8") as arquivo:
    writer = csv.writer(arquivo, delimiter=";")
    writer.writerow([
        "id_denuncia", "tipo_de_denuncia", "id_violencia", "tipo_violencia", 
        "periodo_dia", "endereco", "estado", "nome", "idade", "identidade_de_genero", 
        "orientacao_sexual", "etnia", "escolaridade", "genero_biologico"
    ])
    writer.writerows(dados)

print(f"Arquivo {arquivo_nome} gerado com sucesso!")
