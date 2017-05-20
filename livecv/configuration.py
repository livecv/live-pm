from livecv.release import *
from livecv.component import *
from livecv.version import *

class Configuration:

    def __init__(self, options):
        self.components = {}
        for key, value in options['components'].items():
            self.components[key] = Component(key, value)
        self.version = Version(options['version'])
        self.name = options["name"]
        self.releases = {}
        for key, value in options['releases'].items():
            self.releases[key] = Release(self.name, self.version, key, value)

    def has_release(self, releaseid):
        if ( releaseid in self.releases ):
            return True
        return False

    def release(self, releaseid):
        return self.releases[releaseid]
