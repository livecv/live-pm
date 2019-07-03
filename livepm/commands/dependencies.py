import sys
import os
import getopt
import json
import shutil
import argparse
import requests as re
import urllib.parse
import zipfile
from columnar import columnar

from livepm.lib.command import Command
from livepm.lib.configuration import Configuration

server_url = "https://livekeys.io/api/"

class SearchDependencies(Command):

    name = 'dependencies'
    description = 'Search for a live package dependencies'

    def __init__(self):
        
        pass

    def parse_args(self, argv):

        parser = argparse.ArgumentParser(description='Search for a live package dependencies')
        parser.add_argument('--name', '-n', default=None, help='Package name')
        parser.add_argument('--release', '-r', default=None, help='Package release')
        parser.add_argument('--server_url', '-sU', default=server_url, help='Change server url.')
            
        args = parser.parse_args(argv)

        self.name  = args.name
        self.release = args.release
        self.server_url = args.server_url

    def __call__(self):
        
        # Url construction
        urlParams = 'package/' + self.name + '/' + 'latest/' + self.release
        url = urllib.parse.urljoin(self.server_url, urlParams)
        # Send request
        r = re.get(url, allow_redirects=True)

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

