#!/bin/bash

# Make this configurable, tied to the embedded ldap from knox..
URL="$1"
TRUSTSTORE="$2"
TRUSTSTORE_PASSWORD="$3"
JDBC_URL="jdbc:avatica:remote:url=${URL};serialization=PROTOBUF;avatica_user=guest;avatica_password=guest-password;authentication=BASIC"
if [[ ! -z "${TRUSTSTORE}" ]]; then
  JDBC_URL="${JDBC_URL};truststore=${TRUSTSTORE};truststore_password=${TRUSTSTORE_PASSWORD}"
fi
exec "/usr/lib/jvm/java-8-openjdk-amd64/bin/java" "-cp" "/sqlline/lib/*" "sqlline.SqlLine" "-d" "org.apache.calcite.avatica.remote.Driver" "-u" "${JDBC_URL}" "-n" "SCOTT" "-p" "TIGER" "--color=true" "--fastConnect=true" "--incremental=false" "--isolation=TRANSACTION_READ_COMMITTED"
