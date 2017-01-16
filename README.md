# SqlLine Docker image for Apache Avatica based servers

This is a collection of Docker images designed to provide access to
Apache Avatica based servers via the SQL shell SqlLine.

## Running

```
$ docker pull joshelser/sqlline
$ docker run -ti joshelser/sqlline "jdbc:avatica:remote:url=http://$(hostname):8765"
```

# Using the Apache Phoenix Query Server

```
$ docker pull joshelser/phoenix-thin-sqlline
$ docker run -ti joshelser/phoenix-thin-sqlline "jdbc:avatica:remote:url=http://$(hostname):8765"
```

# Customizing for other Avatica-based servers

Create your own Dockerfile, extending `joshelser/sqlline`, adding any necessary jars to the image
and ensuring that the jars are added to the classpath.

```
From joshelser/sqlline

ADD https://repo1.maven.org/maven2/org/apache/phoenix/phoenix-queryserver-client/4.9.0-HBase-1.2/phoenix-queryserver-client-4.9.0-HBase-1.2.jar /sqlline/lib

ENTRYPOINT ["/sqlline/sqlline.py", "--classpath", "/sqlline/lib/*"]
```

Then, build the image

```
$ docker build . -t joshelser/custom-sqlline
```

And run it per the other examples

```
$ docker run -t joshelser/custom-sqlline "jdbc:avatica:remote:url=http://$(hostname):8765"
```

# Usage for `sqlline.py`

These are the full list of arguments that you can pass to the above docker containers.

```
usage: sqlline.py [-h] [-c COLOR] [-d DRIVER] [-f FILE] [-n NAME]
                  [-p PASSWORD] [-v VERBOSE] [--auto-commit AUTO_COMMIT]
                  [--auto-save AUTO_SAVE] [--fast-connect FAST_CONNECT]
                  [--force FORCE] [--header-interval HEADER_INTERVAL]
                  [--incremental INCREMENTAL]
                  [--isolation {TRANSACTION_NONE,TRANSACTION_READ_COMMITTED,TRANSACTION_READ_UNCOMMITTED,TRANSACTION_REPEATABLE_READ,TRANSACTION_SERIALIZABLE}]
                  [--max-width MAX_WIDTH]
                  [--max-column-width MAX_COLUMN_WIDTH]
                  [--number-format NUMBER_FORMAT]
                  [--output-format {table,vertical,csv,tsv}]
                  [--show-header SHOW_HEADER]
                  [--show-nested-errors SHOW_NESTED_ERRORS]
                  [--show-time SHOW_TIME] [--show-warnings SHOW_WARNINGS]
                  [--silent SILENT] [--avatica-user AVATICA_USER]
                  [--avatica-password AVATICA_PASSWORD]
                  [--avatica-authentication {SPNEGO,DIGEST,BASIC,NONE}]
                  [--avatica-serialization {PROTOBUF,JSON}]
                  [--avatica-truststore AVATICA_TRUSTSTORE]
                  [--avatica-truststore-password AVATICA_TRUSTSTORE_PASSWORD]
                  [--classpath CLASSPATH] [--java JAVA]
                  url
```

Custom containers can also be created which automatically provide some of these options
for a "familiar" experience with a simple command.

# Using Apache Knox with Avatica (out-dated)

## Prerequisite: Start Knox and Avatica 

```
$ git clone https://github.com/joshelser/knox-dev-docker/ && cd knox-dev-docker
$ docker-compose -f docker-compose-avatica.yml up -d
```

## Create the truststore

```
$ cd ../avatica-sqlline.git
$ openssl s_client -showcerts -connect localhost:8443  </dev/null
$ <copy BEGIN CERTIFICATE to END CERTIFICATE to knox.cer>
$ keytool -import -keystore ~/knox.jks -file ~/knox.cer -alias knox
$ cp ~/knox.jks truststores/
```

## Build the container

```
$ docker build . -t sqlline:1
```

## No Knox

```
$ docker run -it sqlline:1 http://$(hostname):8765
```

## With Knox

```
$ docker run -v $(pwd)/truststores:/truststores -it sqlline:1 "https://$(hostname):8443/gateway/sandbox/avatica/" /truststores/knox.jks <truststore_secret>
```
