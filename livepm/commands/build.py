import sys
import os
import getopt
import json
import shutil
import argparse

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
        parser.add_argument('package_path', default='', help="Path to a livecv package or package file.")
        parser.add_argument('release_id', default='', help="Id of release.")

        args = parser.parse_args(argv)

        self.package_file = Configuration.findpackage(os.path.abspath(args.package_path))
        self.release_id   = args.release_id
        self.source_dir   = args.source if args.source else os.path.dirname(self.package_file)
        self.build_dir    = args.build if args.build else self.source_dir + '/build'

        self.source_dir = os.path.abspath(self.source_dir)

    def __call__(self):

        print('\nParsing build file \'' + self.package_file + '\'...')

        with open(self.package_file) as jsonfile:
            packagejson = json.load(jsonfile)

        self.config = Configuration(packagejson)
        if ( not self.config.has_release(self.release_id) ):
            raise Exception("Failed to find release id:" + self.release_id)

        self.release = self.config.release(self.release_id)

        print('\nConfiguration found: ' + self.release_id)

        self.build_dir = self.build_dir + '/' + self.release.compiler

        print('  Modules:')
        for key, value in self.config.components.items():
            print('   * ' + str(value))

        print('  Dependencies:')
        for value in self.config.dependencies:
            print('   * ' + str(value))

        print('  Source dir: \'' + self.source_dir + '\'')
        print('  Release dir: \'' + self.build_dir + '\'')
        print('  Compiler: \'' + self.release.compiler + '\'')

        self.release.init_environment()
        print('  Environment:')
        for key, value in self.release.environment.items():
            print('   * ' + key + ':\'' + os.environ[key] + '\'')

        print('\nCleaning release dir: \'' + self.build_dir + '\'')
        if ( os.path.isdir(self.build_dir) ):
            shutil.rmtree(self.build_dir)
        os.makedirs(self.build_dir)

        if ( len(self.config.dependencies) > 0 ):
            print('\nSolving dependencies:')
            for depends in self.config.dependencies:
                print('\n --------------------- ' + str(depends) + ' --------------------- \n')
                depends(self.source_dir, self.build_dir, self.release_id)
                builder = Build(depends.repodir, self.release_id)
                builder.releasedir = depends.releasedir
                builder(depends.repodir, depends.releasedir, options)

                for value in self.release.buildsteps:
                    if ( value.name == 'qmake' ):
                        value.options = [
                            "BUILD_DEPENDENCIES=false",
                            "LIVECV_BIN_PATH=\'" + depends.releasedir + "/bin\'",
                            "DEPLOY_PATH=\'" + self.build_dir + "/bin\'"
                        ]

        print('\nExecuting build steps:')

        for value in self.release.buildsteps:
            print('\n *** ' + str(value) + ' *** \n')
            value(self.source_dir, self.build_dir, os.environ)

