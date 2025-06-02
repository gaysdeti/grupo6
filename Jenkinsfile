pipeline {
    agent any

    triggers {
        cron('*/1 * * * *') // Executa a cada 1 minuto
    }

    stages {
        stage('Executar Pipeline') {
            steps {
                script {
                    sh 'docker exec projetopi7-gerador-1 python /app/gerador.py'
                    sh 'docker exec projetopi7-tratamento-1 Rscript /app/tratamento.R'
                    sh 'docker exec projetopi7-analise-1 python /app/graficos.py'
                }
            }
        }
    }
}
//o jenkinsfile local é para ir ao github e, ao puxar os codigos, ele gere um pipeline com base nesse script
//grafana e/ou prometheus é para monitorar e avisar quando a build é construida e/ou regerada (a cada 1min)
//como justificar as metricas na apresentacao?
