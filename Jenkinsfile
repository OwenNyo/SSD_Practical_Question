pipeline {
    agent any

    environment {
        APP_DIR = 'webapp'
        FLASK_PORT = '5000'
        SERVICE_NAME = 'web'
        SONARQUBE_ENV = 'SonarQube' // from docker-compose.yml
    }

    stages {

        stage('Install Dependencies') {
            steps {
                echo "📦 Creating virtual environment and installing requirements..."
                dir("${APP_DIR}") {
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Dependency Audit') {
            steps {
                echo "🔒 Running pip-audit to check for vulnerable dependencies..."
                dir("${APP_DIR}") {
                    sh '''
                        . venv/bin/activate
                        pip install pip-audit
                        pip-audit || echo "⚠️ Vulnerabilities found, but continuing..."
                    '''
                }
            }
        }

        stage('Lint Code') {
            steps {
                echo "🔍 Linting source files with flake8..."
                dir("${APP_DIR}") {
                    sh '''
                        . venv/bin/activate
                        pip install flake8
                        flake8 app.py test_app.py || true
                    '''
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo "🧪 Running unit tests..."
                dir("${APP_DIR}") {
                    script {
                        if (fileExists('test_app.py')) {
                            sh '. venv/bin/activate && python test_app.py'
                        } else {
                            echo "⚠️ test_app.py not found — skipping tests."
                        }
                    }
                }
            }
        }

        stage('Healthcheck') {
            steps {
                echo "🌐 Checking if Flask app is responding at http://${SERVICE_NAME}:${FLASK_PORT}..."
                script {
                    def healthUrl = "http://${SERVICE_NAME}:${FLASK_PORT}"
                    sh "curl -s --fail ${healthUrl} || (echo '❌ App is not responding' && exit 1)"
                }
            }
        }

        stage('SonarQube Analysis') {
            environment {
                PATH = "${env.PATH}:${pwd()}/sonar-scanner-5.0.1.3006-linux/bin"
            }
            steps {
                echo '🔎 Running SonarQube scan...'
                withSonarQubeEnv("${env.SONARQUBE_ENV}") {
                    withCredentials([string(credentialsId: 'SONAR_TOKEN', variable: 'SONAR_TOKEN')]) {
                        dir('webapp') {
                            sh '''
                                wget -q https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
                                unzip -q sonar-scanner-cli-5.0.1.3006-linux.zip
                                ./sonar-scanner-5.0.1.3006-linux/bin/sonar-scanner \
                                  -Dsonar.projectKey=flask-app \
                                  -Dsonar.sources=. \
                                  -Dsonar.python.version=3.11 \
                                  -Dsonar.host.url=http://sonarqube:9000 \
                                  -Dsonar.login=${SONAR_TOKEN}
                            '''
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed. Check logs above."
        }
        always {
            echo "📦 Pipeline run complete."
        }
    }
}
