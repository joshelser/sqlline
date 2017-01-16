FROM openjdk:8-jre
RUN apt-get update && apt-get install -y python
RUN mkdir -p /sqlline/lib
#ADD https://repo1.maven.org/maven2/org/apache/calcite/avatica/avatica/1.9.0/avatica-1.9.0.jar /sqlline/lib/
COPY avatica-1.10.0-SNAPSHOT.jar /sqlline/lib/
ADD https://repo1.maven.org/maven2/sqlline/sqlline/1.2.0/sqlline-1.2.0.jar /sqlline/lib/
ADD https://repo1.maven.org/maven2/jline/jline/2.14.2/jline-2.14.2.jar /sqlline/lib/
ADD https://repo1.maven.org/maven2/org/slf4j/slf4j-simple/1.7.22/slf4j-simple-1.7.22.jar /sqlline/lib
ADD https://repo1.maven.org/maven2/org/slf4j/slf4j-api/1.7.22/slf4j-api-1.7.22.jar /sqlline/lib

COPY sqlline.py /sqlline/
RUN chmod +x /sqlline/sqlline.py
ENTRYPOINT ["/sqlline/sqlline.py", "--classpath", "/sqlline/lib/*"]

# Default argument -- localhost doesn't work...
# CMD ["http://localhost:8765"]
