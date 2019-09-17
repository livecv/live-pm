import sys
import os
import getopt
import json
import shutil
import argparse
import requests as re
import urllib.parse
from columnar import columnar
import platform

from livepm.lib.command import Command
from livepm.lib.configuration import Configuration

server_url = "https://livekeys.io/api/"

class RemoteShowCommand(Command):

    name = 'remote-show'
    description = 'Show information about the package that is not installed.'

    def __init__(self):
        
        pass

    def parse_args(self, argv):

        parser = argparse.ArgumentParser(description='Show information about the package that is not installed.')
        parser.add_argument('name', nargs='?', help='Package name')
        parser.add_argument('--server_url', '-sU', default=server_url, help='Change server url.')
            
        args = parser.parse_args(argv)

        self.name  = args.name
        self.server_url = args.server_url

    
        # Get the os for release extension
        if platform.system() == 'Linux':
            self.release = 'linux'

        elif platform.system() == 'Darwin':

            self.release = 'macos'

        elif platform.system() == 'Windows':

            self.release = 'win'


    def __call__(self):
        
        # Construct url
        urlParams = 'package/' + self.name + '/' + 'latest/' + self.release
        url = urllib.parse.urljoin(self.server_url, urlParams)

        # Check url and send request
        try:

            r = re.get(url, allow_redirects=True)
            jsonResponse = json.loads(r.text)

        # throw an error if url is not valid
        except:

            print('Invalid url.')
            sys.exit(1)

        try:

            print(self.name + ' version: ' + jsonResponse['version'][:-4], '\n')
            print('Dependencies:', '\n')
            
            for package in jsonResponse['dependencies']:

                print('\t','*',package['package']['name'], 'version ', package['version'][:-4])

        # throw an error if version is not found.           
        except:

            print(self.name + ' not found.')
            sys.exit(1)
