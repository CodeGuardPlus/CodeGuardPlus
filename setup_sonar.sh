#setup server
docker pull sonarqube
docker run -d --name sonarqube -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true -p 9000:9000 sonarqube:latest

# setup scanner
export SONAR_SCANNER_HOME=./.sonar/sonar-scanner-5.0.1.3006-linux
curl --create-dirs -sSLo ./.sonar/sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
unzip -o ./.sonar/sonar-scanner.zip -d ./.sonar/
export PATH=$SONAR_SCANNER_HOME/bin:$PATH
export SONAR_SCANNER_OPTS="-server"