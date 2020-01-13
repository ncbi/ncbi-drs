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
                sh 'build.sh'
            }
        }
        stage('docs') {
            steps {
                sh 'build.sh docs'
            }
        }
        stage('package') {
            steps {
                sh 'build.sh package'
            }
        }
    }
}
