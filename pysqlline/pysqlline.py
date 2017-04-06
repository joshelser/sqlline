#!/usr/bin/env python

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

import argparse
import subprocess

class PySqlline(object):
    # Constants
    SQLLINE_CLASS='sqlline.SqlLine'
    TRANSACTION_LEVELS=('TRANSACTION_NONE', 'TRANSACTION_READ_COMMITTED',
        'TRANSACTION_READ_UNCOMMITTED', 'TRANSACTION_REPEATABLE_READ', 'TRANSACTION_SERIALIZABLE')
    DEFAULT_TRANSACTION_LEVEL='TRANSACTION_NONE'
    OUTPUT_FORMATS=('table', 'vertical', 'csv', 'tsv')

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Launches a Sqlline instance.')
        self.addArguments(self.parser)

    def addArguments(self, parser):
        """Adds Sqlline command-line arguments to the provided parser"""
        # Required SqlLine arguments
        parser.add_argument('url', help='JDBC URL')
        parser.add_argument('-d', '--driver', help='Class name of the JDBC Driver', required=True)

        # Optional SqlLine arguments
        parser.add_argument('-c', '--color', help='Color setting for sqlline.', default=True, type=bool)
        parser.add_argument('-f', '--file', help='Path to a file of SQL commands to execute', default=None)
        parser.add_argument('-n', '--name', help='JDBC database user', default=None)
        parser.add_argument('-p', '--password', help='JDBC database password', default=None)
        parser.add_argument('-v', '--verbose', help='Verbosity on sqlline.', default=True, type=bool)
        parser.add_argument('--auto-commit', help='Enables automatic transaction commit', default=None, type=bool)
        parser.add_argument('--auto-save', help='Automatically save preferences', default=None, type=bool)
        parser.add_argument('--fast-connect', help='Fetch all schemas on initial connection', default=False, type=bool)
        parser.add_argument('--force', help='Continue to execute the provided script after errors', default=False, type=bool)
        parser.add_argument('--header-interval', help='The interval between which headers are displayed', default=None, type=int)
        parser.add_argument('--incremental', help='Incrementally fetch rows', default=False, type=bool)
        parser.add_argument('--isolation', help='The transaction isolation level', default=PySqlline.DEFAULT_TRANSACTION_LEVEL, choices=PySqlline.TRANSACTION_LEVELS)
        parser.add_argument('--max-width', help='The maximum width of the terminal', default=None, type=int)
        parser.add_argument('--max-column-width', help='The maximum width to use when displaying columns', default=None, type=int)
        parser.add_argument('--number-format', help='DecimalFormat pattern to format numbers', default=None)
        parser.add_argument('--output-format', help='Format mode for result display', default=None, choices=PySqlline.OUTPUT_FORMATS)
        parser.add_argument('--show-header', help='Display the column names in query results', default=None, type=bool)
        parser.add_argument('--show-nested-errors', help='Display nested errors', default=None, type=bool)
        parser.add_argument('--show-time', help='Display execution time when verbose', default=None, type=bool)
        parser.add_argument('--show-warnings', help='Display connection warnings', default=None, type=bool)
        parser.add_argument('--silent', help='Be more silent', default=None, type=bool)

        # Environment-specific
        parser.add_argument('--classpath', help='Classpath for SqlLine', default=None)
        parser.add_argument('--java', help='Java command', default='/usr/bin/java')

    def getUrl(self, args):
        return args.url

    def getCommand(self, args):
        """Converts the command-line arguments into a list representing the Java Sqlline command to be executed"""
        cmd=[args.java]
        if args.classpath:
            cmd.extend(['-cp', args.classpath])

        # Require arguments to sqlline
        cmd.extend([PySqlline.SQLLINE_CLASS, '-d', args.driver, '-u', self.getUrl(args)])

        # All of the provided optional arguments
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

        return cmd

    def run(self):
        """Parses the arguments, creates a Java command, and executes that command"""
        # Parse the args
        args = self.parser.parse_args()
        command = self.getCommand(args)
        print 'Executing: ' + ' '.join(command)
        subprocess.call(command)

if __name__ == '__main__':
    PySqlline().run()
