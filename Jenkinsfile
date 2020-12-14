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
                sh '#!/bin/bash'
                sh 'make setup'
                sh 'cat ~/.bash_profile'
                sh 'ls -la ~'
                sh 'echo $USER'
                sh 'echo $PATH'
                sh 'source ~/.bookstore_api/bin/activate'
                sh 'echo $VIRTUAL_ENV'
                sh 'echo $PATH'
                sh 'make'
            }
        }
        stage('deploy') {
            steps {
                echo "echo deploy"
            }
        }
    }
}
