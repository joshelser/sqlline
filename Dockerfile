FROM openjdk:8-jre
RUN mkdir -p /sqlline/lib
#ADD https://repo1.maven.org/maven2/org/apache/calcite/avatica/avatica/1.9.0/avatica-1.9.0.jar /sqlline/lib/
COPY avatica-1.10.0-SNAPSHOT.jar /sqlline/lib/
ADD https://repo1.maven.org/maven2/sqlline/sqlline/1.2.0/sqlline-1.2.0.jar /sqlline/lib/
ADD https://repo1.maven.org/maven2/jline/jline/2.12/jline-2.12.jar /sqlline/lib/
ADD https://repo1.maven.org/maven2/org/slf4j/slf4j-simple/1.7.12/slf4j-simple-1.7.12.jar /sqlline/lib
ADD https://repo1.maven.org/maven2/org/slf4j/slf4j-api/1.7.12/slf4j-api-1.7.12.jar /sqlline/lib
COPY sqlline.sh /sqlline/
RUN chmod +x /sqlline/sqlline.sh

ENTRYPOINT ["/sqlline/sqlline.sh"]
# Default argument -- localhost doesn't work...
# CMD ["http://localhost:8765"]
