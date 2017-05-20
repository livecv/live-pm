import os
import sys
import getopt
import json
from livecv.configuration import *

def version_sync(packagefile, sourcedir):
    print('\nParsing build file \'' + packagefile + '\'...')

    with open(packagefile) as jsonfile:
        packagejson = json.load(jsonfile)

    config = Configuration(packagejson)

    print('  Source dir: \'' + sourcedir + '\'')
    print('  Modules:')
    for key, value in config.components.items():
        print('   * ' + str(value))
        version = value.version
        for versionfile, versionexp in value.versionsyncs.items():
            filepath = os.path.join(sourcedir, versionfile)
            print('      > ' + 'Updating file \'' + filepath + '\' to version \'' + str(version) + '\'')
            version.savetofile(filepath, versionexp)

def main(argv):
    # try:
        sourcedir   = None

        usage = 'Usage: livecv_version_sync.py [-s <source-dir>] <packagefile>'
        # try:
        opts, args = getopt.getopt(argv,"hc:s:")
        for opt, arg in opts:
            if ( opt == '-h' ):
                print(usage)
                sys.exit()
            elif ( opt == '-s'):
                sourcedir = arg

        if ( len(args) == 0 ):
            print('No package file specified.')
            print(usage)
            sys.exit(2)
        if ( len(args) > 1):
            print('Too many arguments specified.')
            print(usage)
            sys.exit(2)


        packagefile = os.path.abspath(args[0])

        # Fix source path
        if ( sourcedir == None ):
            sourcedir = os.path.dirname(packagefile)

        version_sync(args[0], os.path.abspath(sourcedir))
        print()
        #
        # except getopt.GetoptError:
        #     print()
        #     sys.exit(2)

    # except Exception as err:
    #     print("Cannot build project due to the following exception:\n Exception: " + str(err))
    #     sys.exit(1)


if __name__ == "__main__":
   main(sys.argv[1:])
