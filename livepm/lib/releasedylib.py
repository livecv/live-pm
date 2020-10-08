import os
import platform
import fnmatch

from time import sleep

from livepm.lib.process import Process
from livepm.lib.releaseaction import ReleaseAction
from livepm.lib.filesystem import FileSystem
from livepm.lib.dylibdependencies import DylibDependencyTransfer

class ReleaseDylibAddRPath(ReleaseAction):
    
    def __init__(self, parent, step, options = None):
        super().__init__("dylibaddrpath", parent, step)
        self.options = options

    def __call__(self, sourcedir, releasedir, environment = os.environ):
        for key, value in self.options.items():
            if not os.path.isabs(key):
                key = os.path.join(self.run_dir(releasedir), key)

            log = ''

            entries = FileSystem.listEntries(key)
            for entry in entries:
                if not os.path.islink(entry):
                    for rpath in value:
                        intproc = Process.run(
                            ['install_name_tool', '-add_rpath', rpath, entry], 
                            self.run_dir(releasedir)
                        )
                        Process.trace('Dylib AddRPath: ', intproc)
                        log += "Dylib Added RPath: " + entry + " -> " + rpath + '; '
            
            print(log)


class ReleaseDylibRelink(ReleaseAction):

    def __init__(self, parent, step, options = None):
        super().__init__('dylibrelink', parent, step)
        self.options = options

    def __call__(self, sourcedir, releasedir, environment = os.environ):
        for key, value in self.options.items():
            if not os.path.isabs(key):
                key = os.path.join(self.run_dir(releasedir), key)

            proc = Process.run(['otool', '-L', key], self.run_dir(releasedir))
            collect = []

            while proc.poll() is None:
                line = proc.stdout.readline()
                if line:
                    ReleaseDylibRelink.addLine(collect, line)

            line = proc.stdout.readline()
            while( line ):
                ReleaseDylibRelink.addLine(collect, line)
                line = proc.stdout.readline()

            header_was_printed = False

            for l in collect:
                for liboldpattern, libnewvalue in value.items():
                    if ( fnmatch.fnmatch(l, liboldpattern) ):
                        libname = l
                        libnameidx = l.rfind('/')
                        if libnameidx != -1:
                            libname = l[libnameidx:]
                        
                        if libnewvalue == '-':
                            libnewvalue = libname
                        elif libnewvalue.endswith('/-'):
                            libnewvalue = libnewvalue[0:-2] + libname

                        if not header_was_printed:
                            print('Dylib: ' + key + ':')
                            header_was_printed = True
                        print('Dylib:    ' + l + ' -> ' + libnewvalue)

                        # install_name_tool -change /usr/local/opt/opencv/lib/libopencv_core.3.3.dylib @rpath/OpenCV.framework/Libraries/libopencv_core.3.3.dylib liblcvcore.dylib
                        intproc = Process.run(
                            ['install_name_tool', '-change', l, libnewvalue, key], 
                            self.run_dir(releasedir)
                        )
                        Process.trace('Dylib Link: ', intproc)

    def addLine(collect, line):
        try:
            idx = line.index('(')
            line = line[:idx]
        except ValueError:
            pass
        
        if not line.strip().endswith(':') and line:
            collect.append(line.strip())


class ReleaseDylibTransferDependencies(ReleaseAction):
    
    def __init__(self, parent, step, options = None):
        super().__init__("dylibtransferdependencies", parent, step)
        self.options = options

    def __call__(self, sourcedir, releasedir, environment = os.environ):
        structurepaths = {}
        for key, value in self.parent.environment.items():
            structurepaths[value] = environment[key]

        deploydir = os.path.abspath(releasedir + '/../' + self.parent.release_name())

        self.options['dependencies'] = self.options['dependencies'].format_map(structurepaths)
        self.options['files']        = self.options['files'].format_map(structurepaths)
        self.options['destination']  = os.path.join(deploydir, self.options['destination'].format_map(structurepaths))
        
        ldt = DylibDependencyTransfer(self.options)

        def dlyboutput(s):
            print('Dylib DT:' + s)
            sleep(0.01)
            print("SLEPT FOR 0.01")


        # ldt.run(lambda s : print('Dylib Dependency Transfer: ' + s))
        ldt.run(dlyboutput)
        # counter_test = 0
        # while ( counter_test < 2000 ):
        #     print(counter_test)
        #     counter_test += 1
        # print("DEP TRANSFER NOT RUN")