pipeline {
    agent any
    environment {
        DOCKER_USER = 'saim687'
    }
    stages {
        stage('Fetch') { 
            steps {
                checkout scm
            }
        }
        stage('Build and Run') {
            steps {
                sh "docker build -t ${DOCKER_USER}/sentiment-api:unstable ."
                sh "docker run -d -p 5000:5000 --name test-instance ${DOCKER_USER}/sentiment-api:unstable"
                sh "sleep 15"
            }
        }
        stage('Unit Test') {
            steps {
                sh "docker exec test-instance pytest tests/test_api.py"
            }
        }
        stage('UI Test') {
            steps {
                sh "docker exec test-instance pytest tests/test_ui.py"
            }
        }
        stage('Build and Push') {
            steps {
                sh "docker stop test-instance && docker rm test-instance"
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh "echo \$PASS | docker login -u \$USER --password-stdin"
                }
                sh "docker push ${DOCKER_USER}/sentiment-api:unstable"
                
                sh "git checkout stable-fallback"
                sh "docker build -t ${DOCKER_USER}/sentiment-api:stable ."
                sh "docker push ${DOCKER_USER}/sentiment-api:stable"
                sh "git checkout main"
            }
        }
        stage('Deploy to Minikube') {
            steps {
                sh "kubectl apply -f k8s/pvc.yaml"
                sh "kubectl apply -f k8s/blue-deployment.yaml"
                sh "kubectl apply -f k8s/green-deployment.yaml"
                sh "kubectl apply -f k8s/service.yaml"
            }
        }
    }
}
