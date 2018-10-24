pipeline {
    agent any

    environment {
        APPLICATION_ROOT = '/openccg'
    }

    stages {
        stage('build') {
            steps {
                sh 'docker build . --no-cache -t web-openccg:$(git rev-parse --short HEAD)'
            }
        }

        stage('test') {
            steps {
                sh 'docker run --rm web-openccg:$(git rev-parse --short HEAD) python3 -m unittest discover /tests'
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
                sh 'docker-compose --project-name litmus up --detach --renew-anon-volumes --force-recreate'
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

