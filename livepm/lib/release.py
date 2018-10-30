import os
import platform

from livepm.lib.releaseaction import ReleaseAction
from livepm.lib.releasesolveincludes import ReleaseSolveIncludes
from livepm.lib.releasedylib import ReleaseDylibRelink, ReleaseDylibAddRPath
from livepm.lib.releaseclean import ReleaseClean
from livepm.lib.process import Process
from livepm.lib.filesystem import FileSystem
from livepm.lib.winvsenviron import *


class ReleaseMake(ReleaseAction):

    def __init__(self, parent, step, options = None):
        super().__init__('make', parent, step)
        self.options = options
        self.makecommand = 'make'

    def __call__(self, sourcedir, releasedir, environment = os.environ):
        proc = Process.run([self.makecommand] + self.options, self.run_dir(releasedir), environment)
        Process.trace('MAKE: ', proc, end='')

class ReleaseNMake(ReleaseAction):

    def __init__(self, parent, step, options = None):
        super().__init__('nmake', parent, step)
        self.options = options
        self.makecommand = 'nmake'

    def __call__(self, sourcedir, releasedir, environment = os.environ):
        VSEnvironment.setupenv(140, 'x86_amd64')
        proc = Process.run([self.makecommand] + self.options, self.run_dir(releasedir), environment)
        Process.trace('MAKE: ', proc, end='')

class ReleaseQmake(ReleaseAction):

    def __init__(self, parent, step, options = None):
        super().__init__('qmake', parent, step)
        self.options = options
        self.qmakecommand = os.path.join(
            os.environ['QTDIR'],
            'bin/qmake' + ('.exe' if platform.system().lower() == 'windows' else ''))

    def __call__(self, sourcedir, releasedir, environment = os.environ):
        if platform.system().lower() == 'windows':
            VSEnvironment.setupenv(140, 'x86_amd64')
        proc = Process.run([self.qmakecommand] + self.options + [os.path.abspath(sourcedir)], self.run_dir(releasedir), environment)
        Process.trace('QMAKE: ', proc, end='')

class ReleaseCopy(ReleaseAction):
    def __init__(self, parent, step, options = None):
        super().__init__('copy', parent, step)
        self.options = options

    def __call__(self, sourcedir, releasedir, environment = os.environ):
        structurepaths = {}
        for key, value in self.parent.environment.items():
            structurepaths[value] = environment[key]

        structurepaths['source']  = sourcedir
        structurepaths['release'] = releasedir

        print('COPY:' + releasedir)

        FileSystem.copyFileStructure(self.run_dir(releasedir), self.options, structurepaths)

class ReleaseRun(ReleaseAction):
    def __init__(self, parent, step, options = None):
        super().__init__('run', parent, step)
        self.options = options

    def __call__(self, sourcedir, releasedir, environment = os.environ):
        print('RUN:' + str(self.options))
        proc = Process.run([] + self.options, self.run_dir(releasedir), environment)
        Process.trace('RUN: ', proc, end='')

class ReleaseWrite(ReleaseAction):
    def __init__(self, parent, step, options = None):
        super().__init__('write', parent, step)
        self.options = options

    def __call__(self, sourcedir, releasedir, environment = os.environ):
        filepath = os.path.join(self.run_dir(releasedir), self.options['file'])

        if isinstance(self.options['data'], list):
            writedata = ''.join(self.options['data'])
        else:
            writedata = self.options['data']

        print('WRITE: File \'' + filepath + '\'')
        f = open(filepath, 'w')
        f.write(writedata)
        f.close()

class Release:
    def __init__(self, name, version, releaseid, opt):
        self.id = releaseid
        self.name = name
        self.version = version
        self.compiler = opt['compiler']
        self.environmentopt = opt['environment']
        self.buildopt = opt['build']
        self.deployopt = opt['deploy']
        self.environment = {}

        self.buildsteps = []
        for val in opt['build']:
            if ( len(val) != 1 ):
                raise Exception("Build step must be of single key type:" + str(val))
            buildtype = next(iter(val))
            buildstep = self.create_action('build', buildtype, val[buildtype])
            self.buildsteps.append(buildstep)

        self.deploysteps = []
        for val in opt['deploy']:
            if ( len(val) != 1 ):
                raise Exception("Deploy step must be of single key type:" + str(val))
            deploytype = next(iter(val))
            deploystep = self.create_action('deploy', deploytype, val[deploytype])
            self.deploysteps.append(deploystep)

    def dir_name(self):
        return self.name.replace('.', '-')

    def release_name(self):
        return self.dir_name() + '-' + str(self.version) + '-' + self.id.replace('_', '-')

    def init_environment(self):
        for key, value in self.environmentopt.items():
            if key not in os.environ:
                raise Exception("Failed to find key in environment: " + key)
            self.environment[key] = value

    def create_action(self, step, type, options):
        actions = {
            'make' : ReleaseMake,
            'nmake' : ReleaseNMake,
            'qmake' : ReleaseQmake,
            'copy' : ReleaseCopy,
            'run' : ReleaseRun,
            'write' : ReleaseWrite,
            'solveincludes': ReleaseSolveIncludes,
            'dylibrelink': ReleaseDylibRelink,
            'dylibaddrpath': ReleaseDylibAddRPath,
            'clean' : ReleaseClean
        }
        return actions[type](self, step, options)

    def to_json(self):
        return {
            "compiler" : self.compiler,
            "environment" : self.environmentopt,
            "build" : self.buildopt,
            "deploy" : self.deployopt
        }


# runsample = [
#     {'run': ['ls'], 'wd': '..' },
#     {'run': ['ls -la | grep deploy.py'], 'shell' : True}
# ]
# def runarray(structure, prefix = ''):
#     for runitem in structure:
#         if ( isinstance(runitem, list) ):
#             if ( len(runitem) > 0 ):
#                 proc = DeployExec.run(runitem, DeployExec.scriptdir())
#                 DeployExec.trace(prefix + runitem[0] + ': ', proc, end = '')
#         elif ( isinstance(runitem, dict) ):
#             if ( len(runitem['run']) > 0 ):
#                 wd = runitem['wd'] if ('wd' in runitem) else DeployExec.scriptdir()
#                 if not os.path.isabs(wd):
#                     wd = os.path.join(DeployExec.scriptdir(), wd)
#                 shell = True if 'shell' in runitem and runitem['shell'] else False
#                 proc = DeployExec.run(runitem['run'], wd, shell=shell)
#                 DeployExec.trace(prefix + runitem['run'][0] + ': ', proc, end = '')
