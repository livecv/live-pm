import sys
import os
import getopt
import json
import shutil
from livepm.lib.configuration import Configuration

class Builder:

    def __init__(self, packagepath, releaseid):
        self.packagefile = Configuration.findpackage(packagepath)
        self.releaseid = releaseid

        print('\nParsing build file \'' + self.packagefile + '\'...')

        with open(self.packagefile) as jsonfile:
            packagejson = json.load(jsonfile)

        self.config = Configuration(packagejson)
        if ( not self.config.has_release(self.releaseid) ):
            raise Exception("Failed to find release id:" + self.releaseid)

        self.release = self.config.release(self.releaseid)

        print('\nConfiguration found: ' + self.releaseid)

    def __call__(self, sourcedir, builddir, options = {}):

        sourcedir = os.path.abspath(sourcedir)

        print('  Modules:')
        for key, value in self.config.components.items():
            print('   * ' + str(value))

        print('  Dependencies:')
        for value in self.config.dependencies:
            print('   * ' + str(value))

        print('  Source dir: \'' + sourcedir + '\'')
        print('  Release dir: \'' + builddir + '\'')
        print('  Compiler: \'' + self.release.compiler + '\'')

        self.release.init_environment()
        print('  Environment:')
        for key, value in self.release.environment.items():
            print('   * ' + key + ':\'' + os.environ[key] + '\'')

        print('\nCleaning release dir: \'' + builddir + '\'')
        if ( os.path.isdir(builddir) ):
            shutil.rmtree(builddir)
        os.makedirs(builddir)

        if ( len(self.config.dependencies) > 0 ):
            print('\nSolving dependencies:')
            for depends in self.config.dependencies:
                print('\n --------------------- ' + str(depends) + ' --------------------- \n')
                depends(sourcedir, builddir, self.releaseid)
                b = Builder(depends.repodir, self.releaseid)
                b.releasedir = depends.releasedir
                b(depends.repodir, depends.releasedir, options)

                for value in self.release.buildsteps:
                    if ( value.name == 'qmake' ):
                        value.options = [
                            "BUILD_DEPENDENCIES=false",
                            "LIVECV_BIN_PATH=\'" + depends.releasedir + "/bin\'",
                            "LIVECV_DEV_PATH=\'" + sourcedir + "/dependencies/livecv" + "\'",
                            "DEPLOY_PATH=\'" + builddir + "/bin\'"
                        ]

        print('\nExecuting build steps:')

        for value in self.release.buildsteps:
            print('\n *** ' + str(value) + ' *** \n')
            value(sourcedir, builddir, os.environ)
