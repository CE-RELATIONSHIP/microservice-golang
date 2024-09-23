pipeline {
    agent { label 'build-agent' }
    environment {
        APP_NAME = "web-api"
        IMAGE_NAME = 'spdx'
        ROBOT_REPO = 'https://github.com/CE-RELATIONSHIP/jenkins-automate-testing'
        ROBOT_BRANCH = 'main'
        MAIN_REPO = 'https://https://github.com/CE-RELATIONSHIP/jenkins-assignment/'
        MAIN_BRANCH = 'jenkins-pipeline-peqch-only'
        NAMESPACE = 'ce-relationship'
        GITHUB_CRED = credentials('github-registry')
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
                    // if not OK
                    if (sh(script: "docker exec ${APP_NAME} sh -c 'python -m unit_test -v; exit;'", returnStatus: true)) {
                        error("Build terminated: failed the unit test'.")
                    }
                }
                /////////////////////////////////////////
            }
        }

        stage("Release") {
            steps {
                sh "docker tag ${IMAGE_NAME} ghcr.io/${NAMESPACE}/${IMAGE_NAME}"
                sh "docker tag ${IMAGE_NAME} ghcr.io/${NAMESPACE}/${IMAGE_NAME}:${BUILD_NUMBER}"

                sh "docker login ghcr.io -u ${GITHUB_CRED_USR} -p ${GITHUB_CRED_PSW}"

                sh "docker push ghcr.io/${NAMESPACE}/${IMAGE_NAME}"
                sh "docker push ghcr.io/${NAMESPACE}/${IMAGE_NAME}:${BUILD_NUMBER}"

                sh "docker inspect ghcr.io/${NAMESPACE}/${IMAGE_NAME}"
                sh "docker inspect ghcr.io/${NAMESPACE}/${IMAGE_NAME}:${BUILD_NUMBER}"

                sh "docker rmi ghcr.io/${NAMESPACE}/${IMAGE_NAME}"
                sh "docker rmi ghcr.io/${NAMESPACE}/${IMAGE_NAME}:${BUILD_NUMBER}"
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