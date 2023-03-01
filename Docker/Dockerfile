ARG CODE_VERSION=latest

# Runtime stage
FROM ubuntu:${CODE_VERSION}
LABEL maintainer "Alejandro Vega - <agevega@hotmail.com>"

COPY scripts /home/

ENV DB_HOST=""
ENV DB_DATABASE=""
ENV DB_PORT=""
ENV DB_USER=""
ENV DB_PASSWORD=""

EXPOSE 8080

WORKDIR /home

RUN ./packages.sh
RUN ./clone-repo.sh

ENTRYPOINT [ "/bin/bash" ]
CMD [ "run.sh" ]
