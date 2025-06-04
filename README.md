# Projeto Integrador - Grupo 6: Gays de TI 🏳️‍🌈

Este repositório contém o Projeto Integrador do **Grupo 6 - Gays de TI**, desenvolvido com foco em Big Data, visualização de dados, integração contínua e monitoramento de containers Docker.

---

## 📌 Descrição Geral

O projeto realiza o seguinte fluxo:

1. **Geração de Dados (gerador.py)**  
   Produz dados simulando denúncias envolvendo questões de identidade de gênero, orientação sexual, violência e outros atributos sociais.

2. **Tratamento dos Dados (tratamento.R)**  
   Limpa e padroniza os dados brutos, salvando um novo arquivo `dados_tratados.csv`.

3. **Análise e Visualização (graficos.py)**  
   Gera automaticamente gráficos a partir dos dados tratados, salvando as imagens em `/dados`.

4. **Visualização Web (Flask + JS)**  
   Exibe os gráficos em uma página web atualizada automaticamente, acessível via navegador.

5. **Automação com Jenkins**  
   Jenkins executa todo o pipeline a cada minuto (CI/CD), reconstruindo os dados e atualizando os gráficos automaticamente.

6. **Monitoramento com Prometheus + Grafana + cAdvisor**  
   Visualização dos containers ativos, métricas e controle do sistema.

---

## Estrutura dos Microserviços

```bash
├── gerador/           # Microserviço gerador de dados (Python)
├── tratamento/        # Microserviço de limpeza dos dados (R)
├── analise/           # Microserviço de análise e geração de gráficos (Python)
├── web/               # Serviço Flask que exibe os gráficos
│   ├── app.py
│   ├── templates/
│   │   └── index.html
├── dados/             # Pasta de dados compartilhados (volume)
├── prometheus/        # Configuração do Prometheus
├── grafana/           # Dados persistentes do Grafana
├── jenkins/           # Jenkinsfile e configurações
├── docker-compose.yml
└── README.md
```

---

## Como Executar

### 1. Clone o repositório:

```bash
git clone https://github.com/gaysdeti/grupo6.git
cd grupo6
```

### 2. Suba o ambiente completo com Docker:

```bash
docker compose up --build
```

> O Jenkins irá iniciar automaticamente os microserviços a cada 1 minuto.

### 3. Acesse os serviços:

- **Web (Flask com gráficos):** http://localhost:5000  
- **Grafana:** http://localhost:3000  
- **Prometheus:** http://localhost:9090  
- **Jenkins:** http://localhost:8090  

---

## Gráficos Disponíveis

- Distribuição por Tipo de Violência  
- Distribuição por Identidade de Gênero  
- Distribuição por Orientação Sexual  
- Distribuição de Denúncias por Idade (gráfico de linha)  
- Tipo de Violência por Identidade de Gênero (gráfico combinado)  
- Tipo de Violência por Orientação Sexual (gráfico combinado)  
- Correlação entre variáveis (heatmap)

---

## Tecnologias Utilizadas

- **Python** – Geração e análise dos dados
- **R** – Tratamento e limpeza dos dados
- **Flask** – Backend para visualização
- **JavaScript** – Atualização dinâmica dos gráficos
- **Docker** – Contêineres isolados para cada microserviço
- **Jenkins** – Orquestração do pipeline CI/CD
- **Grafana + Prometheus + cAdvisor** – Monitoramento leve e eficaz

---

## Observações Técnicas

- Os gráficos são atualizados automaticamente na interface web com JavaScript (`setInterval`) sem precisar de recarregar a página.
- O volume Docker `dados_compartilhados` mantém a consistência entre os serviços.
- Todos os serviços estão orquestrados via `docker-compose.yml`.

---

## Autoria

> Projeto desenvolvido por **Grupo 6 - Gays de TI**  
> Curso de Ciências da Computação — Projeto Integrador 2025
