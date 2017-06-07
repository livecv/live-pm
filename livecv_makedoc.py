import sys
import os
import platform
import shutil
from livecv.process import *

def filebyext(d, ext):
    for file in os.listdir(d):
        if file.endswith(ext):
            return os.path.join(d, file)

def main(argv):
    # try:
        usage = 'Usage: livecv_document.py <sourcedir> [<releasedir]'
        # try:
        if ( len(argv) == 0 ):
            print('No sourcedir specified.')
            print(usage)
            sys.exit(2)
        if ( len(argv) > 2 ):
            print('Too many arguments specified.')
            print(usage)
            sys.exit(2)
        if ( argv[0] == '-h' ):
            print(usage)
            sys.exit(0)

        sourcedir = os.path.abspath(argv[0])
        if ( len(argv) == 2 ):
            releasedir = os.path.abspath(argv[1])
        else:
            releasedir = os.path.join(sourcedir, 'build')

        if ( 'QTDIR' not in os.environ ):
            raise Exception("Failed to find environment variable \'QTDIR\'.")

        qdoccommand = os.path.join(
            os.environ['QTDIR'],
            'bin/qdoc' + ('.exe' if platform.system().lower() == 'windows' else ''))

        docsourcedir = filebyext(os.path.join(sourcedir, 'doc/src'), 'qdocconf')

        proc = Process.run([qdoccommand] + ['--highlighting'] + [docsourcedir], sourcedir, os.environ)
        Process.trace('QDOC: ', proc, end='')

        releasedirname = os.path.join(releasedir, 'doc')

        print('\nCreating archive...')
        if ( sys.platform.lower().startswith("win") ):
            shutil.make_archive(releasedirname, "zip", os.path.join(sourcedir, 'doc/html'))
            print(' * Generated: ' + releasedirname + '.zip')
        else:
            shutil.make_archive(releasedirname, "gztar", os.path.join(sourcedir, 'doc/html'))
            print(' * Generated: ' + releasedirname + '.tar.gz')

        #
        # except getopt.GetoptError:
        #     print()
        #     sys.exit(2)

    # except Exception as err:
    #     print("Cannot build project due to the following exception:\n Exception: " + str(err))
    #     sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
