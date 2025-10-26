pipeline {
    agent any

    environment {
        REGISTRY = "myregistry.example.com"                  // твой приватный реестр
        DOCKER_CRED = credentials('privat_docker_registry_cred')        // один Jenkins Credential
        DOCKER_USER = "${DOCKER_CRED_USR}"                  // username из Credential
        DOCKER_PASS = "${DOCKER_CRED_PSW}"                  // password из Credential
        DOCKER_BUILDKIT = "1"
    }

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
    }

    stages {

        stage('Checkout') {
            steps {
                echo "🔄 Checking out code..."
                checkout scm
            }
        }

    stage('Set IMAGE_NAME') {
        steps {
            script {
                def name = sh(script: "grep -E '^name\\s*=' pyproject.toml | sed 's/name\\s*=\\s*\"\\(.*\\)\"/\\1/'", returnStdout: true).trim()
                def version = sh(script: "grep -E '^version\\s*=' pyproject.toml | sed 's/version\\s*=\\s*\"\\(.*\\)\"/\\1/'", returnStdout: true).trim()
                env.IMAGE_NAME = "${name}:${version}"
                echo "🔹 IMAGE_NAME=${env.IMAGE_NAME}"
            }
        }
}



        stage('Build Docker Image') {
            steps {
                sh './scripts/build.sh'
            }
        }

        stage('Push Image to Registry') {
            steps {
                sh './scripts/private_registry_push.sh'
            }
        }

        stage('Clean Up') {
            steps {
                sh './scripts/cleanup.sh'
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
