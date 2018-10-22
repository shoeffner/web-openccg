pipeline {
    agent any

    environment {
        OPENCCG_NETWORK = 'litmus_default'
        OPENCCG_EXTERNAL_PORT = '8081'
    }

    stages {
        stage('build') {
            steps {
                sh 'docker build . -t web-openccg:$(git rev-parse --short HEAD)'
            }
        }

        stage('test') {
            steps {
                sh 'docker run --rm -v "$(pwd)/app":/app -v "$(pwd)/tests":/tests web-openccg:$(git rev-parse --short HEAD) python3 -m unittest discover /tests'
            }
        }

        stage('retag') {
            steps {
                sh 'docker tag web-openccg:$(git rev-parse --short HEAD) web-openccg:latest'
            }
            when {
                branch 'master'
            }
        }

        stage('deploy') {
            steps {
                sh 'docker-compose up -d'
            }
            when {
                branch 'master'
            }
        }
    }

    post {
        always {
            sh 'docker image rm web-openccg:$(git rev-parse --short HEAD)'
            deleteDir()
        }
    }
}
