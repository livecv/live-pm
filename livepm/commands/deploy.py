import sys
import os
import getopt
import json
import shutil
import argparse

from livepm.lib.command import Command
from livepm.lib.configuration import Configuration

class DeployCommand(Command):
    name = 'deploy'
    description = 'Deploy and pack a live package'

    def __init__(self):
        pass

    def parse_args(self, argv):
        parser = argparse.ArgumentParser(description='Deploy a live package')
        parser.add_argument('--source', '-s', default=None, help='Path to source directory or package file.')
        parser.add_argument('--options', '-o', default=None, help='Specific deploy options.')
        parser.add_argument('--build', '-b', default=None, help='Custom build directory. Default directory is build.')
        parser.add_argument('package_path', default='', help="Path to a livecv package or package file.")
        parser.add_argument('release_id', default='', help="Id of release.")

        args = parser.parse_args(argv)

        self.package_file = Configuration.findpackage(os.path.abspath(args.package_path))
        self.release_id   = args.release_id
        self.source_dir   = args.source if args.source else os.path.dirname(self.package_file)
        self.build_dir    = args.build if args.build else self.source_dir + '/build'

        self.source_dir = os.path.abspath(self.source_dir)
        # usage = 'Usage: livecv_deploypy [-b <self.build_dir>] <buildfile> <self.release_id>'

    def __call__(self):

        print('\nParsing build file \'' + self.package_file + '\'...')

        with open(self.package_file) as jsonfile:
            packagejson = json.load(jsonfile)

        config = Configuration(packagejson)
        if ( not config.has_release(self.release_id) ):
            raise Exception("Failed to find release id:" + self.release_id)

        print('  Version:' + str(config.version))
        print('  Modules:')
        for key, value in config.components.items():
            print('   * ' + str(value))

        print('  Dependencies:')
        for value in config.dependencies:
            print('   * ' + str(value))

        release = config.release(self.release_id)
        releasedir = os.path.abspath(os.path.join(self.build_dir, release.compiler))

        print('\nConfiguration found: ' + self.release_id)
        print('  Source dir: \'' + self.source_dir + '\'')
        print('  Release dir: \'' + releasedir + '\'')
        print('  Compiler: \'' + release.compiler + '\'')

        release.init_environment()
        print('  Environment:')
        for key, value in release.environment.items():
            print('   * ' + key + '[' + value + ']: \'' + os.environ[key] + '\'')

        buildname = release.release_name()
        deploydir = os.path.abspath(releasedir + '/../' + buildname)
        releasename = release.name.replace('.', '-')

        deploydirroot = deploydir + '/' + releasename + '/'
        if releasename == 'livecv' and sys.platform.lower() == 'darwin':
            deploydirroot = deploydir + '/'

        print('\nCleaning deploy dir: \'' + deploydir + '\'')

        if (os.path.isdir(deploydir)):
            shutil.rmtree(deploydir)

        print('Creating deploy dir: \'' + deploydirroot + '\'')
        os.makedirs(deploydirroot)

        print('\nExecuting deployment steps:')
        for value in release.deploysteps:
            print('\n *** ' + str(value).upper() + ' *** \n')
            value(self.source_dir, releasedir, os.environ)

        print('\nRemoving junk...')

        for subdir, dirs, files in os.walk(deploydirroot):
            for file in files:
                filepath = os.path.join(subdir, file)
                if ( file == '.gitignore' ):
                    os.remove(filepath)
                    print(' * Removed:' + filepath)

        print('\nCreating archive...')
        if ( sys.platform.lower().startswith("win") ):
            shutil.make_archive(deploydirroot + '/..', "zip", deploydir)
            print(' * Generated: ' + buildname + '.zip')
        elif sys.platform.lower() == 'darwin':
            shutil.make_archive(deploydirroot, "gztar", deploydirroot)
            print(' * Generated: ' + buildname + '.tar.gz')
        else:
            shutil.make_archive(deploydirroot, "gztar", deploydirroot)
            print(' * Generated: ' + buildname + '.tar.gz')
