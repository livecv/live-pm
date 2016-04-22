import os
import io
import subprocess
import shutil
import scriptcommon
from subprocess import Popen

def find_opencv():
	p = subprocess.Popen(['pkg-config', '--libs-only-L', 'opencv'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	out, err = p.communicate()
	strippedout = out.decode('utf-8').strip()
	if ( strippedout.startswith('-L') ):
		return strippedout[2:]
	return stripepdout

def makerelease_gcc():
	SOURCE_DIR  = scriptcommon.OSOperations.scriptdir() + '/..'
	RELEASE_DIR = scriptcommon.OSOperations.scriptdir() + '/../build/build-gcc'

	v = scriptcommon.Version(
		'../application/src/qlivecv.h',
		r'(?:\s*#define LIVECV_VERSION_MAJOR)\s*([0-9]*)\s*\n'
		 '(?:\s*#define LIVECV_VERSION_MINOR)\s*([0-9]*)\s*\n'
		 '\s*(?:#define LIVECV_VERSION_PATCH)\s*([0-9]*)\s*')

	print('Creating live cv release: version ' + str(v.versionMajor) + '.' + str(v.versionMinor) + '.' + str(v.versionPatch))

	buildname   = 'livecv-' + str(v.versionMajor) + '.' + str(v.versionMinor) + '.' + str(v.versionPatch) + '-gcc-launcher'
	releasepath = RELEASE_DIR + '/../' + buildname + '/livecv/'

	if os.path.isdir(RELEASE_DIR + '/../' + buildname):
		shutil.rmtree(RELEASE_DIR + '/../' + buildname)
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
		os.path.join(os.environ['QTDIR'], 'lib') : {
			'libQt5Core.so*': 'lib/-',
			'libQt5DBus.so*': 'lib/-',
			'libQt5Gui.so*': 'lib/-',
			'libQt5OpenGL.so*': 'lib/-',
			'libQt5Qml.so*': 'lib/-',
			'libQt5Quick.so*': 'lib/-',
			'libQt5Script.so*': 'lib/-',
			'libQt5Widgets.so*': 'lib/-',
			'libQt5Network.so*': 'lib/-',
			'libicudata.so*': 'lib/-',
			'libicui18n.so*': 'lib/-',
			'libicuio.so*': 'lib/-',
			'libicule.so*': 'lib/-',
			'libiculx.so*': 'lib/-',
			'libicutu.so*': 'lib/-',
			'libicuuc.so*': 'lib/-'
		},
		os.path.join(os.environ['QTDIR'], 'plugins') : {
			'imageformats' : 'lib/plugins/imageformats',
			'platforminputcontexts' : 'lib/plugins/platforminputcontexts',
			'platforms' : 'lib/plugins/platforms',
			'platformthemes' : 'lib/plugins/platformthemes'
		},
		os.path.join(os.environ['QTDIR'], 'qml') : {
			'QtQuick' : {
				'Controls/libqtquickcontrolsplugin.so': 'plugins/QtQuick/Controls/-',
				'Controls/qmldir': 'plugins/QtQuick/Controls/-',
				'Controls/Private' : 'plugins/QtQuick/Controls/Private',
				'Controls/Styles' : 'plugins/QtQuick/Controls/Styles',
				'Dialogs/libdialogplugin.so' : 'plugins/QtQuick/Dialogs/-',
				'Dialogs/qmldir': 'plugins/QtQuick/Dialogs/-',
				'Dialogs/Private/libdialogsprivateplugin.so' : 'plugins/QtQuick/Dialogs/Private/-',
				'Dialogs/Private/qmldir' : 'plugins/QtQuick/Dialogs/Private/-',
				'Layouts/libqquicklayoutsplugin.so': 'plugins/QtQuick/Layouts/-',
				'Layouts/qmldir': 'plugins/QtQuick/Layouts/-',
				'LocalStorage/libqmllocalstorageplugin.so': 'plugins/QtQuick/LocalStorage/-',
				'LocalStorage/qmldir': 'plugins/QtQuick/LocalStorage/-',
				'Particles.2/libparticlesplugin.so': 'plugins/QtQuick/Particles.2/-',
				'Particles.2/qmldir': 'plugins/QtQuick/Particles.2/-',
				'PrivateWidgets/libwidgetsplugin.so': 'plugins/QtQuick/PrivateWidgets/-',
				'PrivateWidgets/qmldir': 'plugins/QtQuick/PrivateWidgets/-',
				'Window.2/libwindowplugin.so': 'plugins/QtQuick/Window.2/-',
				'Window.2/qmldir': 'plugins/QtQuick/Window.2/-',
				'XmlListModel/libqmlxmllistmodelplugin.so': 'plugins/QtQuick/XmlListModel/-',
				'XmlListModel/qmldir': 'plugins/QtQuick/XmlListModel/-',
			},
			'QtQuick.2' : {
				'libqtquick2plugin.so': 'plugins/QtQuick.2/-',
				'qmldir': 'plugins/QtQuick.2/-'
			},
			'Qt' : {
				'labs/folderlistmodel/libqmlfolderlistmodelplugin.so' : 'plugins/Qt/labs/folderlistmodel/-',
				'labs/folderlistmodel/qmldir' : 'plugins/Qt/labs/folderlistmodel/-',
				'labs/settings/libqmlsettingsplugin.so' : 'plugins/Qt/labs/settings/-',
				'labs/settings/qmldir' : 'plugins/Qt/labs/settings/-',
				'WebSockets/libdeclarative_qmlwebsockets.so': 'plugins/Qt/WebSockets/-',
				'WebSockets/qmldir' : 'plugins/Qt/WebSockets/-'
			}
		},
		find_opencv() : {
			'libopencv_calib3d.so*' : 'lib/-',
			'libopencv_core.so*' : 'lib/-',
			'libopencv_features2d.so*' : 'lib/-',
			'libopencv_flann.so*' : 'lib/-',
			'libopencv_highgui.so*' : 'lib/-',
			'libopencv_imgproc.so*' : 'lib/-',
			'libopencv_video.so*' : 'lib/-'
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
        
	print('Generating launcher...')

	launcherf = open(os.path.join(releasepath, 'launcher.sh'), 'w')
	launcherf.write('#!/bin/bash\n' + 
			'export LD_LIBRARY_PATH=`pwd`/lib\n' + 
			'export QML_IMPORT_PATH=`pwd`/plugins\n' + 
			'export QML2_IMPORT_PATH=`pwd`/plugins\n' + 
			'export QT_PLUGIN_PATH=`pwd`/lib/plugins\n' +
			'export QT_QPA_PLATFORM_PLUGIN_PATH=`pwd`/lib/plugins/platforms\n' + 
			'./livecv')
	launcherf.close()
	print(' * Generated launcher.sh')


	print('Removing junk...')

	for subdir, dirs, files in os.walk(releasepath):
		for file in files:
			filepath = os.path.join(subdir, file)
			if ( file == '.gitignore' ):
				os.remove(filepath)
				print(' * Removed:' + filepath)

	print('Creating archive...')
				
	shutil.make_archive(RELEASE_DIR + '/../' + buildname, "gztar", RELEASE_DIR + '/../' + buildname)

	print(' * Generated: ' + buildname + '.tar.gz')
	

if __name__ == '__main__':
	makerelease_gcc()
