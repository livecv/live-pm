import os
import sys
import io
import re

class License:
	def __init__(self, sourcedir, extensions):
		self.sourcedir  = sourcedir
		self.extensions = extensions

	def update(self, newlicense, oldlicense = ''):
		for subdir, dirs, files in os.walk(self.sourcedir):
			for file in files:
				filename, fileextension = os.path.splitext(subdir + '/' + file)
				if ( len(fileextension) > 0 ):
					if ( fileextension[0] == '.' ):
						fileextension = fileextension[1:]
					if any(fileextension in s for s in self.extensions):
						if( oldlicense != '' ):
							self.updatelicense(subdir + '/' + file, newlicense, oldlicense)
						else:
							self.addlicense(subdir + '/' + file, newlicense)

	def addlicense(self, file, license):
		fileresr = open(file, 'r')
		filecontents = fileresr.read()
		if(filecontents.find(license) != -1):
			fileresr.close()
			return

		fileresw = open(file, 'w')
		fileresw.write(license + '\n\n' + filecontents)
		fileresw.close()
		print('Added license to ' + file + '\n')

	def updatelicense(self, file, newlicense, oldlicense):
		fileresr = open(file, 'r')
		filecontents = fileresr.read()
		if(filecontents.find(newlicense) != -1):
			fileresr.close()
			return

		licensetext = re.search(oldlicense, filecontents, re.DOTALL)
		if ( licensetext ):
			filecontents = filecontents.replace(licensetext.group(0), newlicense)
			fileresw = open(file, 'w')
			fileresw.write(filecontents)
			fileresw.close()
			print('Updated license in ' + file + '\n')
		else:
			fileresw = open(file, 'w')
			fileresw.write(newlicense + '\n\n' + filecontents)
			fileresw.close()
			print('Added license to ' + file + '\n')
