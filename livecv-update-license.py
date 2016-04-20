import os
import io
import scriptcommon

SOURCE_DIR_APPLICATION = scriptcommon.OSOperations.scriptdir() + '/../application'
SOURCE_DIR_LIB         = scriptcommon.OSOperations.scriptdir() + '/../lib'
SOURCE_DIR_PLUGINS     = scriptcommon.OSOperations.scriptdir() + '/../plugins'
SOURCE_DIR_TESTS       = scriptcommon.OSOperations.scriptdir() + '/../tests'

NEW_LICENSE = str('/****************************************************************************\n'
			'**\n'
			'** Copyright (C) 2014-2016 Dinu SV.\n'
			'** (contact: mail@dinusv.com)\n'
			'** This file is part of Live CV Application.\n'
			'**\n'
			'** GNU Lesser General Public License Usage\n'
			'** This file may be used under the terms of the GNU Lesser\n'
			'** General Public License version 3 as published by the Free Software\n'
			'** Foundation and appearing in the file LICENSE.LGPLv3 included in the\n'
			'** packaging of this file. Please review the following information to\n'
			'** ensure the GNU Lesser General Public License version 3 requirements\n'
			'** will be met: https://www.gnu.org/licenses/lgpl.html.\n'
			'**\n'
			'****************************************************************************/')
	
OLD_LICENSE = '\/\*{20,}.*Copyright\s\(C\)\s2014\sDinu\sSV.*\*{20,}\/'

license = scriptcommon.License(SOURCE_DIR_APPLICATION, ['h', 'hpp', 'cpp', 'qml', 'js'])
license.update(NEW_LICENSE, OLD_LICENSE)
license = scriptcommon.License(SOURCE_DIR_LIB, ['h', 'hpp', 'cpp', 'qml', 'js'])
license.update(NEW_LICENSE, OLD_LICENSE)
license = scriptcommon.License(SOURCE_DIR_PLUGINS, ['h', 'hpp', 'cpp', 'qml', 'js'])
license.update(NEW_LICENSE, OLD_LICENSE)
license = scriptcommon.License(SOURCE_DIR_TESTS, ['h', 'hpp', 'cpp', 'qml', 'js'])
license.update(NEW_LICENSE, OLD_LICENSE)