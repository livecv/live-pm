import sys
import os
import argparse
from string import Template

from livepm.lib.command import Command
from livepm.lib.configuration import Configuration

class NewCommand(Command):
    name = 'new'
    description = 'Create elements within a package'

    def __init__(self):
        pass

    def parse_args(self, argv):
        parser = argparse.ArgumentParser(description = NewCommand.description)
        parser.add_argument('package_path', default = '', help="Path to the livecv package or package file")
