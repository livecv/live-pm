import sys
import os
import getopt
import json
import shutil
import argparse
import requests as re
import zipfile
from livepm.lib.command import Command
from livepm.lib.configuration import Configuration

server_url = "urlhere"

class InstallCommand(Command):

    name = 'install'
    description = 'Install a live package'

    def __init__(self):
        pass

    def parse_args(self, argv):
        parser = argparse.ArgumentParser(description='Install a live package')
        parser.add_argument('--name', '-n', default=None, help='Name of the package')
        parser.add_argument('--release', '-r', default=None, help='Package release')
        parser.add_argument('--server_url', '-sU', default=server_url, help='Change server url.')
        parser.add_argument('--livekeys_dir', '-d' ,default=False, action='store_true', help="Installation directory")

        args = parser.parse_args(argv)

        self.name   = args.name
        self.release   = args.release
        self.server_url   = args.server_url
        self.livekeys_dir = os.environ['LIVEKEYS_DIR'] if args.livekeys_dir else os.getcwd()
    
    def __call__(self):

        # Check the livekeys env variable
        try:
            os.environ["LIVEKEYS_DIR"]
        except KeyError:
            print("Enviroment variable not set.")
            sys.exit(1)

        # Construct url
        url = self.server_url + '/package/' + self.name + '/latest/' + self.release
        # Send request
        r = re.get(url, allow_redirects=True)
        
        # Check the url
        if r.ok:
            # Create a folder for package
            os.mkdir(self.livekeys_dir + '/' + self.name)

            jsonResponse = json.loads(r.text)
            
            # Request the zip file
            getZip = re.get(jsonResponse['url'])
            
            # Read dependencies
            versions = jsonResponse['dependencies']

            # Download main package
            package_path = self.livekeys_dir + '/' + self.name + '/' + self.name + '-' + jsonResponse['version']
            open( package_path + '.zip', 'wb').write(getZip.content)

            # unzip main package and remove zip file
            zipPath = (package_path + '.zip')
            zip = zipfile.ZipFile(zipPath)
            zip.extractall(package_path)
            zip.close()
            os.remove(package_path + '.zip')
    
            # Dependency recursive download
            def downloadDependencies(versions):
                
                for i in versions:

                    version = i['version']
                    packageName = i['package']
                    dependencyUrl = i['url']
                    dependencyPath = self.livekeys_dir + '/' + self.name + '/' + packageName['name'] + '-' + i['version']

                    # Download dependency
                    open( dependencyPath + '.zip' , 'wb').write(dependencyUrl.content)

                    # unzip main package and remove zip file
                    zipPath = (dependencyPath + '.zip')
                    zip = zipfile.ZipFile(zipPath)
                    zip.extractall(dependencyPath)
                    zip.close()
                    os.remove(dependencyPath + '.zip')

                    downloadDependencies(i['dependencies'])
                    
            downloadDependencies(versions)
        else:
            print("Package not found")



        


