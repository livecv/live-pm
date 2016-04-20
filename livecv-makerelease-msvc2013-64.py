import os
import io
import subprocess
import shutil
import scriptcommon
from subprocess import Popen

SOURCE_DIR  = scriptcommon.OSOperations.scriptdir() + '/..'
RELEASE_DIR = scriptcommon.OSOperations.scriptdir() + '/../build/build-msvc2013-64'

v = scriptcommon.Version(
    '../application/src/qlivecv.h',
    r'(?:\s*#define LIVECV_VERSION_MAJOR)\s*([0-9]*)\s*\n'
     '(?:\s*#define LIVECV_VERSION_MINOR)\s*([0-9]*)\s*\n'
     '\s*(?:#define LIVECV_VERSION_PATCH)\s*([0-9]*)\s*')


buildname   = 'livecv-' + str(v.versionMajor) + '.' + str(v.versionMinor) + '.' + str(v.versionPatch) + '-msvc2013-x64'
releasepath = RELEASE_DIR + '/../' + buildname + '/'

if os.path.isdir(releasepath):
    shutil.rmtree(releasepath)
os.makedirs(releasepath)


scriptcommon.OSOperations.copyFileStructure(releasepath, {
    os.path.join(os.environ['QT_DIR'], 'msvc2013_64/bin') : {
        'icudt*.dll': '-',
        'icuin*.dll': '-',
        'icuuc*.dll': '-',
		'libmysql.dll': '-',
        'Qt*Core.dll': '-',
		'Qt*Sql.dll': '-',
		'Qt*Network.dll': '-',
		'Qt*Gui.dll': '-',
		'Qt*Widgets.dll': '-',
		'libEGL.dll': '-',
		'libGLESv2.dll' : '-',
    },
	os.path.join(os.environ['QT_DIR'], 'msvc2013_64/plugins/sqldrivers/qsqlmysql.dll'): 'sqldrivers/qsqlmysql.dll',
	os.path.join(os.environ['OPENCV_DIR'], 'bin') : {
        'opencv_core2410.dll': '-',
        'opencv_imgproc2410.dll': '-',
        'opencv_highgui2410.dll': '-'
    },
    os.path.join(os.environ['VS120COMNTOOLS'], '../../VC/redist/x64/Microsoft.VC120.CRT') : {
        'msvcp120.dll': '-',
        'msvcr120.dll': '-'
    },
    scriptcommon.OSOperations.find('livecv.exe', RELEASE_DIR) : '-'
})

shutil.make_archive(releasepath, "zip", RELEASE_DIR + '/../' + buildname)


