FROM r-base:latest

WORKDIR /app

COPY . .

RUN R -e "install.packages(c('dplyr', 'stringi'), repos='https://cloud.r-project.org/')"

CMD ["Rscript", "tratamento.R"]
