import sys
import os
import getopt
import platform
import scriptcommon


def build(compiler = None, bits = None, sourcedir = None):
    if ( bits == None ):
        bits = '64' if sys.maxsize > 2**32 else 32
    if (compiler is None):
        if ( sys.platform.lower().startswith("win")):
            compiler = 'msvc2013' + ('_64' if bits == '64' else '')
        else:
            compiler = 'gcc' + ('_64' if bits == '64' else '')


    if ( not 'QTDIR' in os.environ ):
        raise Exception("QTDIR environment variable has not been set.")

    if ( not 'OPENCV_DIR' in os.environ and compiler.startswith('msvc')):
        raise Exception("OPENCV_DIR environment variable has not been set.")

    if (sourcedir == None):
        sourcedir = scriptcommon.OSOperations.scriptdir() + '/..'

    releasedir = sourcedir + '/build/' + compiler

    qmake = os.path.join(os.environ['QTDIR'], '../' + compiler + '/bin/qmake' + ('' if 'gcc' in compiler else '.exe'))
    make  = 'nmake' if compiler.startswith('msvc') else 'make'
    if ( compiler.startswith('msvc') ):
        if bits == '64':
            scriptcommon.VSEnvironment.setupenv(120, 'x86_amd64')
        else:
            scriptcommon.VSEnvironment.setupenv(120, 'x86')
            os.environ['OPENCV_DIR'] = os.environ['OPENCV_DIR'].replace('\\x64\\', '\\x86\\')


    print('Building Live CV on ' + os.environ['OPENCV_DIR'])
    print('Compiler: ' + compiler)
    print('Qmake:' + qmake)
    print('From: ' + sourcedir)
    print('To: ' + releasedir)

    b = scriptcommon.Build(sourcedir, releasedir, qmake, make)
    b.cleandir()
    b.createmakefile(os.environ)
    b.runmake(os.environ)

def main(argv):
    try:
        compiler = None
        osbit = None
        sourcedir = None

        usage = 'Usage: livecv_build.py [-c <compiler> -b <platform:32 or 64> -s <source-dir>]'

        try:
            opts, args = getopt.getopt(argv,"hc:b:s:")
            for opt, arg in opts:
                if ( opt == '-h' ):
                    print(usage)
                    sys.exit()
                elif ( opt == '-c'):
                    compiler = arg
                elif ( opt == '-b'):
                    osbit = arg
                elif ( opt == '-s'):
                    sourcedir = arg

            build(compiler, osbit, sourcedir)

        except getopt.GetoptError:
            print()
            sys.exit(2)

    except Exception as err:
        print("Cannot build project due to the following exception:\n Exception: " + str(err))
        sys.exit(1)

if __name__ == "__main__":
   main(sys.argv[1:])
