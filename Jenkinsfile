pipeline {
    agent any
    parameters {
        choice(name: 'Command', choices: ['setup', 'execute_tests'], description: '')
    }
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

            }
        }
        stage('deploy') {
            steps {
                echo "echo deploy"
            }
        }
    }
}
