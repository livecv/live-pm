import sys
import os
import getopt
import platform
import shutil
import scriptcommon

deployStructure = {
    'gcc' : {
        '{release}/application' : {
            'livecv' : '-',
            'liblcveditor.so*' : '-',
            'libqmljsparser.so*' : '-',
            'liblcvlib.so*' : '-',
            'liblcvlib.*' : 'api/lib/-',
            'plugins' : {
                'lcvcontrols': 'plugins/lcvcontrols',
                'lcvcore': 'plugins/lcvcore',
                'lcvimgproc': 'plugins/lcvimgproc',
                'lcvvideo': 'plugins/lcvvideo/-',
                'lcvfeatures2d': 'plugins/lcvfeatures2d',
                'lcvphoto': 'plugins/lcvphoto'
            }
        },
        '{source}/lib/include' : {
            'qlcvglobal.h' : 'api/include/-',
            'qmat.h' : 'api/include/-',
            'qmataccess.h' : 'api/include/-',
            'qmatdisplay.h' : 'api/include/-',
            'qmatfilter.h' : 'api/include/-',
            'qmatnode.h' : 'api/include/-',
            'qmatshader.h' : 'api/include/-',
            'qmatstate.h' : 'api/include/-',
            'qstatecontainer.h' : 'api/include/-'
        },
        '{source}/samples' : '-'
    },
    'gcc_standalone' : {
        '{release}/application' : {
            'livecv' : '-',
            'liblcveditor.so*' : '-',
            'libqmljsparser.so*' : '-',
            'liblcvlib.so*' : '-',
            'plugins' : {
                'lcvcontrols': 'plugins/lcvcontrols',
                'lcvcore': 'plugins/lcvcore',
                'lcvimgproc': 'plugins/lcvimgproc',
                'lcvvideo': 'plugins/lcvvideo/-',
                'lcvfeatures2d': 'plugins/lcvfeatures2d',
                'lcvphoto': 'plugins/lcvphoto'
            },
        },
        '{source}/lib/include' : {
            'qlcvglobal.h' : 'api/include/-',
            'qmat.h' : 'api/include/-',
            'qmataccess.h' : 'api/include/-',
            'qmatdisplay.h' : 'api/include/-',
            'qmatfilter.h' : 'api/include/-',
            'qmatnode.h' : 'api/include/-',
            'qmatshader.h' : 'api/include/-',
            'qmatstate.h' : 'api/include/-',
            'qstatecontainer.h' : 'api/include/-'
        },
        '{source}/samples' : '-',
		'{qtbuild}/lib' : {
			'libQt5Core.so*': 'lib/-',
			'libQt5DBus.so*': 'lib/-',
			'libQt5Gui.so*': 'lib/-',
			'libQt5OpenGL.so*': 'lib/-',
			'libQt5Qml.so*': 'lib/-',
			'libQt5Quick.so*': 'lib/-',
			'libQt5Script.so*': 'lib/-',
			'libQt5Widgets.so*': 'lib/-',
			'libQt5Network.so*': 'lib/-',
        	'libQt5Xml.so*': '-',
			'libQt5XcbQpa.so*': 'lib/-',
			'libicudata.so*': 'lib/-',
			'libicui18n.so*': 'lib/-',
			'libicuio.so*': 'lib/-',
			'libicule.so*': 'lib/-',
			'libiculx.so*': 'lib/-',
			'libicutu.so*': 'lib/-',
			'libicuuc.so*': 'lib/-'
		},
		'{qtbuild}/plugins' : {
			'imageformats' : 'lib/plugins/imageformats',
			'platforminputcontexts' : 'lib/plugins/platforminputcontexts',
			'platforms' : 'lib/plugins/platforms',
			'platformthemes' : 'lib/plugins/platformthemes',
			'xcbglintegrations' : 'lib/plugins/xcbglintegrations'
		},
		'{qtbuild}/qml' : {
			'QtQuick' : {
				'Controls/libqtquickcontrolsplugin.so': 'plugins/QtQuick/Controls/-',
				'Controls/qmldir': 'plugins/QtQuick/Controls/-',
                'Controls/*.qmltypes': 'plugins/QtQuick/Controls/-',
				'Controls/Private' : 'plugins/QtQuick/Controls/Private',
				'Controls/Styles' : 'plugins/QtQuick/Controls/Styles',
				'Dialogs' : 'plugins/QtQuick/Dialogs',
				'Layouts': 'plugins/QtQuick/Layouts',
				'LocalStorage': 'plugins/QtQuick/LocalStorage',
				'Particles.2': 'plugins/QtQuick/Particles.2',
				'PrivateWidgets': 'plugins/QtQuick/PrivateWidgets',
				'Window.2': 'plugins/QtQuick/Window.2',
				'XmlListModel': 'plugins/QtQuick/XmlListModel'
			},
			'QtQuick.2' : 'plugins/QtQuick.2',
            'QtQml' : 'plugins/QtQml',
			'Qt' : 'plugins/Qt',
			'QtWebSockets' : 'plugins/-'
		},
		'{opencv_dir}' : {
			'libopencv_calib3d.so*' : '-',
			'libopencv_core.so*' : '-',
			'libopencv_features2d.so*' : '-',
            'libopencv_shape.so*' : '-',
			'libopencv_flann.so*' : '-',
			'libopencv_highgui.so*' : '-',
			'libopencv_imgproc.so*' : '-',
            'libopencv_imgcodecs.so*' : '-',
            'libopencv_objdetect.so*' : '-',
            'libopencv_stitching.so*' : '-',
            'libopencv_photo.so*' : '-',
            'libopencv_videoio.so*' : '-',
			'libopencv_video.so*' : '-'
		},
    },
    'msvc2013' : {
        '{qtbuild}/bin' : {
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
        '{qtbuild}/plugins' : {
        	'platforms/qwindows.dll': 'platforms/qwindows.dll'
        },
        '{qtbuild}/qml' : {
        	'QtQuick' : {
        		'Controls/qtquickcontrolsplugin.dll': 'plugins/QtQuick/Controls/-',
        		'Controls/qmldir': 'plugins/QtQuick/Controls/-',
        		'Controls/*.qmltypes': 'plugins/QtQuick/Controls/-',
                'Controls/Styles/Flat/qtquickextrasflatplugin.dll' : 'plugins/QtQuick/Controls/Styles/Flat/-',
                'Controls/Styles/Flat/qmldir' : 'plugins/QtQuick/Controls/Styles/Flat/-',
        		'Dialogs/dialogplugin.dll' : 'plugins/QtQuick/Dialogs/-',
        		'Dialogs/qmldir': 'plugins/QtQuick/Dialogs/-',
                'Dialogs/*.qmltypes': 'plugins/QtQuick/Dialogs/-',
                'Dialogs/Private/dialogsprivateplugin.dll' : 'plugins/QtQuick/Dialogs/Private/-',
                'Dialogs/Private/qmldir' : 'plugins/QtQuick/Dialogs/Private/-',
                'Dialogs/Private/*.qmltypes' : 'plugins/QtQuick/Dialogs/Private/-',
        		'Layouts/qquicklayoutsplugin.dll': 'plugins/QtQuick/Layouts/-',
        		'Layouts/qmldir': 'plugins/QtQuick/Layouts/-',
                'Layouts/*.qmltypes': 'plugins/QtQuick/Layouts/-',
        		'LocalStorage/qmllocalstorageplugin.dll': 'plugins/QtQuick/LocalStorage/-',
        		'LocalStorage/qmldir': 'plugins/QtQuick/LocalStorage/-',
                'LocalStorage/*.qmltypes': 'plugins/QtQuick/LocalStorage/-',
        		'Particles.2/particlesplugin.dll': 'plugins/QtQuick/Particles.2/-',
        		'Particles.2/qmldir': 'plugins/QtQuick/Particles.2/-',
                'Particles.2/*.qmltypes': 'plugins/QtQuick/Particles.2/-',
        		'PrivateWidgets/widgetsplugin.dll': 'plugins/QtQuick/PrivateWidgets/-',
        		'PrivateWidgets/qmldir': 'plugins/QtQuick/PrivateWidgets/-',
                'PrivateWidgets/*.qmltypes': 'plugins/QtQuick/PrivateWidgets/-',
        		'Window.2/windowplugin.dll': 'plugins/QtQuick/Window.2/-',
        		'Window.2/qmldir': 'plugins/QtQuick/Window.2/-',
                'Window.2/*.qmltypes': 'plugins/QtQuick/Window.2/-',
        		'XmlListModel/qmlxmllistmodelplugin.dll': 'plugins/QtQuick/XmlListModel/-',
        		'XmlListModel/qmldir': 'plugins/QtQuick/XmlListModel/-',
                'XmlListModel/*.qmltypes': 'plugins/QtQuick/XmlListModel/-'
        	},
        	'QtQuick.2' : {
        		'qtquick2plugin.dll': 'plugins/QtQuick.2/-',
        		'qmldir': 'plugins/QtQuick.2/-',
        		'*.qmltypes': 'plugins/QtQuick.2/-'
        	},
        	'Qt/labs' : {
        		'folderlistmodel/qmlfolderlistmodelplugin.dll' : 'plugins/Qt/labs/folderlistmodel/-',
        		'folderlistmodel/qmldir' : 'plugins/Qt/labs/folderlistmodel/-',
        		'folderlistmodel/*.qmltypes' : 'plugins/Qt/labs/folderlistmodel/-',
        		'settings/qmlsettingsplugin.dll' : 'plugins/Qt/labs/settings/-',
                'settings/*.qmltypes' : 'plugins/Qt/labs/settings/-',
        		'settings/qmldir' : 'plugins/Qt/labs/settings/-'
        	}
        },
        '{vs120comntools}/../../VC/redist/x64/Microsoft.VC120.CRT' : {
        	'msvcp120.dll': '-',
        	'msvcr120.dll': '-'
        },
        '{release}/application/release/livecv.exe' : '-',
        '{release}/application/release/lcvlib.dll' : '-',
        '{release}/application/release/lcveditor.dll' : '-',
        '{release}/application/release/qmljsparser.dll' : '-',
        '{release}/application/release' : {
        	'opencv_*.dll': '-',
        	'plugins': {
        		'lcvcontrols': 'plugins/lcvcontrols',
        		'lcvcore/lcvcore.dll': 'plugins/lcvcore/-',
        		'lcvcore/qmldir': 'plugins/lcvcore/-',
        		'lcvcore/*.qmltypes': 'plugins/lcvcore/-',
        		'lcvimgproc/lcvimgproc.dll': 'plugins/lcvimgproc/-',
        		'lcvimgproc/qmldir': 'plugins/lcvimgproc/-',
        		'lcvimgproc/*.qmltypes': 'plugins/lcvimgproc/-',
        		'lcvvideo/lcvvideo.dll': 'plugins/lcvvideo/-',
        		'lcvvideo/qmldir': 'plugins/lcvvideo/-',
        		'lcvvideo/*.qmltypes': 'plugins/lcvvideo/-',
        		'lcvfeatures2d/lcvfeatures2d.dll': 'plugins/lcvfeatures2d/-',
        		'lcvfeatures2d/*.qmltypes': 'plugins/lcvfeatures2d/-',
        		'lcvfeatures2d/qmldir': 'plugins/lcvfeatures2d/-',
        		'lcvphoto/lcvphoto.dll': 'plugins/lcvphoto/-',
        		'lcvphoto/*.qmltypes': 'plugins/lcvphoto/-',
        		'lcvphoto/qmldir': 'plugins/lcvphoto/-'
        	}
        },
        '{source}/lib/include' : {
            'qlcvglobal.h' : 'api/include/-',
            'qmat.h' : 'api/include/-',
            'qmataccess.h' : 'api/include/-',
            'qmatdisplay.h' : 'api/include/-',
            'qmatfilter.h' : 'api/include/-',
            'qmatnode.h' : 'api/include/-',
            'qmatshader.h' : 'api/include/-',
            'qmatstate.h' : 'api/include/-',
            'qstatecontainer.h' : 'api/include/-'
        },
        '{release}/lib/release/lcvlib.lib': 'api/lib/-',
        '{source}/samples' : '-'
    },
    'msvc2013_64' : {
        '{qtbuild}/bin' : {
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
        '{qtbuild}/plugins' : {
        	'platforms/qwindows.dll': 'platforms/qwindows.dll'
        },
        '{qtbuild}/qml' : {
        	'QtQuick' : {
        		'Controls/qtquickcontrolsplugin.dll': 'plugins/QtQuick/Controls/-',
        		'Controls/qmldir': 'plugins/QtQuick/Controls/-',
        		'Controls/*.qmltypes': 'plugins/QtQuick/Controls/-',
                'Controls/Styles/Flat/qtquickextrasflatplugin.dll' : 'plugins/QtQuick/Controls/Styles/Flat/-',
                'Controls/Styles/Flat/qmldir' : 'plugins/QtQuick/Controls/Styles/Flat/-',
        		'Dialogs/dialogplugin.dll' : 'plugins/QtQuick/Dialogs/-',
        		'Dialogs/qmldir': 'plugins/QtQuick/Dialogs/-',
                'Dialogs/*.qmltypes': 'plugins/QtQuick/Dialogs/-',
                'Dialogs/Private/dialogsprivateplugin.dll' : 'plugins/QtQuick/Dialogs/Private/-',
                'Dialogs/Private/qmldir' : 'plugins/QtQuick/Dialogs/Private/-',
                'Dialogs/Private/*.qmltypes' : 'plugins/QtQuick/Dialogs/Private/-',
        		'Layouts/qquicklayoutsplugin.dll': 'plugins/QtQuick/Layouts/-',
        		'Layouts/qmldir': 'plugins/QtQuick/Layouts/-',
                'Layouts/*.qmltypes': 'plugins/QtQuick/Layouts/-',
        		'LocalStorage/qmllocalstorageplugin.dll': 'plugins/QtQuick/LocalStorage/-',
        		'LocalStorage/qmldir': 'plugins/QtQuick/LocalStorage/-',
                'LocalStorage/*.qmltypes': 'plugins/QtQuick/LocalStorage/-',
        		'Particles.2/particlesplugin.dll': 'plugins/QtQuick/Particles.2/-',
        		'Particles.2/qmldir': 'plugins/QtQuick/Particles.2/-',
                'Particles.2/*.qmltypes': 'plugins/QtQuick/Particles.2/-',
        		'PrivateWidgets/widgetsplugin.dll': 'plugins/QtQuick/PrivateWidgets/-',
        		'PrivateWidgets/qmldir': 'plugins/QtQuick/PrivateWidgets/-',
                'PrivateWidgets/*.qmltypes': 'plugins/QtQuick/PrivateWidgets/-',
        		'Window.2/windowplugin.dll': 'plugins/QtQuick/Window.2/-',
        		'Window.2/qmldir': 'plugins/QtQuick/Window.2/-',
                'Window.2/*.qmltypes': 'plugins/QtQuick/Window.2/-',
        		'XmlListModel/qmlxmllistmodelplugin.dll': 'plugins/QtQuick/XmlListModel/-',
        		'XmlListModel/qmldir': 'plugins/QtQuick/XmlListModel/-',
                'XmlListModel/*.qmltypes': 'plugins/QtQuick/XmlListModel/-'
        	},
        	'QtQuick.2' : {
        		'qtquick2plugin.dll': 'plugins/QtQuick.2/-',
        		'qmldir': 'plugins/QtQuick.2/-',
        		'*.qmltypes': 'plugins/QtQuick.2/-'
        	},
        	'Qt/labs' : {
        		'folderlistmodel/qmlfolderlistmodelplugin.dll' : 'plugins/Qt/labs/folderlistmodel/-',
        		'folderlistmodel/qmldir' : 'plugins/Qt/labs/folderlistmodel/-',
        		'folderlistmodel/*.qmltypes' : 'plugins/Qt/labs/folderlistmodel/-',
        		'settings/qmlsettingsplugin.dll' : 'plugins/Qt/labs/settings/-',
                'settings/*.qmltypes' : 'plugins/Qt/labs/settings/-',
        		'settings/qmldir' : 'plugins/Qt/labs/settings/-'
        	}
        },
        '{vs120comntools}/../../VC/redist/x64/Microsoft.VC120.CRT' : {
        	'msvcp120.dll': '-',
        	'msvcr120.dll': '-'
        },
        '{release}/application/release/livecv.exe' : '-',
        '{release}/application/release/lcvlib.dll' : '-',
        '{release}/application/release/lcveditor.dll' : '-',
        '{release}/application/release/qmljsparser.dll' : '-',
        '{release}/application/release' : {
        	'opencv_*.dll': '-',
        	'plugins': {
        		'lcvcontrols': 'plugins/lcvcontrols',
        		'lcvcore/lcvcore.dll': 'plugins/lcvcore/-',
        		'lcvcore/qmldir': 'plugins/lcvcore/-',
        		'lcvcore/*.qmltypes': 'plugins/lcvcore/-',
        		'lcvimgproc/lcvimgproc.dll': 'plugins/lcvimgproc/-',
        		'lcvimgproc/qmldir': 'plugins/lcvimgproc/-',
        		'lcvimgproc/*.qmltypes': 'plugins/lcvimgproc/-',
        		'lcvvideo/lcvvideo.dll': 'plugins/lcvvideo/-',
        		'lcvvideo/qmldir': 'plugins/lcvvideo/-',
        		'lcvvideo/*.qmltypes': 'plugins/lcvvideo/-',
        		'lcvfeatures2d/lcvfeatures2d.dll': 'plugins/lcvfeatures2d/-',
        		'lcvfeatures2d/*.qmltypes': 'plugins/lcvfeatures2d/-',
        		'lcvfeatures2d/qmldir': 'plugins/lcvfeatures2d/-',
        		'lcvphoto/lcvphoto.dll': 'plugins/lcvphoto/-',
        		'lcvphoto/*.qmltypes': 'plugins/lcvphoto/-',
        		'lcvphoto/qmldir': 'plugins/lcvphoto/-'
        	}
        },
        '{source}/lib/include' : {
            'qlcvglobal.h' : 'api/include/-',
            'qmat.h' : 'api/include/-',
            'qmataccess.h' : 'api/include/-',
            'qmatdisplay.h' : 'api/include/-',
            'qmatfilter.h' : 'api/include/-',
            'qmatnode.h' : 'api/include/-',
            'qmatshader.h' : 'api/include/-',
            'qmatstate.h' : 'api/include/-',
            'qstatecontainer.h' : 'api/include/-'
        },
        '{release}/lib/release/lcvlib.lib': 'api/lib/-',
        '{source}/samples' : '-'
	}
}

def build(compiler = None, bits = None, sourcedir = None, deployid = None):
    if ( bits == None ):
        bits = '64' if sys.maxsize > 2**32 else 32
    if (compiler is None):
        if ( sys.platform.lower().startswith("win")):
            compiler = 'msvc2013' + ('_64' if bits == '64' else '')
        else:
            compiler = 'gcc' + ('_64' if bits == '64' else '')
    if ( deployid is None):
        deployid = compiler

    if ( not 'QTDIR' in os.environ ):
        raise Exception("QTDIR environment variable has not been set.")

    if ( not 'OPENCV_DIR' in os.environ and compiler.startswith('msvc')):
        raise Exception("OPENCV_DIR environment variable has not been set.")

    if (sourcedir == None):
        sourcedir = scriptcommon.OSOperations.scriptdir() + '/..'

    if ( not os.path.exists(sourcedir) ):
        raise Exception("Source directory does not exist: " + sourcedir)

    releasedir = sourcedir + '/build/' + compiler
    if ( not os.path.exists(releasedir) ):
        raise Exception("Release path does not exist: " + releasedir + '. Make sure to build livecv first.')

    print('Packaging Live CV')
    print('Compiler: ' + compiler)
    print('Source: ' + sourcedir)

    print('Acquiring version...')

    v = scriptcommon.Version(
        os.path.join(sourcedir, 'application/src/base/qlivecv.h'),
        r'(?:\s*#define LIVECV_VERSION_MAJOR)\s*([0-9]*)\s*\n'
         '(?:\s*#define LIVECV_VERSION_MINOR)\s*([0-9]*)\s*\n'
         '\s*(?:#define LIVECV_VERSION_PATCH)\s*([0-9]*)\s*')

    versionstring = str(v.versionMajor) + '.' + str(v.versionMinor) + '.' + str(v.versionPatch)
    print('Version: ' + versionstring)

    buildname = 'livecv-' + versionstring + '-' + deployid.replace('_64', '').replace('_', '-') + ('-x64' if bits == '64' else '-x86')
    packagedir = releasedir + '/../' + buildname
    packagedirroot = packagedir + '/livecv/'

    if (os.path.isdir(packagedir)):
        shutil.rmtree(packagedir)
    os.makedirs(packagedirroot)

    print('Copying required files...')

    qtbuild = os.path.join(os.environ['QTDIR'], '../' + compiler)

    scriptcommon.OSOperations.copyFileStructure(packagedirroot, deployStructure[deployid], {
        'qtbuild': qtbuild,
        'qtdir': os.environ['QTDIR'],
        'opencv_dir': os.environ['OPENCV_DIR'],
        'source': sourcedir,
        'release': releasedir,
        'vs120comntools': os.environ.get('VS120COMNTOOLS', '')
    })

    print('Creating include files...')

    def generateInclude(location, file, generated):
        hppf = open(os.path.join(location, generated), 'w')
        hppf.write('#include "' + file + '"\n')
        hppf.close()
        print(' * Generated: ' + generated + ' <-- ' + file)

    includepath = os.path.join(packagedirroot, 'api/include')
    generateInclude(includepath, 'qmat.h',            'QMat')
    generateInclude(includepath, 'qmataccess.h',      'QMatAccess')
    generateInclude(includepath, 'qmatdisplay.h',     'QMatDisplay')
    generateInclude(includepath, 'qmatfilter.h',      'QMatFilter')
    generateInclude(includepath, 'qmatnode.h',        'QMatNode')
    generateInclude(includepath, 'qmatshader.h',      'QMatShader')
    generateInclude(includepath, 'qmatstate.h',       'QMatState')
    generateInclude(includepath, 'qstatecontainer.h', 'QStateContainer')

    if ( 'gcc' in compiler ):
        print('Setting file permissions...')
        os.chmod(os.path.join(packagedirroot, 'livecv'), 0o755)
        if ( 'standalone' in deployid ):
            print('Generating launcher...')
            launcherf = open(os.path.join(packagedirroot, 'launcher.sh'), 'w')
            launcherf.write('#!/bin/bash\n' +
            		'export LD_LIBRARY_PATH=`pwd`/lib:\n' +
            		'export QML_IMPORT_PATH=`pwd`/plugins\n' +
            		'export QML2_IMPORT_PATH=`pwd`/plugins\n' +
            		'export QT_PLUGIN_PATH=`pwd`/lib/plugins\n' +
            		'export QT_QPA_PLATFORM_PLUGIN_PATH=`pwd`/lib/plugins/platforms\n' +
            		'./livecv')
            launcherf.close()
            os.chmod(os.path.join(packagedirroot, 'launcher.sh'), 0o755)
            print(' * Generated launcher.sh')


    print('Removing junk...')

    for subdir, dirs, files in os.walk(packagedirroot):
        for file in files:
            filepath = os.path.join(subdir, file)
            if ( file == '.gitignore' ):
                os.remove(filepath)
                print(' * Removed:' + filepath)

    print('Creating archive...')
    if ( sys.platform.lower().startswith("win") ):
        shutil.make_archive(packagedirroot + '/..', "zip", packagedir)
    	print(' * Generated: ' + buildname + '.zip')
    else:
        shutil.make_archive(packagedirroot, "gztar", packagedirroot)
    	print(' * Generated: ' + buildname + '.tar.gz')


def main(argv):
    try:
        compiler  = None
        osbit     = None
        sourcedir = None
        deployid  = None

        usage = 'Usage: livecv_deploy.py [-c <compiler> -b <platform:32 or 64> -s <source-dir> -d <deployid>]'

        try:
            opts, args = getopt.getopt(argv,"hc:b:s:d:")
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
                elif ( opt == '-d'):
                    deployid = arg

            build(compiler, osbit, sourcedir, deployid)

        except getopt.GetoptError:
            print(usage)
            sys.exit(2)

    except Exception as err:
        print("Cannot deploy project due to the following exception:\n Exception: " + str(err))
	sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])
