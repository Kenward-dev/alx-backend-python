pipeline {
    agent {
        docker {
            image 'python:3.9-slim'
            args '-u root:root'
        }
    }
    
    environment {
        APP_DIR = 'messaging_app'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'github-credentials', 
                    url: 'https://github.com/Kenward-dev/alx-backend-python.git',
                    branch: 'main'
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                dir("${APP_DIR}") {
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install pytest
                    '''
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                dir("${APP_DIR}") {
                    sh '''
                        . venv/bin/activate
                        pytest test_simple.py -v -s --junitxml=test-results.xml
                    '''
                }
            }
        }
        
        stage('Generate Report') {
            steps {
                publishTestResults testResultsPattern: "${APP_DIR}/test-results.xml"
            }
        }
    }
    
    post {
        success {
            echo "All tests passed successfully!"
        }
    }
}