pipeline {
    agent any

    stages {
        stage('pre-test') {
            steps {
                echo "pre-test stage"
                sh 'hostname'
                sh 'whoami'
                sh 'pwd'
                sh 'ls -la'
            }
        }
        stage('test') {
            steps {
                echo "test stage"
                sh 'make setup'
                sh 'source ~/.bookstore_api/bin/activate'
                // sh 'make'
            }
        }
        stage('deploy') {
            steps {
                echo "echo deploy"
            }
        }
    }
}