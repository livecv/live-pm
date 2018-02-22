import os
import platform
from livepm.lib.process import *

class MinimalGit:

    def __init__(self, repository):
        self.repository = repository

    def clone(self, branch = 'master', location = None, cwd = os.getcwd()):
        location_path = [] if location == None else [os.path.abspath(location)]
        proc = Process.run(['git', 'clone', '-b', branch, self.repository] + location_path, cwd)
        Process.trace('GIT: ', proc, end = '')
