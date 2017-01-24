import os
import sys
import io
import scriptcommon

def main(argv):
    usage = 'Usage: livecv_version.py get / set <version> sourcedir'
    if ( len(argv) == 0 ):
        print(usage)

    accesstype = argv[0]
    newVersion = None
    sourcedir  = os.path.join(scriptcommon.OSOperations.scriptdir(), '..')

    if ( accesstype == 'get' ):
        if ( len(argv) > 1 ):
            sourcedir = argv[1]

        v = scriptcommon.Version(
            os.path.join(sourcedir, 'application/src/base/qlivecv.h'),
            r'(?:\s*#define LIVECV_VERSION_MAJOR)\s*([0-9]*)\s*\n'
             '(?:\s*#define LIVECV_VERSION_MINOR)\s*([0-9]*)\s*\n'
             '\s*(?:#define LIVECV_VERSION_PATCH)\s*([0-9]*)\s*')
        print(str(v.versionMajor) + '.' + str(v.versionMinor) + '.' + str(v.versionPatch))

    elif (accesstype == 'set' ):
        if ( len(argv) == 1 ):
            print(usage)
            sys.exit()

        newVersion = argv[1].split('.')
        if ( len(argv) > 2 ):
            sourcedir = argv[2]

        v = scriptcommon.Version(
            os.path.join(sourcedir, 'application/src/base/qlivecv.h'),
            r'(?:\s*#define LIVECV_VERSION_MAJOR)\s*([0-9]*)\s*\n'
             '(?:\s*#define LIVECV_VERSION_MINOR)\s*([0-9]*)\s*\n'
             '\s*(?:#define LIVECV_VERSION_PATCH)\s*([0-9]*)\s*')

        if ( len(newVersion) != 3 ):
            print("Unknown version:" + argv[1] + ' Version must be <major>.<minor>.<patch>')

        v.versionMajor = int(newVersion[0]);
        v.versionMinor = int(newVersion[1]);
        v.versionPatch  = int(newVersion[2]);
        print('Setting new version: ' + str(v.versionMajor) + '.' + str(v.versionMinor) + '.' + str(v.versionPatch))

        readmefile = os.path.join(sourcedir, 'README.md')
        savestructure = {
            readmefile: r'\s*(?:\* \*\*Version\*\*\:)\s*([0-9]*)\.{1}([0-9]*)\.{1}([0-9]*)\s*'
        }
        print(str(savestructure))
        v.save(savestructure)
        # v.save({
        #     readmefile: r'\s*(?:\* \*\*Version\*\*\:)\s*([0-9]*)\.{1}([0-9]*)\.{1}([0-9]*)\s*'
        # })
    else:
        print(usage)


if __name__ == "__main__":
   main(sys.argv[1:])
