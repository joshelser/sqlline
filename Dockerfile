FROM openjdk:8-jre-alpine
RUN apk add --update \
    python \
    python-dev \
    build-base \
  && rm -rf /var/cache/apk/*

RUN mkdir -p /sqlline/

ARG SQLLINE_JAR_NAME="sqlline-1.2.0-jar-with-dependencies.jar"

ADD https://repo1.maven.org/maven2/sqlline/sqlline/1.2.0/${SQLLINE_JAR_NAME} /sqlline/lib/
ADD https://repo1.maven.org/maven2/org/slf4j/slf4j-simple/1.7.22/slf4j-simple-1.7.22.jar /sqlline/lib/
ADD https://repo1.maven.org/maven2/org/slf4j/slf4j-api/1.7.22/slf4j-api-1.7.22.jar /sqlline/lib/
ADD pysqlline /sqlline/pysqlline
RUN chmod +x /sqlline/pysqlline/pysqlline.py

RUN addgroup -S sqlline && adduser -S -G sqlline sqlline
RUN chown -R sqlline: /sqlline
USER sqlline

ENTRYPOINT ["/sqlline/pysqlline/pysqlline.py"]
