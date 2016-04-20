import os
import io
import subprocess
import shutil
import scriptcommon
from subprocess import Popen


SOURCE_DIR  = scriptcommon.OSOperations.scriptdir() + '/..'
RELEASE_DIR = scriptcommon.OSOperations.scriptdir() + '/../build/build-msvc2013-32'
QMAKE       = os.path.join(os.environ['QT_DIR'], 'msvc2013/bin/qmake.exe')
MAKE        = "nmake"

scriptcommon.VSEnvironment.setupenv(120, 'x86')

os.environ['OPENCV_DIR'] = os.environ['OPENCV_DIR'].replace('\\x64\\', '\\x86\\')

b = scriptcommon.Build(SOURCE_DIR, RELEASE_DIR, QMAKE, MAKE)
b.cleandir()
b.createmakefile(os.environ)
b.runmake(os.environ)
