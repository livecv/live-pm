from livecv.version import *
import os
import git

class Dependency:
    def __init__(self, options):
        self.name = options['name']
        self.version = Version(options['version'])
        self.repository = options['repository']

    def __call__(self, sourcedir):
        repodir = os.path.join(sourcedir, 'dependencies/' + self.name)
        if ( not os.path.exists(repodir) ):
            try:
                git.Git().clone(self.repository, repodir)
            except Exception as e:
                print("Failed to clone repo to \'" + sourcedir + "\': " + str(e))
                print("Clone the repo manually in order to continue.")
                exit(1)

        # BUILD

        # SET BIN_PATH
        # SET DEV_PATH
        # SET BUILD_DEPENDENCIES=false
        # SET DEPLOY_PATH



    def __str__(self):
        return str(self.name) + '(' + str(self.version) + ')'
