import sys
import os
import getopt
import json
import shutil
from livecv.configuration import *

def build(packagefile, releaseid, sourcedir, builddir, options = {}):

    print('\nParsing build file \'' + packagefile + '\'...')

    with open(packagefile) as jsonfile:
        packagejson = json.load(jsonfile)

    config = Configuration(packagejson)
    if ( not config.has_release(releaseid) ):
        raise Exception("Failed to find release id:" + releaseid)

    release = config.release(releaseid)

    sourcedir = os.path.abspath(sourcedir)
    releasedir = os.path.abspath(os.path.join(builddir, release.compiler))

    print('\nConfiguration found: ' + releaseid)

    print('  Modules:')
    for key, value in config.components.items():
        print('   * ' + str(value))

    print('  Dependencies:')
    for value in config.dependencies:
        print('   * ' + str(value))

    print('  Source dir: \'' + sourcedir + '\'')
    print('  Release dir: \'' + releasedir + '\'')
    print('  Compiler: \'' + release.compiler + '\'')
    print('  Environment:')
    for key, value in release.environment.items():
        print('   * ' + key + ':\'' + os.environ[key] + '\'')

    print('\nCleaning release dir: \'' + releasedir + '\'')
    if ( os.path.isdir(releasedir) ):
        shutil.rmtree(releasedir)
    os.makedirs(releasedir)

    print('\nSolving dependencies:')
    for value in config.dependencies:
        print('\n *** ' + str(value) + ' *** \n')
        value(sourcedir)

    exit(0)

    print('\nExecuting build steps:')

    for value in release.buildsteps:
        print('\n *** ' + str(value) + ' *** \n')
        value(sourcedir, releasedir, os.environ)

def main(argv):
    # try:
        sourcedir   = None
        builddir    = None
        options     = None

        usage = 'Usage: livecv_build.py [-s <source-dir> -o <options> -b <builddir>] <packagefile> <releaseid>'
        # try:
        opts, args = getopt.getopt(argv,"hc:s:o:b")
        for opt, arg in opts:
            if ( opt == '-h' ):
                print(usage)
                sys.exit()
            elif ( opt == '-r'):
                releaseid = arg
            elif ( opt == '-s'):
                sourcedir = arg
            elif ( opt == 'b'):
                builddir = arg
            elif ( opt == '-o'):
                options = arg

        if ( len(args) == 0 ):
            print('No deployment file specified.')
            print(usage)
            sys.exit(2)
        if ( len(args) == 1 ):
            print('No release id specified.')
            print(usage)
            sys.exit(2)
        if ( len(args) > 2 ):
            print('Too many arguments specified.')
            print(usage)
            sys.exit(2)

        packagefile = Configuration.findpackage(os.path.abspath(args[0]))

        # Fix source path
        if ( sourcedir == None ):
            sourcedir = os.path.dirname(packagefile)
        if ( builddir == None ):
            builddir = sourcedir + '/build'

        build(packagefile, args[1], sourcedir, builddir)
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
