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

        livekeys_dir_list = os.listdir(self.livekeys_dir)
        current_dir_list = os.listdir(self.current_dir)

        # list packages from livekeys_dir
        if livekeys_dir_list:

            print("Globally installed packages:\n")
            
            
            for package in livekeys_dir_list:
                
                print(' > ' + package)

        print("\nLocally installed packages:\n")

        # list packages from current dir
        if current_dir_list:

            for package in current_dir_list:

                print(' > ' + package)
            
               