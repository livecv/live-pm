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
        parser.add_argument('--livedoc', default='', help="Path to livedoc.")

        args = parser.parse_args(argv)

        self.sourcedir = os.path.abspath(args.source)
        self.releasedir = args.release
        self.livedoc = args.livedoc
        if ( self.releasedir == '' ):
            self.releasedir = os.path.join(self.sourcedir, 'build', 'doc')
        else:
            self.releasedir = os.path.abspath(self.releasedir)
        if ( self.livedoc == '' ):
            self.livedoc = os.path.join(os.getcwd(), 'live-doc.js')

    def __call__(self):
        proc = Process.run(['node'] + [self.livedoc] + ['--output-path', self.releasedir] + [self.sourcedir], os.path.dirname(self.livedoc), os.environ)
        Process.trace('LIVEDOC: ', proc, end='')

        # releasedirname = os.path.join(self.releasedir, 'doc')

        # print('\nCreating archive...')
        # if ( sys.platform.lower().startswith("win") ):
        #     shutil.make_archive(releasedirname, "zip", os.path.join(self.sourcedir, 'doc/html'))
        #     print(' * Generated: ' + releasedirname + '.zip')
        # else:
        #     shutil.make_archive(releasedirname, "gztar", os.path.join(self.sourcedir, 'doc/html'))
        #     print(' * Generated: ' + releasedirname + '.tar.gz')


    def filebyext(d, ext):
        for file in os.listdir(d):
            if file.endswith(ext):
                return os.path.join(d, file)

