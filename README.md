# SqlLine Docker image for Apache Avatica based servers

This is a collection of Docker images designed to provide access to
Apache Avatica based servers via the SQL shell SqlLine.

## Running

```
$ docker run -ti joshelser/sqlline "jdbc:avatica:remote:url=http://$(hostname):8765"
```

# Using the Apache Phoenix Query Server

```
$ docker run -ti joshelser/phoenix-sqlline "jdbc:avatica:remote:url=http://$(hostname):8765"
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
