# Copyright 2017 Josh Elser
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM openjdk:8-jre-alpine
RUN apk add --update \
    python \
    python-dev \
    build-base \
  && rm -rf /var/cache/apk/*

ARG SQLLINE_VERSION="1.2.0"
ARG SLF4J_VERSION="1.7.22"

RUN mkdir -p /sqlline/
ADD https://repo1.maven.org/maven2/sqlline/sqlline/${SQLLINE_VERSION}/sqlline-${SQLLINE_VERSION}-jar-with-dependencies.jar /sqlline/lib/
ADD https://repo1.maven.org/maven2/org/slf4j/slf4j-simple/${SLF4J_VERSION}/slf4j-simple-${SLF4J_VERSION}.jar /sqlline/lib/
ADD https://repo1.maven.org/maven2/org/slf4j/slf4j-api/${SLF4J_VERSION}/slf4j-api-${SLF4J_VERSION}.jar /sqlline/lib/
ADD pysqlline /sqlline/pysqlline

RUN chmod +x /sqlline/pysqlline/pysqlline.py

# TODO Wish we could do this, but it breaks people using this image as a base image
# USER sqlline
# RUN addgroup -S sqlline && adduser -S -G sqlline sqlline
# RUN chown -R sqlline: /sqlline

ENTRYPOINT ["/sqlline/pysqlline/pysqlline.py"]
