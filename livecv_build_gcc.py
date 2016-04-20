import os
import io
import subprocess
import shutil
import scriptcommon
from subprocess import Popen

def build_gcc():
    SOURCE_DIR  = scriptcommon.OSOperations.scriptdir() + '/..'
    RELEASE_DIR = scriptcommon.OSOperations.scriptdir() + '/../build/build-gcc'
    QMAKE       = os.path.join(os.environ['QTDIR'], 'bin/qmake')
    MAKE        = 'make'

    b = scriptcommon.Build(SOURCE_DIR, RELEASE_DIR, QMAKE, MAKE)
    b.cleandir()
    b.createmakefile()
    b.runmake(os.environ)


if __name__ == '__main__':
    build_gcc()
