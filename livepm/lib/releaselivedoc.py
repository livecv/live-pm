import os
import shutil
from livepm.lib.process import Process
from livepm.lib.releaseaction import *


class ReleaseLiveDoc(ReleaseAction):
    def __init__(self, parent, step, options = None):
        super().__init__('livedoc', parent, step)
        if 'path' in options:
            self.deploy_path = options['path']
        else:
            self.deploy_path = None
        
        if not 'LIVEDOC' in os.environ:
            print("Warning!: 'LIVEDOC' environment variable not set. Documentation will not be generated.")
            return

    def __call__(self, sourcedir, releasedir, environment = os.environ):
        deploy_to = self.run_dir(releasedir)
        if self.deploy_path:
            deploy_to = os.path.join(deploy_to, self.deploy_path)

        if not 'LIVEDOC' in os.environ:
            print("Warning!: 'LIVEDOC' environment variable not set. Skipping documentation.")
            return

        proc = Process.run(['node', os.environ['LIVEDOC'], '--deploy', deploy_to, os.path.abspath(sourcedir)], os.path.dirname(os.environ['LIVEDOC']), environment)
        Process.trace('LIVEDOC: ', proc, end='')
