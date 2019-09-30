import sys
import os
import getopt
import json
import shutil
import argparse

from livepm.lib.builder import Builder
from livepm.lib.command import Command
from livepm.lib.configuration import Configuration

class BuildCommand(Command):
    name = 'build'
    description = 'Build a live package'

    def __init__(self):
        pass

    def parse_args(self, argv):
        parser = argparse.ArgumentParser(description = 'Build a live package.')
        parser.add_argument('--source', '-s', default=None, help='Path to source directory.')
        parser.add_argument('--options', '-o', default=None, help='Specific build options')
        parser.add_argument('--build', '-b', default='', help='Custom build directory. Default directory is build.')
        parser.add_argument('package_path', default='', help="Path to a livekeys package or package file.")
        parser.add_argument('release_id', default='', help="Id of release.")

        args = parser.parse_args(argv)

        self.package_file = Configuration.findpackage(os.path.abspath(args.package_path))
        self.release_id   = args.release_id
        self.source_dir   = args.source if args.source else os.path.dirname(self.package_file)
        self.build_dir    = args.build if args.build else self.source_dir + '/build'
        self.options      = args.options

        self.source_dir = os.path.abspath(self.source_dir)

    def __call__(self):
        b = Builder(self.package_file, self.release_id)
        b.deploy_to_livekeys = False
        b(self.source_dir, os.path.join(self.build_dir, b.release.compiler), self.options)
