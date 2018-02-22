import glob
from livepm.lib.release import *
from livepm.lib.component import *
from livepm.lib.version import *
from livepm.lib.dependency import *

class Configuration:

    def __init__(self, options):
        self.components = {}
        for key, value in options['components'].items():
            self.components[key] = Component(key, value)
        self.version = Version(options['version'])
        self.name = options["name"]
        self.releases = {}
        self.dependencies = []
        if ( 'dependencies' in options ):
            for value in options['dependencies']:
                self.dependencies.append(Dependency(value))

        for key, value in options['releases'].items():
            self.releases[key] = Release(self.name, self.version, key, value)

    def has_release(self, releaseid):
        if ( releaseid in self.releases ):
            return True
        return False

    def release(self, releaseid):
        return self.releases[releaseid]

    def findpackage(path):
        if ( os.path.isdir(path) ):
            files = glob.glob(os.path.join(path, 'live*.json'))
            if len(files) == 0:
                raise Exception("No file package file found in " + path)
            return files[0]
        else:
            return path
