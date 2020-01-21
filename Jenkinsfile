pipeline
{
    agent any

    stages {
        stage('Build') {
            steps {
                sh './build.sh'
            }
        }
        stage('Unit Tests') {
            steps {
                sh './unit_test.sh'
            }
        }
        stage('Docs') {
            steps {
                sh './build_docs.sh'
            }
        }
        stage('Package') {
            steps {
                sh './package.sh'
            }
        }
        stage('Test') {
            steps {
                sh './test.sh'
            }
        }
    }
}
