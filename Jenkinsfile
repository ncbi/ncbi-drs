pipeline
{
    agent any

    stages {
        stage('Build') {
            steps {
                sh './build.sh'
            }
        }
        stage('Test') {
            steps {
                sh './build.sh test'
            }
        }
        stage('docs') {
            steps {
                sh './build.sh docs'
            }
        }
        stage('package') {
            steps {
                sh './build.sh package'
            }
        }
    }
}
