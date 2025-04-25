pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "nba-ticket-booking"
        DOCKER_TAG = "latest"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/yourusername/your-repo.git'  // Replace with your repository URL
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG .'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // You can set up Django tests here
                    sh 'docker run --rm $DOCKER_IMAGE:$DOCKER_TAG python manage.py test'
                }
            }
        }

        stage('Deploy to Staging') {
            steps {
                script {
                    // Deploy to your staging server here, e.g., push the Docker image to a registry
                    // Example: Docker push command or deployment script
                    sh 'docker push $DOCKER_IMAGE:$DOCKER_TAG'
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                script {
                    // Deploy to production server
                    // For example, SSH to production and pull the Docker image
                    sh 'ssh user@your-prod-server "docker pull $DOCKER_IMAGE:$DOCKER_TAG && docker-compose -f /path/to/docker-compose.yml up -d"'
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
