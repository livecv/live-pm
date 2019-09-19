import sys
import os
import getopt
import json
import shutil
import argparse

from livepm.lib.command import Command
from livepm.lib.configuration import Configuration

class ListCommand(Command):

    name = 'list'
    description = 'List of installed packages'

    def __init__(self):
        
        pass

    def parse_args(self, argv):

        parser = argparse.ArgumentParser(description='List all packages')

        args = parser.parse_args(argv)

        self.livekeys_dir = os.path.join(os.environ['LIVEKEYS_DIR'], 'plugins')
        self.current_dir = os.path.join(os.getcwd(), 'packages')

    def __call__(self):

        # list packages from livekeys_dir
        try:

            livekeys_dir_list = os.listdir(self.livekeys_dir)

            if livekeys_dir_list:
                
                for i in livekeys_dir_list:
                    pluginPath = os.path.join(self.livekeys_dir, i)
                    with open(os.path.join(pluginPath, "live.package.json")) as livePackages:
                        data = json.load(livePackages)
                        print('Global:', '\n')
                        print('\t','>> ' + data['name'] + '-' + data['version'])
            
            else:

                print('No global packages found.')
        
        except:

            print(self.livekeys_dir + ' not found.')
            pass

        # list packages from current dir
        try:

            current_dir_list = os.listdir(self.current_dir)

            if current_dir_list:
                
                for i in current_dir_list:
                    pluginPath = os.path.join(self.current_dir, i)
                    with open(os.path.join(pluginPath, "live.package.json")) as livePackages:
                        data = json.load(livePackages)
                        print('Local:', '\n')
                        print('\t','>> ' + data['name'] + '-' + data['version'])
            
            else:

                print('No packages found.')
        
        except:

            print(self.current_dir + ' not found.')

                


    
            
               