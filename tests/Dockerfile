FROM ubuntu:latest
COPY tests/server-test.sh server-test.sh 
RUN apt update && apt install -y netcat && chmod u+x server-test.sh 
ENTRYPOINT ["/bin/sh"]
