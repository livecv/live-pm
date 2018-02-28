import os
import shutil
from livepm.lib.releaseaction import *

class ReleaseSolveIncludesItem:
    def __init__(self, parent, include, to, source):
        self.parent = parent
        self.include = include
        self.to = to
        self.source = source

    def find(name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)
        return None

    def __call__(self, releasedir, paths):
        absinclude = self.include.format_map(paths)
        absto = os.path.join(self.parent.run_dir(releasedir), self.to)
        if ( not os.path.exists(absto) ):
            os.makedirs(absto)
        print('Includes: Iterating \'' + absinclude + '\'')
        for filename in os.listdir(absinclude):
            if filename.endswith(".h") or filename.endswith(".hh") or filename.endswith('.hpp'):
                filefound = False
                for sourcepath in self.source:
                    sourcepath = sourcepath.format_map(paths)
                    sourcefile = ReleaseSolveIncludesItem.find(filename, sourcepath)
                    if ( sourcefile is not None ):
                        sourcefilepath = os.path.join(sourcepath, filename)
                        shutil.copyfile(sourcefilepath, os.path.join(absto, filename))
                        print('Includes: Solved \'' + sourcefilepath + '\'')
                        filefound = True
                        break
                if ( not filefound ):
                    print('Includes: Warning, no match found for \'' + filename + '\'')


class ReleaseSolveIncludes(ReleaseAction):
    def __init__(self, parent, step, options = None):
        super().__init__('solveincludes', parent, step)
        self.items = []
        for value in options:
            self.items.append(ReleaseSolveIncludesItem(
                self, value['from'], value['to'], value['source']
            ))

    def __call__(self, sourcedir, releasedir, environment = os.environ):

        structurepaths = {}
        for key, value in self.parent.environment.items():
            structurepaths[value] = environment[key]

        structurepaths['source']  = sourcedir
        structurepaths['release'] = releasedir

        for item in self.items:
            item(releasedir, structurepaths)
