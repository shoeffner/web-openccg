pipeline {
    agent any

    stages {
        stage('build') {
            steps {
                sh 'docker-compose build . -t web-openccg:$(git rev-parse --short HEAD)'
            }
        }

        stage('test') {
            steps {
                sh 'docker-compose -p litmus run --rm -v $(pwd)/tests:/tests openccg python3 -m unittest discover /tests'
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
