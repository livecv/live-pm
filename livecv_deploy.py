import sys
import os
import getopt
import json
import shutil
from livecv.configuration import *

def deploy(packagefile, releaseid, sourcedir, builddir, options = {}):

    print('\nParsing build file \'' + packagefile + '\'...')

    with open(packagefile) as jsonfile:
        packagejson = json.load(jsonfile)

    config = Configuration(packagejson)
    if ( not config.has_release(releaseid) ):
        raise Exception("Failed to find release id:" + releaseid)

    print('  Version:' + str(config.version))
    print('  Modules:')
    for key, value in config.components.items():
        print('   * ' + str(value))

    print('  Dependencies:')
    for value in config.dependencies:
        print('   * ' + str(value))

    release = config.release(releaseid)
    releasedir = os.path.abspath(os.path.join(builddir, release.compiler))

    print('\nConfiguration found: ' + releaseid)
    print('  Source dir: \'' + sourcedir + '\'')
    print('  Release dir: \'' + releasedir + '\'')
    print('  Compiler: \'' + release.compiler + '\'')
    print('  Environment:')
    for key, value in release.environment.items():
        print('   * ' + key + '[' + value + ']: \'' + os.environ[key] + '\'')

    buildname = release.release_name()
    deploydir = os.path.abspath(releasedir + '/../' + buildname)
    deploydirroot = deploydir + '/livecv/'

    print('\nCleaning deploy dir: \'' + deploydir + '\'')

    if (os.path.isdir(deploydir)):
        shutil.rmtree(deploydir)
    os.makedirs(deploydirroot)

    print('\nExecuting deployment steps:')
    for value in release.deploysteps:
        print('\n *** ' + str(value).upper() + ' *** \n')
        value(sourcedir, releasedir, os.environ)


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
    else:
        shutil.make_archive(deploydirroot + '/..', "gztar", deploydirroot)
        print(' * Generated: ' + buildname + '.tar.gz')

def main(argv):
    # try:
        sourcedir   = None
        builddir    = None
        options     = None

        usage = 'Usage: livecv_deploypy [-s <source-dir> -o <options> -b <builddir>] <buildfile> <releaseid>'
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

        deploy(packagefile, args[1], sourcedir, builddir)
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
