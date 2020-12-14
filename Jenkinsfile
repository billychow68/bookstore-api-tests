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
                if( ${params.Command} == 'setup' ) {
                   sh '''
                        #!/bin/bash
                        make setup
                    '''
                }
                else {
                    sh '''  
                        #!/bin/bash
                        # make setup
                        cat ~/.bash_profile
                        ls -la ~
                        echo $USER
                        echo $PATH
                        source ~/.bookstore_api/bin/activate
                        echo $VIRTUAL_ENV
                        echo $PATH
                        make
                    '''
                }
            }
        }
        stage('deploy') {
            steps {
                echo "echo deploy"
            }
        }
    }
}
