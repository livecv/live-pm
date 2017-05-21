import os

class ReleaseAction:
    def __init__(self, name, parent, step):
        self.name = name
        self.step = step
        self.parent = parent

    def run_dir(self, releasedir):
        if ( self.step == 'build' ):
            return releasedir
        elif ( self.step == 'deploy' ):
            deploydir = os.path.abspath(releasedir + '/../' + self.parent.release_name())
            deploydirroot = os.path.join(deploydir, self.parent.name) + '/'
            return deploydirroot

    def __str__(self):
        return self.name
