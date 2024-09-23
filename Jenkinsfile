def unitStatus
def robotStatus

pipeline {
    agent { label 'build-agent' }
    environment {
        APP_NAME = "web-api"
        IMAGE_NAME = 'spdx:${BUILD_NUMBER}'
        ROBOT_REPO = 'https://github.com/CE-RELATIONSHIP/jenkins-automate-testing'
        ROBOT_BRANCH = 'main'
        MAIN_REPO = 'https://https://github.com/CE-RELATIONSHIP/jenkins-assignment/'
        MAIN_BRANCH = 'jenkins-pipeline-peqch-only'
    }

    stages {
        stage("Build") {
            steps {
                sh "docker build --tag ${IMAGE_NAME} ."
                sh "docker image ls"
            }
        }

        stage("Run and Test"){
            steps {
                ////// update and start container //////
                script {
                    sh(script: "docker stop ${APP_NAME}", returnStatus: true)
                    sh(script: "docker rm ${APP_NAME} -f", returnStatus: true)

                    sh(script: "docker run --name ${APP_NAME} -d -p 80:5000 ${IMAGE_NAME}")
                }

                ////// unit test running batch  //////
                script {
                    def output = sh(
                        returnStatus: true,
                        returnStdout: true, 
                        script: "docker exec ${APP_NAME} sh -c 'python -m unit_test -v;'"
                        )

                    // if not OK
                    if (output != "0") {
                        error("Build terminated: failed the unit test'.")
                    }
                }
                /////////////////////////////////////////
            }
        }

        stage("Deliver") {
            steps {
                sh "echo Deliver"
            }
        }

        stage("Deploy") {
            agent { label 'deploy-server' }
            steps {
                sh "echo Deploy"
            }
        }

    }
}