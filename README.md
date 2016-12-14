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
$ docker run -it sqlline:1 http://$(hostname):8443
```

## With Knox

```
$ docker run -v $(pwd)/truststores:/truststores -it sqlline:1 "https://$(hostname):8443/gateway/sandbox/avatica/" /truststores/knox.jks <truststore_secret>
```
