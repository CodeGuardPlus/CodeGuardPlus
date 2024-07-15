wget https://github.com/github/codeql-cli-binaries/releases/download/v2.17.5/codeql-linux64.zip
unzip codeql-linux64.zip -d ~
git clone --depth=1 --branch codeql-cli-2.17.5 https://github.com/github/codeql.git ~/codeql/codeql-repo
~/codeql/codeql pack download codeql-cpp@0.7.1 codeql-python@0.6.2 codeql/ssa@0.0.16 codeql/tutorial@0.0.9 codeql/regex@0.0.12 codeql/util@0.0.9
cp data/base/cwe-190/1-c/ArithmeticTainted.ql ~/codeql/codeql-repo/cpp/ql/src/Security/CWE/CWE-190/ArithmeticTainted.ql