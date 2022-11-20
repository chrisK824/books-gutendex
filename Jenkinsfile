pipeline {
	agent any

    stages {
        stage('Build deb11 package') {
            steps {
                script {
					deb11_name = sh(script: "cat ./package/control |grep Package | cut -d \":\" -f 2 |  sed 's/^[[:space:]]*//'", returnStdout: true).trim()
					deb11_version = sh(script: "cat ./package/control | grep Version | cut -d \":\" -f2 | cut -d \" \" -f2", returnStdout: true).trim()
				}
                sh "mkdir -p ${deb11_name}_${deb11_version}/usr/share/moro-books/"
                sh "mkdir -p ${deb11_name}_${deb11_version}/usr/bin/"
                sh "mkdir -p ${deb11_name}_${deb11_version}/DEBIAN/"
                sh "cp -v ./package/control ${deb11_name}_${deb11_version}/DEBIAN/"
                sh "cp -v ./package/postinst ${deb11_name}_${deb11_version}/DEBIAN/"
                sh "cp -vr ./src/* ${deb11_name}_${deb11_version}/usr/share/moro-books/"
                sh "cp -v ./requirements.txt ${deb11_name}_${deb11_version}/usr/share/moro-books/requirements.txt"
                sh "chmod -R 755 ${deb11_name}_${deb11_version}"
                sh "dpkg-deb --build ${deb11_name}_${deb11_version}"
            }
        }
	}
    post {
		success {
			echo 'Pipeline complete'
            archiveArtifacts '*.deb'
		}
	}
}
