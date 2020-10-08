import os
import platform
import fnmatch
import shutil

from livepm.lib.process import Process
from livepm.lib.filesystem import FileSystem

class DylibLinkInfoExternal:

    def __init__(self, path):
        self.path = path
        if ( not os.path.exists(path) ):
            raise Exception("Path does not exist:" + path)

        self.dependencies = []
        self.rpath_info = []

        proc = Process.run(['otool', '-L', self.path], os.getcwd())

        while proc.poll() is None:
            line = proc.stdout.readline()
            if line:
                DylibLinkInfoExternal.add_dependency_line(self.dependencies, line)

        line = proc.stdout.readline()
        while( line ):
            DylibLinkInfoExternal.add_dependency_line(self.dependencies, line)
            line = proc.stdout.readline()

        proc = Process.run(['otool', '-l', self.path], os.getcwd())

        while proc.poll() is None:
            line = proc.stdout.readline()
            if line:
                self.add_rpath_line(line)

        line = proc.stdout.readline()
        while( line ):
            self.add_rpath_line(line)
            line = proc.stdout.readline()

    def add_rpath_line(self,line):
        short = line.strip()
        if short.startswith('path '):
            index = short.find('(offset')
            if index > 0:
                self.rpath_info.append(short[5:index].strip())

    def add_dependency_line(collect, line):
        try:
            idx = line.index('(')
            line = line[:idx]
        except ValueError:
            pass
        
        if not line.strip().endswith(':') and line:
            collect.append(line.strip())

    def find_dependencies(self, pattern):
        result = []
        for l in self.dependencies:
            if ( fnmatch.fnmatch(l, pattern) ):
                result.append(l)

        return result

    def find_absolute_dependencies(self, pattern):
        result = []
        for l in self.dependencies:
            if ( fnmatch.fnmatch(self.absolute_dependency(l), pattern) ):
                result.append(l)
        return result

    def absolute_dependency(self, dependency):
        if dependency.startswith('@rpath'):
            for index, rp in enumerate(self.rpath_info):
                res = rp + dependency[6:]
                if os.path.exists(res):
                    return res
            return ''
        return dependency

    def add_rpath(self, path):
        Process.back_tick(
            ['install_name_tool', '-add_rpath', path, self.path], 
            os.getcwd()
        )
        return True

    def change_dependency(self, old, new):
        for index, dep in enumerate(self.dependencies):
            if dep == old:
                Process.back_tick(
                    ['install_name_tool', '-change', dep, new, self.path], 
                    os.getcwd()
                )
                self.dependencies[index] = new
                return True

        return False


    def change_dependencies(self, structure):
        args = ['install_name_tool', ]
        for old, new in structure.items():
            for index, dep in enumerate(self.dependencies):
                if dep == old:
                    args.append('-change')
                    args.append(dep)
                    args.append(new)
                    self.dependencies[index] = new

        args.append(self.path)
        changeproc = Process.run(args, os.getcwd())
        changeproc.wait()

        return True

    # This sets the install name of the .dylib file itself and will be used as the prototype 
    # install name from that point forward when something links with the .dylib
    def change_id(self, old, new):
        for index, dep in enumerate(self.dependencies):
            if dep == old:
                changeproc = Process.run(
                    ['install_name_tool', '-id', dep, new, self.path], 
                    os.getcwd()
                )
                changeproc.wait()

                self.dependencies[index] = new
                return True

        return False
        
