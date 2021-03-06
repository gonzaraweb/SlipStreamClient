#!/usr/bin/env python
"""
 SlipStream Client
 =====
 Copyright (C) 2013 SixSq Sarl (sixsq.com)
 =====
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
from __future__ import print_function

import sys
import os

from slipstream.CommandBase import CommandBase
from slipstream.HttpClient import HttpClient
import slipstream.util as util
import slipstream.SlipStreamHttpClient as SlipStreamHttpClient

default_endpoint = os.environ.get('SLIPSTREAM_ENDPOINT',
                                  'http://slipstream.sixsq.com')
default_cookie = os.environ.get('SLIPSTREAM_COOKIEFILE',
                                os.path.join(util.TMPDIR, 'cookie'))


class MainProgram(CommandBase):
    '''A command-line program to create/update user definition(s).'''

    def __init__(self, argv=None):
        self.user = None
        self.username = None
        self.password = None
        self.cookie = None
        self.endpoint = None
        super(MainProgram, self).__init__(argv)

    def parse(self):
        usage = '''usage: %prog [options] <file>

<file>    XML file to create/update the user.
          For an example look at the ss-user-get output.'''

        self.parser.usage = usage

        self.parser.add_option('-u', '--username', dest='username',
                               help='SlipStream username', metavar='USERNAME',
                               default=os.environ.get('SLIPSTREAM_USERNAME'))
        self.parser.add_option('-p', '--password', dest='password',
                               help='SlipStream password', metavar='PASSWORD',
                               default=os.environ.get('SLIPSTREAM_PASSWORD'))

        self.parser.add_option('--cookie', dest='cookieFilename',
                               help='SlipStream cookie', metavar='FILE',
                               default=default_cookie)

        self.parser.add_option('--endpoint', dest='endpoint',
                               help='SlipStream server endpoint', metavar='URL',
                               default=default_endpoint)

        self.options, self.args = self.parser.parse_args()

        self._checkArgs()

    def _checkArgs(self):

        if len(self.args) == 1:
            self.user = self.read_input_file(self.args[0])
        else:
            self.usageExitWrongNumberOfArguments()

    def doWork(self):
        client = HttpClient(self.options.username, self.options.password)
        client.verboseLevel = self.verboseLevel

        dom = self.read_xml_and_exit_on_error(self.user)
        if not dom.tag in ('user'):
            sys.stderr.write('Invalid xml\n')
            sys.exit(-1)

        dom = self.read_xml_and_exit_on_error(self.user)
        attrs = SlipStreamHttpClient.DomExtractor.getAttributes(dom)

        user = attrs['name']
        uri = util.USER_URL_PATH + '/' + user

        url = self.options.endpoint + uri

        client.put(url, self.user)

if __name__ == "__main__":
    try:
        MainProgram()
    except KeyboardInterrupt:
        print('\n\nExecution interrupted by the user... goodbye!')
        sys.exit(-1)
