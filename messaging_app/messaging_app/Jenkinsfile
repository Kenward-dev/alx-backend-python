pipeline {
    agent {
        docker {
            image 'python:3.10'
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Python') {
            steps {
                sh 'echo "Python already available in Docker image"'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest --html=report.html'
            }
        }

        stage('Generate Report') {
            steps {
                sh 'cat report.html'
            }
        }
    }
}
