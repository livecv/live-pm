import sys
import os
import platform
import shutil
import argparse

from livepm.lib.process import *
from livepm.lib.command import Command

class MakeDocCommand(Command):
    name ='makedoc'
    description = 'Generate documentation.'

    def __init__(self):
        pass

    def parse_args(self, argv):
        parser = argparse.ArgumentParser(description = MakeDocCommand.description)
        parser.add_argument('source', default='', help="Source directory.")
        parser.add_argument('--release', '-r', default='', help="Release directory.")

        args = parser.parse_args(argv)

        self.sourcedir = os.path.abspath(args.source)
        self.releasedir = args.release
        if ( self.releasedir == '' ):
            self.releasedir = os.path.join(self.sourcedir, 'build')
        else:
            self.releasedir = os.path.abspath(self.releasedir)

    def __call__(self):
        if ( 'QTDIR' not in os.environ ):
            raise Exception("Failed to find environment variable \'QTDIR\'.")

        qdoccommand = os.path.join(
            os.environ['QTDIR'],
            'bin/qdoc' + ('.exe' if platform.system().lower() == 'windows' else ''))

        docsourcedir = MakeDocCommand.filebyext(os.path.join(self.sourcedir, 'doc/src'), 'qdocconf')

        proc = Process.run([qdoccommand] + ['--highlighting'] + [docsourcedir], self.sourcedir, os.environ)
        Process.trace('QDOC: ', proc, end='')

        releasedirname = os.path.join(self.releasedir, 'doc')

        print('\nCreating archive...')
        if ( sys.platform.lower().startswith("win") ):
            shutil.make_archive(releasedirname, "zip", os.path.join(self.sourcedir, 'doc/html'))
            print(' * Generated: ' + releasedirname + '.zip')
        else:
            shutil.make_archive(releasedirname, "gztar", os.path.join(self.sourcedir, 'doc/html'))
            print(' * Generated: ' + releasedirname + '.tar.gz')


    def filebyext(d, ext):
        for file in os.listdir(d):
            if file.endswith(ext):
                return os.path.join(d, file)

