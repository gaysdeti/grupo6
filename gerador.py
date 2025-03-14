import pandas as pd
import random
import os

# Função auxiliar para selecionar aleatoriamente um valor de uma lista
def escolher_aleatorio(lista):
    return random.choice(lista)

# Função para gerar dados de uma vítima
def gerar_vitima(id_denuncia, num_vitima):
    nome = f'Vítima {num_vitima}'
    idade = random.randint(18, 80)
    identidade_de_genero = escolher_aleatorio(identidades_de_genero)
    orientacao_sexual = escolher_aleatorio(orientacoes_sexuais)
    etnia = escolher_aleatorio(etnias)
    escolaridade = escolher_aleatorio(escolaridades)
    genero_biologico = escolher_aleatorio(generos_biologicos)
    id_vitima = f'vitima_{num_vitima}'

    return {
        'nome': nome,
        'idade': idade,
        'identidade_de_genero': identidade_de_genero,
        'orientacao_sexual': orientacao_sexual,
        'etnia': etnia,
        'escolaridade': escolaridade,
        'genero_biologico': genero_biologico,
        'id_denuncia': id_denuncia,
        'id_vitima': id_vitima
    }

# Função para gerar dados de uma denúncia
def gerar_denuncia(num_denuncia):
    tipo_de_denuncia = escolher_aleatorio(tipos_de_denuncia)
    id_denuncia = f'denuncia_{num_denuncia}'
    return {
        'tipo_de_denuncia': tipo_de_denuncia,
        'id_denuncia': id_denuncia
    }

# Função para gerar dados de violência
def gerar_violencia(id_vitima, num_violencia):
    tipo_de_violencia = escolher_aleatorio(tipos_de_violencia)
    periodo_do_dia = escolher_aleatorio(periodos_do_dia)
    endereco = f'Rua {num_violencia}, Cidade {num_violencia} - {escolher_aleatorio(estados)}'

    return {
        'tipo_de_violencia': tipo_de_violencia,
        'periodo_do_dia': periodo_do_dia,
        'endereco': endereco,
        'id_vitima': id_vitima
    }

# Função para gerar os dados
def gerar_dados(num_denuncias):
    denuncias = []
    vitimas = []
    violencias = []

    for i in range(num_denuncias):
        # Gerar dados para denúncia, vítima e violência
        denuncia = gerar_denuncia(i+1)
        denuncias.append(denuncia)

        vitima = gerar_vitima(denuncia['id_denuncia'], i+1)
        vitimas.append(vitima)

        violencia = gerar_violencia(vitima['id_vitima'], i+1)
        violencias.append(violencia)

    return denuncias, vitimas, violencias

# Função para salvar os dados em arquivos CSV
def salvar_dados(denuncias, vitimas, violencias):
    # Criação de diretório para salvar os arquivos
    pasta = 'dados_gerados'
    if not os.path.exists(pasta): ##
        os.makedirs(pasta)

    # Criar DataFrames
    df_denuncias = pd.DataFrame(denuncias)
    df_vitimas = pd.DataFrame(vitimas)
    df_violencias = pd.DataFrame(violencias)

    # Salvar DataFrames em arquivos CSV
    df_denuncias.to_csv(os.path.join(pasta, 'denuncias.csv'), index=False)
    df_vitimas.to_csv(os.path.join(pasta, 'vitimas.csv'), index=False)
    df_violencias.to_csv(os.path.join(pasta, 'violencias.csv'), index=False)

    print("Dados gerados e salvos em arquivos CSV na pasta 'dados_gerados'.")

# Listas de atributos possíveis
tipos_de_denuncia = ['Assédio', 'Discriminação', 'Agressão', 'Violência Doméstica', 'Outros']
identidades_de_genero = ['Mulher Cisgênero', 'Mulher Transgênero', 'Homem Cisgênero', 'Homem Transgênero', 'Não-Binário']
orientacoes_sexuais = ['Heterossexual', 'Homossexual', 'Bissexual', 'Assexual', 'Pansexual']
etnias = ['Branco', 'Negro', 'Pardo', 'Amarelo', 'Indígena']
escolaridades = ['Ensino Fundamental Incompleto', 'Ensino Fundamental Completo', 'Ensino Médio Incompleto', 'Ensino Médio Completo', 'Ensino Superior Incompleto', 'Ensino Superior Completo', 'Pós-graduação']
generos_biologicos = ['Feminino', 'Masculino']
tipos_de_violencia = ['Física', 'Psicológica', 'Sexual', 'Patrimonial', 'Moral']
periodos_do_dia = ['Manhã', 'Tarde', 'Noite', 'Madrugada']
estados = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

# Gerar e salvar os dados
num_denuncias = 1000  # Defina o número de registros a serem gerados
denuncias, vitimas, violencias = gerar_dados(num_denuncias)
salvar_dados(denuncias, vitimas, violencias)
