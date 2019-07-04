import sys
import os
import getopt
import json
import shutil
import argparse
import requests as re
import urllib.parse
import zipfile
import platform
from columnar import columnar

from livepm.lib.command import Command
from livepm.lib.configuration import Configuration

server_url = "https://livekeys.io/api/"

class DependenciesCommand(Command):

    name = 'dependencies'
    description = 'Search for a live package dependencies'

    def __init__(self):
        
        pass

    def parse_args(self, argv):

        parser = argparse.ArgumentParser(description='Search for a live package dependencies')
        parser.add_argument('name',default=None, help='Package name')
        parser.add_argument('--version', '-v', nargs='?', help='Package version')
        parser.add_argument('--dev', '-d', default=False, action='store_true', help='Dependencies for dev packages')
        parser.add_argument('--server_url', '-sU', default=server_url, help='Change server url.')
            
        args = parser.parse_args(argv)

        self.name  = args.name
        self.version = args.version
        self.server_url = args.server_url
        self.dev = args.dev

        # OS check
        if platform.system() == 'Linux':

            self.release = 'linux'

        elif platform.system() == 'Darwin':

            self.release = 'macos'

        elif platform.system() == 'Windows':

            self.release = 'win'

        # Check if dev package is requested
        if args.dev:

            self.release = self.release + '-' + 'dev'
            
        else:

            pass

    def __call__(self):

        # Url construction
        # In case package version is specified
        if self.version:

            urlParams = 'package/' + self.name + '/release/' + self.version + '/' + self.release

        else:

            urlParams = 'package/' + self.name + '/' + 'latest/' + self.release
        
        url = urllib.parse.urljoin(self.server_url, urlParams)

        # Send request
        r = re.get(url, allow_redirects=True)

        # Check if the package exist
        if not r.ok:

            # in case of dev release
            if self.dev:

                print('Package ' + self.name + ' development release' + ' not found.')

                # sys.exit(1)

            else:

                print('Package ' + self.name + ' not found.')

            sys.exit(1)
        else:
            
            pass

        jsonResponse = json.loads(r.text)

        # Check if the package has dependencies
        try:

            jsonResponse['dependencies']

        except KeyError:
            
            print('Package ' + self.name + ' has no dependencies.')
            sys.exit(1)

        dependencies = jsonResponse['dependencies']

        for package in dependencies:
                
            headers = [
                    
                'Package name',
                'Version',
                'Date'

                ]

            data = [

                [

                package['package']['name'],
                package['version'],
                package['createdAt']
          
                ]
            ]

            table = columnar(data, headers, no_borders=True)
            print(table)

