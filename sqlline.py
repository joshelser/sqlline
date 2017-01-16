#!/usr/bin/env python

import argparse
import subprocess

def update_url(orig_url, args):
    url_array = [orig_url]
    if args.avatica_user and 'avatica_user' not in orig_url:
        url_array.append('avatica_user=' + args.avatica_user)
    if args.avatica_password and 'avatica_password' not in orig_url:
        url_array.append('avatica_password=' + args.avatica_password)
    if args.avatica_authentication and 'authentication' not in orig_url:
        url_array.append('authentication=' + args.avatica_authentication)
    if args.avatica_serialization and 'serialization' not in orig_url:
        url_array.append('serialization=' + args.avatica_serialization)
    if args.avatica_truststore and 'truststore' not in orig_url:
        url_array.append('truststore=' + args.avatica_truststore)
    if args.avatica_truststore_password and 'truststore_password' not in orig_url:
        url_array.append('truststore_password=' + args.avatica_truststore_password)
    return ';'.join(url_array)

# Constants
SQLLINE_CLASS='sqlline.SqlLine'

TRANSACTION_LEVELS=('TRANSACTION_NONE', 'TRANSACTION_READ_COMMITTED',
    'TRANSACTION_READ_UNCOMMITTED', 'TRANSACTION_REPEATABLE_READ', 'TRANSACTION_SERIALIZABLE')
DEFAULT_TRANSACTION_LEVEL='TRANSACTION_NONE'
OUTPUT_FORMATS=('table', 'vertical', 'csv', 'tsv')

AVATICA_RPC_AUTHENTICATION=('SPNEGO', 'DIGEST', 'BASIC', 'NONE')
DEFAULT_AVATICA_RPC_AUTHENTICATION='NONE'

AVATICA_RPC_SERIALIZATION=('PROTOBUF', 'JSON')
DEFAULT_AVATICA_RPC_SERIALIZATION='PROTOBUF'

parser = argparse.ArgumentParser(description='Launches an Avatica JDBC connection.')

# Required SqlLine arguments
parser.add_argument('url', help='JDBC URL')

# Optional SqlLine arguments
parser.add_argument('-c', '--color', help='Color setting for sqlline.', default=True, type=bool)
parser.add_argument('-d', '--driver', help='Class name of the JDBC Driver',
        default='org.apache.calcite.avatica.remote.Driver')
parser.add_argument('-f', '--file', help='Path to a file of SQL commands to execute', default=None)
parser.add_argument('-n', '--name', help='JDBC database user', default=None)
parser.add_argument('-p', '--password', help='JDBC database password', default=None)
parser.add_argument('-v', '--verbose', help='Verbosity on sqlline.', default=True, type=bool)
parser.add_argument('--auto-commit', help='Enables automatic transaction commit', default=None,
        type=bool)
parser.add_argument('--auto-save', help='Automatically save preferences', default=None,
        type=bool)
parser.add_argument('--fast-connect', help='Fetch all schemas on initial connection', default=False,
        type=bool)
parser.add_argument('--force', help='Continue to execute the provided script after errors',
        default=False, type=bool)
parser.add_argument('--header-interval', help='The interval between which headers are displayed',
        default=None, type=int)
parser.add_argument('--incremental', help='Incrementally fetch rows', default=False, type=bool)
parser.add_argument('--isolation', help='The transaction isolation level',
        default=DEFAULT_TRANSACTION_LEVEL, choices=TRANSACTION_LEVELS)
parser.add_argument('--max-width', help='The maximum width of the terminal', default=None, type=int)
parser.add_argument('--max-column-width', help='The maximum width to use when displaying columns',
        default=None, type=int)
parser.add_argument('--number-format', help='DecimalFormat pattern to format numbers', default=None)
parser.add_argument('--output-format', help='Format mode for result display', default=None,
        choices=OUTPUT_FORMATS)
parser.add_argument('--show-header', help='Display the column names in query results', default=None,
        type=bool)
parser.add_argument('--show-nested-errors', help='Display nested errors', default=None, type=bool)
parser.add_argument('--show-time', help='Display execution time when verbose', default=None,
        type=bool)
parser.add_argument('--show-warnings', help='Display connection warnings', default=None,
        type=bool)
parser.add_argument('--silent', help='Be more silent', default=None, type=bool)

# Avatica-specific
parser.add_argument('--avatica-user', help='Avatica RPC username', default=None)
parser.add_argument('--avatica-password', help='Avatica RPC password', default=None)
parser.add_argument('--avatica-authentication', help='Avatica RPC authentication',
        default=DEFAULT_AVATICA_RPC_AUTHENTICATION, choices=AVATICA_RPC_AUTHENTICATION)
parser.add_argument('--avatica-serialization', help='Avatica RPC serialization',
        default=DEFAULT_AVATICA_RPC_SERIALIZATION, choices=AVATICA_RPC_SERIALIZATION)
parser.add_argument('--avatica-truststore', help='Avatica RPC SSL truststore', default=None)
parser.add_argument('--avatica-truststore-password', help='Avatica RPC SSL truststore password',
        default=None)

# Environment-specific
parser.add_argument('--classpath', help='Classpath for SqlLine', default=None)
parser.add_argument('--java', help='Java command', default='/usr/bin/java')

# Parse the args
args=parser.parse_args()

cmd=[args.java]
if args.classpath:
    cmd.extend(['-cp', args.classpath])

# Append in the avatica options to the JDBC url
url = update_url(args.url, args)

# Require arguments to sqlline
cmd.extend([SQLLINE_CLASS, '-d', args.driver, '-u', url])

if args.name:
    cmd.extend(['-n', args.name])

if args.password:
    cmd.extend(['-p', args.password])

if args.file:
    cmd.extend(['-f', args.file])

if args.color is not None:
    cmd.append('--color=' + str(args.color).lower())

if args.verbose is not None:
    cmd.append('--verbose=' + str(args.verbose).lower())

if args.auto_commit is not None:
    cmd.append('--autoCommit=', str(args.auto_commit).lower())

if args.auto_save is not None:
    cmd.append('--autosave==' + str(args.auto_save).lower())

if args.fast_connect is not None:
    cmd.append('--fastConnect==' + str(args.fast_connect).lower())

if args.force is not None:
    cmd.append('--force=' + str(args.force).lower())

if args.header_interval:
    cmd.append('--headerInterval=' + str(args.header_interval))

if args.incremental is not None:
    cmd.append('--incremental=' + str(args.incremental).lower())

if args.isolation:
    cmd.append('--isolation=' + args.isolation)

if args.max_width:
    cmd.append('--maxWidth=' + str(args.max_width))

if args.max_column_width:
    cmd.append('--maxColumnWidth=' + str(args.max_column_width))

if args.number_format:
    cmd.append('--numberFormat=' + args.number_format)

if args.output_format:
    cmd.append('--outputformat=' + args.output_format)

if args.show_header is not None:
    cmd.append('--showHeader=' + str(args.show_header).lower())

if args.show_nested_errors is not None:
    cmd.append('--showNestedErrs=' + str(args.show_nested_errors).lower())

if args.show_time is not None:
    cmd.append('--showTime=' + str(args.show_time).lower())

if args.show_warnings is not None:
    cmd.append('--showWarnings=' + str(args.show_warnings).lower())

if args.silent is not None:
    cmd.append('--silent=' + str(args.silent).lower())

print ' '.join(cmd)
subprocess.call(cmd)
