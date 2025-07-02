pipeline {
    agent any
    
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
        
        stage('Install Python') {
            steps {
                sh '''
                    python3 --version || echo "Python3 not found"
                    pip3 --version || echo "pip3 not found"
                    
                    apt-get update || echo "Cannot update packages"
                    apt-get install -y python3 python3-pip python3-venv || echo "Cannot install packages, trying with existing Python"
                '''
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