FROM openjdk:8-jre-alpine
RUN apk add --update \
    python \
    python-dev \
    build-base \
  && rm -rf /var/cache/apk/*

RUN mkdir -p /sqlline/

ARG SQLLINE_JAR_NAME="sqlline-1.2.0-jar-with-dependencies.jar"

ADD https://repo1.maven.org/maven2/sqlline/sqlline/1.2.0/${SQLLINE_JAR_NAME} /sqlline/
RUN ln -s /sqlline/$SQLLINE_JAR_NAME /sqlline/sqlline.jar
ADD pysqlline /sqlline/pysqlline
RUN chmod +x /sqlline/pysqlline/pysqlline.py

RUN addgroup -S sqlline && adduser -S -G sqlline sqlline
RUN chown -R sqlline: /sqlline
USER sqlline

ENTRYPOINT ["/sqlline/pysqlline/pysqlline.py"]
