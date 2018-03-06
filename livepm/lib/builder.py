import sys
import os
import getopt
import json
import shutil
from livepm.lib.configuration import Configuration
from livepm.lib.dependencytree import DependencyTree

class Builder:

    def __init__(self, packagepath, releaseid):
        self.packagefile = Configuration.findpackage(packagepath)
        self.releaseid = releaseid
        self.solve_dependencies = True
        self.deploy_to_livecv = True
        self.livecv_bin_path = None
        self.livecv_dev_path = None
        self.dependencies = {}

        print('\nParsing build file \'' + self.packagefile + '\'...')

        with open(self.packagefile) as jsonfile:
            packagejson = json.load(jsonfile)

        self.config = Configuration(packagejson)
        if ( not self.config.has_release(self.releaseid) ):
            raise Exception("Failed to find release id:" + self.releaseid)

        self.release = self.config.release(self.releaseid)

        print('\nConfiguration found: ' + self.releaseid)

    def create_dependency_tree(self, packagepath, sourcedir, builddir):
        dependencies = {}
        package_file = Configuration.findpackage(packagepath)
        with open(package_file) as jsonfile:
            packagejson = json.load(jsonfile)

        config = Configuration(packagejson)
        if ( not self.config.has_release(self.releaseid) ):
            raise Exception("Failed to find release id " + self.releaseid + " in " + package_file)

        if ( len(config.dependencies) > 0 ):
            for depends in config.dependencies:
                depends(sourcedir, builddir, self.releaseid)
                dependencies[depends.name] = self.create_dependency_tree(depends.repodir, sourcedir, builddir)

        # TODO: Check for dependency loops

        return dependencies

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

        if ( len(self.config.dependencies) > 0 and self.solve_dependencies ):
            print('\nSolving dependencies:')
            dependency_tree = self.create_dependency_tree(sourcedir, sourcedir, builddir)
            print('Dependency Tree: ' + str(dependency_tree))

            print('\nSolving build order:')
            dt = DependencyTree(dependency_tree)
            builds = dt.build_order()

            print('Build order: ' + str(builds))

            for dependency_build in builds:
                dependency_source = os.path.join(sourcedir, "dependencies", dependency_build)
                dependency_release = os.path.join(builddir, dependency_build)

                b = Builder(dependency_source, self.releaseid)
                b.solve_dependencies = False

                if self.livecv_bin_path:
                    value.options.append("LIVECV_BIN_PATH=\'" + self.livecv_bin_path + "\'")
                if self.livecv_dev_path:
                    value.options.append("LIVECV_DEV_PATH=\'" + self.livecv_dev_path + "\'")

                b.releasedir = dependency_release
                b(dependency_source, dependency_release, options)

                if dependency_build == 'livecv':
                    self.livecv_bin_path = os.path.join(dependency_release, "bin")
                    self.livecv_dev_path = dependency_source

        print('\nCreating config file:')

        if ( os.path.exists(sourcedir + '/config.pri') ):
            os.rename(sourcedir + '/config.pri', sourcedir + '/config.pri.bak')

        options = ["BUILD_DEPENDENCIES=false"]
        if self.livecv_bin_path:
            options.append("LIVECV_BIN_PATH=\'" + self.livecv_bin_path + "\'")
        if self.livecv_dev_path:
            options.append("LIVECV_DEV_PATH=\'" + self.livecv_dev_path + "\'")
        if self.deploy_to_livecv:
            options.append("DEPLOY_TO_LIVECV=true")
        else:
            options.append("DEPLOY_TO_LIVECV=false")

        writedata = ''
        for t in options:
            writedata += t + '\n'

        f = open(sourcedir + '/config.pri', 'w')
        f.write(writedata)
        f.close()

        print('\nExecuting build steps:')

        for value in self.release.buildsteps:
            print('\n *** ' + str(value) + ' *** \n')

            value(sourcedir, builddir, os.environ)

        print('\nRemoving config file')

        os.remove(sourcedir + '/config.pri')
        if ( os.path.exists(sourcedir + '/config.pri.bak') ):
            os.rename(sourcedir + '/config.pri.bak', self.sourcedir + '/config.pri')


