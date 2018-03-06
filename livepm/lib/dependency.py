from livepm.lib.version import *
from livepm.lib.minimalgit import *
import os

class Dependency:
    def __init__(self, options):
        self.name = options['name']
        self.version = Version(options['version'])
        self.repository = options['repository']

    def __call__(self, sourcedir, releasedir, releaseid, options = {}):
        dependencydir = os.path.join(sourcedir, 'dependencies')
        if not os.path.exists(dependencydir):
            os.makedirs(dependencydir)

        self.repodir = os.path.join(sourcedir, 'dependencies/' + self.name)
        self.releasedir = os.path.join(releasedir, self.name)
        if ( not os.path.exists(self.repodir) ):
            try:
                MinimalGit(self.repository).clone('dev', self.repodir, sourcedir)
            except Exception as e:
                print("Failed to clone repo to \'" + sourcedir + "\': " + str(e))
                print("Clone the repo manually in order to continue.")
                exit(1)

    def __str__(self):
        return str(self.name) + '(' + str(self.version) + ')'
