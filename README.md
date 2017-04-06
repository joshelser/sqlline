# Docker container for Sqlline

[Sqlline](https://github.com/julianhyde/sqlline) is a command-line shell for issuing SQL to
relational databases via JDBC. This project consists of a Python module (pysqlline) which
encapsulates standard command-line access to invoking Sqlline, packaged as a Docker container.

This Docker container is flexible enough to be used with any JDBC driver packaged in a JAR.

## Pulling the image

First, pull the latest version of the sqlline Docker container.

```bash
$ docker pull joshelser/sqlline
```

From this point, there are two options to use the Docker image

### Mapping the JDBC driver into the Docker container

The Docker volumes feature can be used to provide the jar containing the JDBC driver into the
Docker container. For example, a JAR located on the host machine at `/home/user/my_jdbc_driver/my_jdbc_driver.jar`
can be exposed as follows to the Docker container:

```bash
$ docker run --rm -v /home/user/my_jdbc_driver/:/my_jdbc_driver -it joshelser/sqlline [...]
```

### Creating a new Docker container

Similarly, a new Docker container can be created, using this one as the base image:

```bash
$ cat <<EOF > Dockerfile
FROM joshelser/sqlline

RUN mkdir /my_database_jars
ADD http://FQDN.com/path/to/my_jdbc_driver.jar /my_database_jars/

CMD ["--classpath", "/sqlline/lib/*:/my_database_jars/*"]
EOF
```

## Usage for `pysqlline.py`

These are the full list of arguments that you can pass to pysqlline.

```
usage: pysqlline.py [-h] -d DRIVER [-c COLOR] [-f FILE] [-n NAME]
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
                    [--silent SILENT] [--classpath CLASSPATH] [--java JAVA]
                    url
```

## Example usage

[Apache Avatica](https://calcite.apache.org/avatica/) provides a database-agnostic JDBC driver which
makes it extremely re-usable which this Docker image.

For example, conside the following usage for the Avatica JDBC driver with this Docker image:

```bash
$ docker run --rm -v /home/user/.m2/repository/org/apache/calcite/avatica/avatica/1.10.0/:/avatica \
    -it joshelser/sqlline --classpath '/sqlline/lib/*:/avatica/avatica-1.10.0.jar' \
    -d org.apache.calcite.avatica.remote.Driver -n user -p password \
    'jdbc:avatica:remote:url=http://$(hostname -f):8765;SERIALIZATION=PROTOBUF'
```

The above approach is applicable to any JDBC driver.
