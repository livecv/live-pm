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
        self.webpage = options['webpage']
        self.releases = {}
        self.dependencies = []
        if ( 'dependencies' in options ):
            for value in options['dependencies']:
                self.dependencies.append(Dependency(value))

        for key, value in options['releases'].items():
            self.releases[key] = Release(self.name, self.version, key, value)

    def create(name, version = Version("0.1.0"), webpage = ''):
        return Configuration({
            "name" : name,
            "version" : str(version),
            "webpage" : webpage,
            "dependencies" : [],
            "components" : {},
            "releases" : {}
        })

    def has_release(self, releaseid):
        if ( releaseid in self.releases ):
            return True
        return False

    def release(self, releaseid):
        return self.releases[releaseid]

    def add_component(self, name, opt):
        if name in self.components:
            raise Exception("Component already exists: " + name)
        self.components[name] = Component(name, opt)

    def to_json(self):
        dependencies = []
        components = {}
        releases = {}
        for dep in self.dependencies:
            dependencies.append(dep.to_json())
        for key, comp in self.components.items():
            components[comp.name] = comp.to_json()
        for key, release in self.releases.items():
            releases[release.id] = release.to_json()

        return {
            "version" : str(self.version),
            "name" : self.name,
            "webpage" : self.webpage,
            "dependencies" : dependencies,
            "components" : components,
            "releases" : releases
        }

    def findpackage(path):
        if ( os.path.isdir(path) ):
            files = glob.glob(os.path.join(path, 'live*.json'))
            if len(files) == 0:
                raise Exception("No file package file found in " + path)
            return files[0]
        elif not os.path.exists(path):
            raise Exception("Package file does not exist: " + path)
        else:
            return path
