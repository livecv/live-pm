import os
import shutil
import fnmatch

from livepm.lib.releaseaction import *

class ReleaseClean(ReleaseAction):

    def __init__(self, parent, step, options = None):
        super().__init__('clean', parent, step)
        self.options = options

    def __call__(self, sourcedir, releasedir, environment = os.environ):
        for key, value in self.options.items():
            if not os.path.isabs(key):
                key = os.path.join(self.run_dir(releasedir), key)
            for subdir, dirs, files in os.walk(key):
                if ReleaseClean.is_match(subdir, value):
                    shutil.rmtree(subdir)
                    print('CLEAN: Removed ' + subdir)
                else:    
                    for file in files:
                        filepath = os.path.join(subdir, file)
                        if ReleaseClean.is_match(filepath, value):
                            os.remove(filepath)
                            print('CLEAN: Removed ' + filepath)

    def is_match(name, values):
        for value in values:
            if ( fnmatch.fnmatch(name, value) ):
                return True
        return False