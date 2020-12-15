pipeline {
    agent {
        label 'jenkins_slave_1'
    }
    parameters {
        choice(name: 'Command', choices: ['execute_tests', 'setup'], description: '')
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
                script { 
                    if( params.Command == 'setup' ) {
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
                    publishHTML (target: [
                      allowMissing: false,
                      alwaysLinkToLastBuild: true,
                      keepAll: true,
                      reportDir: '/var/lib/jenkins/workspace/api_tests_job/reports/',
                      reportFiles: 'report.html',
                      reportName: "HTML Report"
                    ])
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
