import os
import io
import subprocess
import shutil
import scriptcommon
from subprocess import Popen


SOURCE_DIR  = scriptcommon.OSOperations.scriptdir() + '/..'
RELEASE_DIR = scriptcommon.OSOperations.scriptdir() + '/../build/build-msvc2013-64'
QMAKE       = os.path.join(os.environ['QT_DIR'], 'msvc2013_64/bin/qmake.exe')
MAKE        = "nmake"

scriptcommon.VSEnvironment.setupenv(120, 'x86_amd64')

b = scriptcommon.Build(SOURCE_DIR, RELEASE_DIR, QMAKE, MAKE)
b.cleandir()
b.createmakefile()
b.runmake(os.environ)
