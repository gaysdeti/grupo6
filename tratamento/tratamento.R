# Instalar pacotes necessários, se não estiverem instalados
pacotes <- c("dplyr", "stringi", "ggplot2")

instalar_faltantes <- pacotes[!pacotes %in% installed.packages()[,"Package"]]
if(length(instalar_faltantes)) install.packages(instalar_faltantes)

# Carregar os pacotes
lapply(pacotes, library, character.only = TRUE)

# 1. Carregar pacotes
library(dplyr)
library(stringi)
library(ggplot2)

# 2. Leitura dos dados
caminho <- "/app/dados/dados_denuncia.csv"
if (file.exists(caminho)) {
  dados <- read.csv(caminho, sep = ";", na.strings = "", stringsAsFactors = FALSE)
} else {
  stop(paste("Arquivo não encontrado em:", caminho))
}

# 3. Renomear colunas
colnames(dados) <- c("ID", "TipoDenuncia", "IDViolencia", "TipoViolencia", "PeriodoDia", 
                     "Endereco", "Estado", "Nome", "Idade", "IdentidadeGenero", 
                     "OrientacaoSexual", "Etnia", "Escolaridade", "GeneroBiologico")

# 4. Padronização de texto (remover espaços, acentos, minúsculas)
dados <- dados %>%
  mutate(across(where(is.character), ~ tolower(stri_trans_general(trimws(.), "Latin-ASCII")))) %>%
  mutate(Nome = gsub("^(dr\\.?|dra\\.?|sr\\.?|sra\\.?|srta\\.?)\\s+", "", Nome)) %>%

# Identificar e marcar nomes inválidos (exemplo: nomes com apenas números ou muito curtos)
  mutate(Nome = case_when(
    grepl("^[0-9]+$", Nome) | nchar(Nome) < 3 ~ "Nome inválido", # Critérios de "invalidez"
    TRUE ~ Nome
  ))

#5 Conversão da Idade e tratamento de outliers
# 4. Conversão da Idade e tratamento de outliers
dados$Idade <- as.numeric(gsub("[^0-9]", "", dados$Idade))

# Remover registros com idade ausente ou menor que 10 anos
dados <- dados %>% filter(!is.na(Idade) & Idade >= 10)

# Substituir idades maiores que 100 pela mediana das idades válidas
mediana_idade_valida <- median(dados$Idade[dados$Idade <= 100], na.rm = TRUE)
dados$Idade[dados$Idade > 100] <- mediana_idade_valida

# 6. Remoção e redistribuição de registros inválidos
dados_validos <- dados %>% filter(!is.na(TipoDenuncia) & TipoDenuncia != "invalido")
dados_invalidos <- dados %>% filter(!is.na(TipoDenuncia) & TipoDenuncia == "invalido")

tipos_validos <- unique(dados_validos$TipoDenuncia)

n_invalidos <- nrow(dados_invalidos)
n_tipos <- length(tipos_validos)
qtd_por_tipo <- n_invalidos %/% n_tipos
resto <- n_invalidos %% n_tipos

novos_invalidos <- data.frame()
idx <- 1

for (tipo in tipos_validos) {
  if (idx + qtd_por_tipo - 1 <= n_invalidos) {
    novos <- dados_invalidos[idx:(idx + qtd_por_tipo - 1), ]
    novos$TipoDenuncia <- tipo
    novos_invalidos <- rbind(novos_invalidos, novos)
    idx <- idx + qtd_por_tipo
  }
}

if (resto > 0) {
  moda_tipo <- names(sort(table(dados_validos$TipoDenuncia), decreasing = TRUE))[1]
  restantes <- dados_invalidos[idx:n_invalidos, ]
  restantes$TipoDenuncia <- moda_tipo
  novos_invalidos <- rbind(novos_invalidos, restantes)
}

dados <- rbind(dados_validos, novos_invalidos)

#6.1 Tratamento dos registros inválidos de Estado
estados_validos <- dados %>%
  filter(!is.na(Estado) & Estado != "xx") %>%
  pull(Estado) %>%
  unique()

indices_invalidos_estado <- which(is.na(dados$Estado) | dados$Estado == "xx")
n_invalidos_estado <- length(indices_invalidos_estado)
n_estados <- length(estados_validos)
qtd_por_estado <- n_invalidos_estado %/% n_estados
resto_estado <- n_invalidos_estado %% n_estados

novos_estados <- rep(estados_validos, each = qtd_por_estado)

if (resto_estado > 0) {
  moda_estado <- names(sort(table(dados$Estado[dados$Estado != "xx" & !is.na(dados$Estado)]), decreasing = TRUE))[1]
  novos_estados <- c(novos_estados, rep(moda_estado, resto_estado))
}

set.seed(123)
novos_estados <- sample(novos_estados)
dados$Estado[indices_invalidos_estado] <- novos_estados

# 7. Correção de inconsistências entre gênero biológico e identidade de gênero
dados <- dados %>%
  mutate(
    GeneroBiologico = case_when(
      IdentidadeGenero %in% c("homem cisgenero", "mulher transgenero") ~ "masculino",
      IdentidadeGenero %in% c("mulher cisgenero", "homem transgenero") ~ "feminino",
      TRUE ~ GeneroBiologico
    )
  )

#7.1 Removendo Denuncias 
# Padronizar colunas de texto para evitar erros de filtro
dados <- dados %>%
  mutate(
    IdentidadeGenero = tolower(stri_trans_general(trimws(IdentidadeGenero), "Latin-ASCII")),
    OrientacaoSexual = tolower(stri_trans_general(trimws(OrientacaoSexual), "Latin-ASCII"))
  )

#7.2 Removendo homens cis heteros
dados <- dados %>%
  filter(!(tolower(trimws(GeneroBiologico)) == "masculino" &
           tolower(trimws(IdentidadeGenero)) == "cisgenero" &
           tolower(trimws(OrientacaoSexual)) == "heterossexual"))

# 8. Preenchimento de valores faltantes com moda (para texto)
moda <- function(x) {
  uniq_x <- unique(na.omit(x))
  uniq_x[which.max(tabulate(match(x, uniq_x)))]
}

for (col in names(dados)) {
  if (is.character(dados[[col]])) {
    moda_col <- moda(dados[[col]])
    dados[[col]][is.na(dados[[col]])] <- moda_col
  }
}

# 9. Remover níveis não utilizados e ajustar fatores
dados[] <- lapply(dados, function(col) {
  if (is.character(col)) factor(col) else col
})
dados <- droplevels(dados)

# Garantir que IdentidadeGenero não tenha NA
if (any(is.na(dados$IdentidadeGenero))) {
  moda_genero <- names(sort(table(dados$IdentidadeGenero), decreasing = TRUE))[1]
  dados$IdentidadeGenero[is.na(dados$IdentidadeGenero)] <- moda_genero
}

# 10. Salvar os dados tratados
write.table(dados,
            file = "/app/dados/dados_tratados.csv",
            sep = ";",
            row.names = FALSE,
            col.names = TRUE,
            quote = TRUE,
            fileEncoding = "UTF-8",
            dec = ",")