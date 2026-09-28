pipeline {
    agent any
    stages {
        stage('Seguridad DevSecOps') {
            steps {
                sh 'chmod +x pipeline/ejecutar.sh'
                sh './pipeline/ejecutar.sh'
            }
        }
    }
}
