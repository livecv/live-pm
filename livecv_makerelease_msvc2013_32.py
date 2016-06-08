import os
import io
import subprocess
import shutil
import scriptcommon
from subprocess import Popen

def makerelease_msvc2013_32():
	SOURCE_DIR  = scriptcommon.OSOperations.scriptdir() + '/..'
	RELEASE_DIR = scriptcommon.OSOperations.scriptdir() + '/../build/build-msvc2013-32'

	v = scriptcommon.Version(
		'../application/src/qlivecv.h',
		r'(?:\s*#define LIVECV_VERSION_MAJOR)\s*([0-9]*)\s*\n'
		 '(?:\s*#define LIVECV_VERSION_MINOR)\s*([0-9]*)\s*\n'
		 '\s*(?:#define LIVECV_VERSION_PATCH)\s*([0-9]*)\s*')

	print('Creating live cv release: version ' + str(v.versionMajor) + '.' + str(v.versionMinor) + '.' + str(v.versionPatch))

	buildname   = 'livecv-' + str(v.versionMajor) + '.' + str(v.versionMinor) + '.' + str(v.versionPatch) + '-msvc2013-x86'
	releasepath = RELEASE_DIR + '/../' + buildname + '/'

	if os.path.isdir(releasepath):
		shutil.rmtree(releasepath)
	os.makedirs(releasepath)

	print('Copying required files...')

	scriptcommon.OSOperations.copyFileStructure(releasepath, {
		os.path.join(os.environ['QT_DIR'], 'msvc2013/bin') : {
			'd3dcompiler_47.dll': '-',
			'icudt*.dll': '-',
			'icuin*.dll': '-',
			'icuuc*.dll': '-',
			'libEGL.dll': '-',
			'libGLESv2.dll': '-',
			'Qt*Core.dll': '-',
			'Qt*Network.dll': '-',
			'Qt*Qml.dll': '-',
			'Qt*Quick.dll': '-',
			'Qt*Script.dll': '-',
			'Qt*Gui.dll': '-',
			'Qt*Widgets.dll': '-',
			'Qt*WinExtras.dll': '-'
		},
		os.path.join(os.environ['QT_DIR'], 'msvc2013/plugins') : {
			'platforms/qwindows.dll': 'platforms/qwindows.dll'
		},
		os.path.join(os.environ['QT_DIR'], 'msvc2013/qml') : {
			'QtQuick' : {
				'Controls/qtquickcontrolsplugin.dll': 'plugins/QtQuick/Controls/-',
				'Controls/qmldir': 'plugins/QtQuick/Controls/-',
                'Controls/Styles/Flat/qtquickextrasflatplugin.dll' : 'plugins/QtQuick/Controls/Styles/Flat/-',
                'Controls/Styles/Flat/qmldir' : 'plugins/QtQuick/Controls/Styles/Flat/-',
				'Dialogs/dialogplugin.dll' : 'plugins/QtQuick/Dialogs/-',
				'Dialogs/qmldir': 'plugins/QtQuick/Dialogs/-',
                'Dialogs/Private/dialogsprivateplugin.dll' : 'plugins/QtQuick/Dialogs/Private/-',
                'Dialogs/Private/qmldir' : 'plugins/QtQuick/Dialogs/Private/-',
				'Layouts/qquicklayoutsplugin.dll': 'plugins/QtQuick/Layouts/-',
				'Layouts/qmldir': 'plugins/QtQuick/Layouts/-',
				'LocalStorage/qmllocalstorageplugin.dll': 'plugins/QtQuick/LocalStorage/-',
				'LocalStorage/qmldir': 'plugins/QtQuick/LocalStorage/-',
				'Particles.2/particlesplugin.dll': 'plugins/QtQuick/Particles.2/-',
				'Particles.2/qmldir': 'plugins/QtQuick/Particles.2/-',
				'PrivateWidgets/widgetsplugin.dll': 'plugins/QtQuick/PrivateWidgets/-',
				'PrivateWidgets/qmldir': 'plugins/QtQuick/PrivateWidgets/-',
				'Window.2/windowplugin.dll': 'plugins/QtQuick/Window.2/-',
				'Window.2/qmldir': 'plugins/QtQuick/Window.2/-',
				'XmlListModel/qmlxmllistmodelplugin.dll': 'plugins/QtQuick/XmlListModel/-',
				'XmlListModel/qmldir': 'plugins/QtQuick/XmlListModel/-',
			},
			'QtQuick.2' : {
				'qtquick2plugin.dll': 'plugins/QtQuick.2/-',
				'qmldir': 'plugins/QtQuick.2/-'
			},
			'Qt/labs' : {
				'folderlistmodel/qmlfolderlistmodelplugin.dll' : 'plugins/Qt/labs/folderlistmodel/-',
				'folderlistmodel/qmldir' : 'plugins/Qt/labs/folderlistmodel/-',
				'settings/qmlsettingsplugin.dll' : 'plugins/Qt/labs/settings/-',
				'settings/qmldir' : 'plugins/Qt/labs/settings/-'
			}
		},
		os.path.join(os.environ['VS120COMNTOOLS'], '../../VC/redist/x86/Microsoft.VC120.CRT') : {
			'msvcp120.dll': '-',
			'msvcr120.dll': '-'
		},
		scriptcommon.OSOperations.find('livecv.exe', RELEASE_DIR) : '-',
		scriptcommon.OSOperations.find('lcvlib.dll', RELEASE_DIR) : '-',
		os.path.dirname(scriptcommon.OSOperations.find('livecv.exe', RELEASE_DIR)) : {
			'opencv_*.dll': '-',
			'plugins': {
				'lcvcontrols': 'plugins/lcvcontrols',
				'lcvcore/lcvcore.dll': 'plugins/lcvcore/-',
				'lcvcore/qmldir': 'plugins/lcvcore/-',
				'lcvimgproc/lcvimgproc.dll': 'plugins/lcvimgproc/-',
				'lcvimgproc/qmldir': 'plugins/lcvimgproc/-',
				'lcvvideo/lcvvideo.dll': 'plugins/lcvvideo/-',
				'lcvvideo/qmldir': 'plugins/lcvvideo/-',
				'lcvfeatures2d/lcvfeatures2d.dll': 'plugins/lcvfeatures2d/-',
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
		scriptcommon.OSOperations.find('lcvlib.lib', SOURCE_DIR) : 'api/lib/-',
		
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
				
	shutil.make_archive(releasepath, "zip", RELEASE_DIR + '/../' + buildname)

	print(' * Generated: ' + buildname + '.zip')
	

if __name__ == '__main__':
	makerelease_msvc2013_32()

