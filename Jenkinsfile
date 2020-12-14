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
                sh '''  #!/bin/bash
                        make setup
                        cat ~/.bash_profile
                        ls -la ~
                        'echo $USER
                        echo $PATH
                        source ~/.bookstore_api/bin/activate
                        echo $VIRTUAL_ENV
                        echo $PATH
                        make
                '''
            }
        }
        stage('deploy') {
            steps {
                echo "echo deploy"
            }
        }
    }
}
