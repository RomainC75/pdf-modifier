pipeline {
  agent any
  tools {nodejs "node"}
  stages {
    stage('checkout code') {
      steps {
        git(url: 'https://github.com/RomainC75/pdf-modifier', branch: 'dev')
      }
    }

    stage('log') {
      parallel {
        stage('log') {
          steps {
            sh 'ls -la'
          }
        }

        stage('install') {
          steps {
            sh 'cd server && npm i && npm run dev'
          }
        }

      }
    }

  }
}
