pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
    }

    stages {

        stage('Checkout') {
            steps {
                echo "🔄 Checking out code..."
                checkout scm
            }
        }

        stage('Set Variables') {
            steps {
                script {
                    // читаем имя и версию из pyproject.toml
                    def name = sh(script: "grep -E '^name\\s*=' pyproject.toml | sed 's/name\\s*=\\s*\"\\(.*\\)\"/\\1/'", returnStdout: true).trim()
                    def version = sh(script: "grep -E '^version\\s*=' pyproject.toml | sed 's/version\\s*=\\s*\"\\(.*\\)\"/\\1/'", returnStdout: true).trim()

                    IMAGE_NAME = "${name}:${version}"
                    REGISTRY = "reg.chiz.work.gd" // TODO: add to jenkins env

                    echo "🔹 IMAGE_NAME=${IMAGE_NAME}"
                    echo "🔹 REGISTRY=${REGISTRY}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "🛠 Building Docker image..."
                    sh """
                        export IMAGE_NAME=${IMAGE_NAME}
                        export DOCKER_BUILDKIT=1
                        ./scripts/build.sh
                    """
                }
            }
        }

        stage('Push Image to Registry') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'privat_docker_registry_cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        echo "📤 Pushing image to registry..."
                        sh """
                            export IMAGE_NAME=${IMAGE_NAME}
                            export REGISTRY=${REGISTRY}
                            export DOCKER_USER=${DOCKER_USER}
                            export DOCKER_PASS=${DOCKER_PASS}
                            ./scripts/private_registry_push.sh
                        """
                    }
                }
            }
        }

        stage('Run docker-compose') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'privat_docker_registry_cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {

                    script {
                        echo "📦 Starting services with docker-compose..."
                        sh """
                            export DOCKER_USER=${DOCKER_USER}
                            export DOCKER_PASS=${DOCKER_PASS}
                            ./scripts/run.sh
                        """
                    }
                }
            }
        }



        }


    post {
        always {
            echo "✅ Pipeline finished."
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
