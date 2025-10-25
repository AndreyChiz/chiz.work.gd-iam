pipeline {
    agent any

    stages {
        stage('Install Build Tools') {
            steps {
                sh './scripts/install_build_tools.sh'
            }
        }

        stage('Build Wheels') {
            steps {
                sh './scripts/build_wheels.sh'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh './scripts/build_docker_image.sh'
            }
        }
    }
}
