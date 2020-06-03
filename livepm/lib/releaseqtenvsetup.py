import os
import shutil
from livepm.lib.process import Process
from livepm.lib.releaseaction import *

class ReleaseQtEnvSetup(ReleaseAction):
    def __init__(self, parent, step, options = None):
        super().__init__('qtenvsetup', parent, step)

    def __call__(self, sourcedir, releasedir, environment = os.environ):
        if 'QTDIR' in environment:
            qtdir = environment['QTDIR']

            qtdirparent = os.path.abspath(os.path.join(qtdir, os.pardir))
            qtdirversion = os.path.basename(qtdirparent)
            qtdirparentparent = os.path.abspath(os.path.join(qtdirparent, os.pardir))

            qtdirdocs = os.path.join(qtdirparentparent, 'Docs', 'Qt-' + qtdirversion)

            environment['QTDOCSDIR'] = qtdirdocs
            self.parent.environment['QTDOCSDIR'] = 'qtdocsdir'

            print("Added qtdocsdir to the environment: " + qtdirdocs)
