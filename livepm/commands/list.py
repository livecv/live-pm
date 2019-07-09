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
        
        # list packages livekeys_dir
        if os.listdir(self.livekeys_dir) and os.listdir(self.current_dir):
            
            for package in os.listdir(self.livekeys_dir):
                
                print('>> ' + package)
                
        # list packages current dir
        elif os.listdir(self.current_dir):
            
            for package in os.listdir(self.current_dir):

                print('>> ' + package)

        else:

            print('No packages found.')
                
