pipeline {
    agent any

    stages {
        stage('build') {
            steps {
                sh 'docker build . --no-cache --build-arg GRAMMAR_VERSION=legacy/grammar -t web-openccg:$(git rev-parse --short HEAD)'
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
                sh 'docker-compose -f docker-compose.deploy.yml --project-name litmus up --detach --renew-anon-volumes --force-recreate'
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

