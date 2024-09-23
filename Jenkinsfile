pipeline {
    agent { label 'build-agent' }
    environment {
        APP_NAME = "web-api"
        IMAGE_NAME = 'spdx'

        ROBOT_REPO = 'https://github.com/CE-RELATIONSHIP/jenkins-automate-testing'
        ROBOT_BRANCH = 'main'
        ROBOT_FILE = 'unit_test.robot'

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

                    sh(script: "docker run --name ${APP_NAME} -d -p 5000:5000 ${IMAGE_NAME}")
                }

                ////// unit test running batch  //////
                script {
                    // if not OK
                    if (sh(script: "docker exec ${APP_NAME} sh -c 'python -m unit_test -v; exit;'", returnStatus: true)) {
                        error("Build terminated: failed the unit test'.")
                    }
                }
                /////////////////////////////////////////

                ////// unit test running batch  //////
                git url: "${ROBOT_REPO}", branch: "${ROBOT_BRANCH}"
                sh "robot ${ROBOT_FILE}"
                //////////////////////////////////////
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

                sh "docker image prune -a -f"
            }
        }

        stage("Deploy") {
            agent { label 'deploy-server' }
            steps {
                sh "docker login ghcr.io -u ${GITHUB_CRED_USR} -p ${GITHUB_CRED_PSW}"
                sh "docker pull ghcr.io/${NAMESPACE}/${IMAGE_NAME}"

                sh(script: "docker run --name ${APP_NAME} -d -p 5000:5000 ghcr.io/${NAMESPACE}/${IMAGE_NAME}")
            }
        }

    }
}