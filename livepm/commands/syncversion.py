import os
import sys
import getopt
import json
import argparse

from livepm.lib.command import Command
from livepm.lib.configuration import Configuration

class SyncVersionCommand:
    name = 'syncversion'
    description = 'Sync version from a package file accross files.'

    def __init__(self):
        pass

    def parse_args(self, argv):
        parser = argparse.ArgumentParser(description=SyncVersionCommand.description)
        parser.add_argument('--source', '-s', default=None, help='Path to source directory')
        parser.add_argument('package_path', default='', help='Path to a livecv package or package file.')

        args = parser.parse_args(argv)

        self.package_file = Configuration.findpackage(os.path.abspath(args.package_path))
        self.source_dir   = args.source if args.source else os.path.dirname(self.package_file)
        self.source_dir   = os.path.abspath(self.source_dir)

    def __call__(self):
        print('\nParsing build file \'' + self.package_file + '\'...')

        with open(self.package_file) as jsonfile:
            packagejson = json.load(jsonfile)

        config = Configuration(packagejson)

        print('  Source dir: \'' + self.source_dir + '\'')
        print('  Modules:')
        for key, value in config.components.items():
            print('   * ' + str(value))
            version = value.version
            for versionfile, versionexp in value.versionsyncs.items():
                filepath = os.path.join(self.source_dir, versionfile)
                print('      > ' + 'Updating file \'' + filepath + '\' to version \'' + str(version) + '\'')
                version.savetofile(filepath, versionexp)

