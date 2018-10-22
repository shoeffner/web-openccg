pipeline {
    agent any

    stages {
        stage('build') {
            steps {
                sh 'docker build . -t web-openccg:$(git rev-parse --short HEAD)'
            }
        }

        stage('test') {
            steps {
                sh 'docker run --rm -v "$(pwd)/tests":/tests web-openccg:$(git rev-parse --short HEAD) python3 -m unittest discover /tests'
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
                sh 'docker-compose -p litmus up -d'
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
