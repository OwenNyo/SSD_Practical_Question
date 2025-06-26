pipeline {
    agent any

    environment {
        APP_DIR = 'webapp'
        FLASK_PORT = '5000'
        SERVICE_NAME = 'web'  // Must match docker-compose service name
    }

    stages {
        stage('Install Dependencies') {
            steps {
                echo "📦 Creating virtual environment and installing dependencies..."
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


        stage('Lint Code') {
            steps {
                echo "🔍 Linting source files with flake8..."
                dir("${APP_DIR}") {
                    sh '''
                        . venv/bin/activate
                        pip install flake8
                        flake8 app.py test_webapp.py || true
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
                            sh 'python3 test_app.py'
                        } else {
                            echo "⚠️ test_app.py not found — skipping tests."
                        }
                    }
                }
            }
        }

        stage('Healthcheck') {
            steps {
                echo "🌐 Checking if Flask app is responding..."
                // Test internal Docker Compose network
                script {
                    def healthUrl = "http://${SERVICE_NAME}:${FLASK_PORT}"
                    sh "curl -s --fail ${healthUrl} || (echo '❌ App is not responding' && exit 1)"
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
