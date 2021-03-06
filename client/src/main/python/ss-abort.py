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

from slipstream.CommandBase import CommandBase
from slipstream.Client import Client
from slipstream.ConfigHolder import ConfigHolder
from slipstream.NodeDecorator import NodeDecorator


class MainProgram(CommandBase):
    '''A command-line program to set the abort key/value pair in the info sys
    restlet.'''

    def __init__(self, argv=None):
        self.reason = None
        self.cancel = False
        super(MainProgram, self).__init__(argv)

    def parse(self):
        usage = '''usage: %prog [options] [<reason>]

<reason>         Reason for abort.'''

        self.parser.usage = usage

        self.parser.add_option('--cancel', dest='ignoreAbort',
                               help='cancel the abort status',
                               default=False, action='store_true')

        self.options, self.args = self.parser.parse_args()

        self._checkArgs()

        self.reason = (len(self.args) and self.args[0]) or None

    def _checkArgs(self):
        if len(self.args) > 1:
            self.usageExitTooManyArguments()

    def doWork(self):
        configHolder = ConfigHolder(self.options)
        client = Client(configHolder)
        client.setRuntimeParameter(NodeDecorator.ABORT_KEY, self.reason)

if __name__ == "__main__":
    try:
        MainProgram()
    except KeyboardInterrupt:
        print('\n\nExecution interrupted by the user... goodbye!')
        sys.exit(-1)

