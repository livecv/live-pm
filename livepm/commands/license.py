import os
import sys
import io
import json
import argparse
import re

from livepm.lib.command import Command
from livepm.lib.filesystem import FileSystem

class LicenseCommand(Command):
    name = 'license'
    description = 'Update licenses based on an license index file.'

    def __init__(self):
        pass

    def parse_args(self, argv):
        parser = argparse.ArgumentParser(description = LicenseCommand.description)
        parser.add_argument('license_file', default='', help="Path to the license index file.")
        parser.add_argument('source', default='', help="Path to the source code.")
        
        args = parser.parse_args(argv)

        self.sourcedir = os.path.abspath(args.source)
        self.license_file = os.path.abspath(args.license_file)

    def __call__(self):
        with open(self.license_file) as jsonfile:
            licensejson = json.load(jsonfile)

        self.extensions = licensejson['extensions']
        self.oldlicense = licensejson['replace'] if 'replace' in licensejson else ''
        self.paths      = licensejson['paths']

        license    = licensejson['license']
        if ( isinstance(license, list)):
            self.license = ''
            for val in license:
                self.license += val + '\n'
        else:
            self.license = license

        for path in self.paths:
            sourcepath = os.path.join(self.sourcedir, path)
            self.update(sourcepath, self.license, self.oldlicense)

    def update(self, sourcepath, newlicense, oldlicense = ''):
        for subdir, dirs, files in os.walk(sourcepath):
            for file in files:
                filename, fileextension = os.path.splitext(subdir + '/' + file)
                if ( len(fileextension) > 0 ):
                    if ( fileextension[0] == '.' ):
                        fileextension = fileextension[1:]
                    if any(fileextension in s for s in self.extensions):
                        if( oldlicense != '' ):
                            self.replacelicense(subdir + '/' + file, newlicense, oldlicense)
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
        print('Added license to ' + file)

    def replacelicense(self, file, newlicense, oldlicense):
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
            print('Updated license in ' + file)
        else:
            fileresw = open(file, 'w')
            fileresw.write(newlicense + '\n\n' + filecontents)
            fileresw.close()
            print('Added license to ' + file)
