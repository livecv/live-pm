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

class ShowCommand(Command):

    name = 'show'
    description = 'Shows location and version of installed package'

    def __init__(self):
        
        pass

    def parse_args(self, argv):

        parser = argparse.ArgumentParser(description='Search for a live package')
        parser.add_argument('name', default=None, nargs='?', help='Name of the package')
            
        args = parser.parse_args(argv)
        self.name  = args.name

    def __call__(self):

        try:
            if os.environ['LIVEKEYS_DIR']:
                
                lkeysDir = os.path.join(os.environ["LIVEKEYS_DIR"], 'plugins')

        except KeyError:
            
            print("Enviroment variable LIVEKEYS_DIR not set.")
            pass

        try:

            localDir = os.path.join(os.getcwd(), 'packages')
            
        except:
            
            print('Local packages not found.')
            sys.exit(1)
        
        try:
            
            for package in os.listdir(lkeysDir):

                if package.startswith(self.name):
  
                    path = os.path.join(lkeysDir, package)
                    package_path = os.path.join(path, "live.package.json")

                    if ( os.path.exists(package_path) ):
                        with open(os.path.join(path,"live.package.json")) as livePackages:
                            data = json.load(livePackages)
                            print('>> ' + data['name'] + ' version: ' + data['version'] + ' in ' + path)
        except:

            pass
        
        try:
            
            for package in os.listdir(localDir):

                if package.startswith(self.name):
                
                    path = os.path.join(localDir, package)
                    package_path = os.path.join(path, "live.package.json")

                    if ( os.path.exists(package_path) ):
                        with open(os.path.join(path,"live.package.json")) as livePackages:
                            data = json.load(livePackages)
                            print('>> ' + data['name'] + ' version: ' + data['version'] + ' in ' + path)

        except:

            sys.exit()

                        



        
     