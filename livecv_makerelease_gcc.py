import os
import io
import subprocess
import shutil
import scriptcommon
from subprocess import Popen

def makerelease_gcc():
	SOURCE_DIR  = scriptcommon.OSOperations.scriptdir() + '/..'
	RELEASE_DIR = scriptcommon.OSOperations.scriptdir() + '/../build/build-gcc'

	v = scriptcommon.Version(
		'../application/src/qlivecv.h',
		r'(?:\s*#define LIVECV_VERSION_MAJOR)\s*([0-9]*)\s*\n'
		 '(?:\s*#define LIVECV_VERSION_MINOR)\s*([0-9]*)\s*\n'
		 '\s*(?:#define LIVECV_VERSION_PATCH)\s*([0-9]*)\s*')

	print('Creating live cv release: version ' + str(v.versionMajor) + '.' + str(v.versionMinor) + '.' + str(v.versionPatch))

	buildname   = 'livecv-' + str(v.versionMajor) + '.' + str(v.versionMinor) + '.' + str(v.versionPatch) + '-gcc'
	releasepath = RELEASE_DIR + '/../' + buildname + '/'

	if os.path.isdir(releasepath):
		shutil.rmtree(releasepath)
	os.makedirs(releasepath)

	print('Copying required files...')

	scriptcommon.OSOperations.copyFileStructure(releasepath, {
		scriptcommon.OSOperations.find('livecv', RELEASE_DIR) : '-',
		os.path.dirname(scriptcommon.OSOperations.find('livecv', RELEASE_DIR)) : {
			'liblcvlib.so*': '-',
                        'liblcvlib.*': 'api/lib/-',
			'plugins': {
				'lcvcontrols': 'plugins/lcvcontrols',
				'lcvcore/liblcvcore.so': 'plugins/lcvcore/-',
				'lcvcore/qmldir': 'plugins/lcvcore/-',
				'lcvimgproc/liblcvimgproc.so': 'plugins/lcvimgproc/-',
				'lcvimgproc/qmldir': 'plugins/lcvimgproc/-',
				'lcvvideo/liblcvvideo.so': 'plugins/lcvvideo/-',
				'lcvvideo/qmldir': 'plugins/lcvvideo/-',
				'lcvfeatures2d/liblcvfeatures2d.so': 'plugins/lcvfeatures2d/-',
				'lcvfeatures2d/qmldir': 'plugins/lcvfeatures2d/-'
			}
		},
		scriptcommon.OSOperations.find('qlcvglobal.h', SOURCE_DIR) : 'api/include/-',
		scriptcommon.OSOperations.find('qmat.h', SOURCE_DIR) : 'api/include/-',
		scriptcommon.OSOperations.find('qmataccess.h', SOURCE_DIR) : 'api/include/-',
		scriptcommon.OSOperations.find('qmatdisplay.h', SOURCE_DIR) : 'api/include/-',
		scriptcommon.OSOperations.find('qmatfilter.h', SOURCE_DIR) : 'api/include/-',
		scriptcommon.OSOperations.find('qmatnode.h', SOURCE_DIR) : 'api/include/-',
		scriptcommon.OSOperations.find('qmatshader.h', SOURCE_DIR) : 'api/include/-',
		scriptcommon.OSOperations.find('qmatstate.h', SOURCE_DIR) : 'api/include/-',
		scriptcommon.OSOperations.find('qstatecontainer.h', SOURCE_DIR) : 'api/include/-',
		
		os.path.join(SOURCE_DIR, 'samples') : '-'
		
	})

	print('Creating include files...')

	def generateInclude(location, file, generated):
		hppf = open(os.path.join(location, generated), 'w')
		hppf.write('#include "' + file + '"\n')
		hppf.close()
		print(' * Generated: ' + generated + ' <-- ' + file)

	includepath = os.path.join(releasepath, 'api/include')
	generateInclude(includepath, 'qmat.h',            'QMat')
	generateInclude(includepath, 'qmataccess.h',      'QMatAccess')
	generateInclude(includepath, 'qmatdisplay.h',     'QMatDisplay')
	generateInclude(includepath, 'qmatfilter.h',      'QMatFilter')
	generateInclude(includepath, 'qmatnode.h',        'QMatNode')
	generateInclude(includepath, 'qmatshader.h',      'QMatShader')
	generateInclude(includepath, 'qmatstate.h',       'QMatState')
	generateInclude(includepath, 'qstatecontainer.h', 'QStateContainer')

	print('Removing junk...')

	for subdir, dirs, files in os.walk(releasepath):
		for file in files:
			filepath = os.path.join(subdir, file)
			if ( file == '.gitignore' ):
				os.remove(filepath)
				print(' * Removed:' + filepath)

	print('Creating archive...')
				
	shutil.make_archive(releasepath, "gztar", RELEASE_DIR + '/../' + buildname)

	print(' * Generated: ' + buildname + '.zip')
	

if __name__ == '__main__':
	makerelease_gcc()
