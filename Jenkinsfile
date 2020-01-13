pipeline
{
    agent
    {
        docker
        {
            image 'ncbi-drs.ubuntu.ci'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    stages {
        stage('build') {
            steps {
                sh 'test'
            }
        }
        stage('docs') {
            steps {
                sh 'make docs'
            }
        }
        stage('package') {
            steps {
                sh 'make package'
            }
        }
    }
}
