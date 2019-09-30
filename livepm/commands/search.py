import sys
import os
import getopt
import json
import shutil
import argparse
import requests as re
import urllib.parse
from columnar import columnar

from livepm.lib.command import Command
from livepm.lib.configuration import Configuration

server_url = "https://livekeys.io/api/"

class SearchCommand(Command):

    name = 'search'
    description = 'Search for a live package'

    def __init__(self):
        
        pass

    def parse_args(self, argv):

        parser = argparse.ArgumentParser(description='Search for a live package')
        parser.add_argument('keyword', default=None, nargs='?', help='Search term')
        parser.add_argument('--server_url', '-sU', default=server_url, help='Change server url.')
            
        args = parser.parse_args(argv)

        self.keyword  = args.keyword
        self.server_url = args.server_url

    def __call__(self):
        
        # Url construction
        if not self.server_url.endswith('/'):
            self.server_url += '/'

        urlParams = 'package?search=' + self.keyword
        url = urllib.parse.urljoin(self.server_url, urlParams)
        
        r = re.get(url, allow_redirects=True)

        jsonResponse = json.loads(r.text)
        
        # Check if there is data for current search
        if jsonResponse['data']:

            headers = [
                
                'Package name',
                'Description',
                'Date',
                'Created by'

                ]

            data = []
                
            for item in jsonResponse['data']:

                data.append(

                    [

                    item['name'],
                    item['description'],
                    item['createdAt'],
                    item['user']['username'] if 'user' in item else ''
                        
                    ]
                )

            table = columnar(data, headers, no_borders=True)
            print(table)

        else:

            print("No match found for: " + self.keyword)
