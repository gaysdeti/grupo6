pipeline {
    agent any

    environment {
        PATH = "/usr/bin:/usr/local/bin:/bin:/usr/sbin:/sbin"
    }

    triggers {
        cron('H/1 * * * *') // Executa a cada 1 minuto
    }

    stages {
        stage('Executar Pipeline') {
            steps {
                // Gera os dados
                sh 'docker compose run --rm gerador'

                // Trata os dados
                sh 'docker compose run --rm tratamento'

                // Gera os gráficos
                sh 'docker compose run --rm analise'
            }
        }
    }
}
