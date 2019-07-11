import sys
import os
import getopt
import json
import shutil
import argparse

from livepm.lib.command import Command
from livepm.lib.configuration import Configuration

class UninstallCommand(Command):

    name = 'uninstall'
    description = 'Removes a package'

    def __init__(self):
        
        pass

    def parse_args(self, argv):

        parser = argparse.ArgumentParser(description='Removes a package')

        parser.add_argument('name', default=None, help='Name of the package')
        parser.add_argument('--uninstall_globally', '-g' ,default=False, action='store_true', help="Removes package from livekeys_dir")

        args = parser.parse_args(argv)

        self.glob = args.uninstall_globally
        self.name = args.name


        # Directory construction
        if args.uninstall_globally:

            try:

                if os.environ['LIVEKEYS_DIR']:

                    self.dir = os.environ["LIVEKEYS_DIR"]
                    self.folder = 'plugins'

            except KeyError:

                print("Enviroment variable LIVEKEYS_DIR not set.")
                sys.exit(1)
        else:

            try:

                self.dir = os.getcwd()
                self.folder = 'packages'
                os.listdir(os.path.join(self.dir, self.folder))
            
            except:

                print('Local packages not found.')
                sys.exit(1)

    def __call__(self):

        directory = os.path.join(self.dir, self.folder)

        # Check if plugins dir is empty
        if not os.listdir(directory):

                print('No packages found')

        else:
            
            for package in os.listdir(directory):

                # Check for specific packages and remove them
                if package.startswith(self.name):
                    
                    shutil.rmtree(os.path.join(directory, package))
                    
                    # Remove package from live.package.json
                    if os.path.exists(os.path.join(os.getcwd(), "live.packages.json")):
                        
                        with open(os.path.join(os.getcwd(),"live.packages.json")) as livePackages:
                            data = json.load(livePackages)

                            data['dependencies'].pop(self.name)

                        with open(os.path.join(os.getcwd(),"live.packages.json"),'w') as livePackages:
                            json.dump(data, livePackages, ensure_ascii=False, indent=4)

                    print('>> Package removed: ' + package)

                    exit()

                else:

                    print('Package ' + self.name + ' not found.') 


                   
