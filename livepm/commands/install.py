import sys
import os
import getopt
import json
import shutil
import argparse
import requests as re
import urllib.parse
import zipfile
from livepm.lib.command import Command
from livepm.lib.configuration import Configuration

server_url = "https://livekeys.io/api"

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
        parser.add_argument('--install_globally', '-g' ,default=False, action='store_true', help="Install to livekeys dir")

        args = parser.parse_args(argv)

        self.name   = args.name
        self.release   = args.release
        self.server_url   = args.server_url
  
        # Directory construction
        if args.install_globally:
            
            try:
                if os.environ['LIVEKEYS_DIR']:
                    self.dir = os.environ["LIVEKEYS_DIR"]
                    self.folder = 'plugins'

            except KeyError:
                print("Enviroment variable LIVEKEYS_DIR not set.")
                sys.exit(1)

        else:
            self.dir = os.getcwd()
            self.folder = 'packages'
    
    def __call__(self):
        # Construct url
        urlParams = 'package/' + self.name + '/' + 'latest/' + self.release
        url = urllib.parse.urljoin(self.server_url, urlParams)
        # Send request
        r = re.get(url, allow_redirects=True)
        
        # Check the url
        if r.ok:

            # Package path construction
            plugin_directory= os.path.join(self.dir, self.folder, self.name)
            
            # Create folders if installing in cwd
            if os.environ != ["LIVEKEYS_DIR"]:
                os.makedirs(plugin_directory)

            else:
                # os.makedirs(plugin_directory)
                pass

            jsonResponse = json.loads(r.text)
            
            # Request the zip file
            getZip = re.get(jsonResponse['url'])
            
            # Read dependencies
            versions = jsonResponse['dependencies']

            # Download main package
            package_path = os.path.join(plugin_directory, self.name + '-' + jsonResponse['version']  )
            open( package_path + '.zip', 'wb').write(getZip.content)

            # unzip main package and remove zip file
            zipPath = (package_path + '.zip')
            zip = zipfile.ZipFile(zipPath)
            zip.extractall(package_path)
            zip.close()
            os.remove(package_path + '.zip')

            # Check for package.json and create one if missing
            for package in os.listdir(os.path.join(self.dir, self.folder)):
                
                if package.startswith(self.name):
                    path = os.path.join(plugin_directory)
                    print(package)
                    
                    try:
                        if os.listdir(os.path.join(path, 'live.package.json')):
                        
                            for file in os.listdir(path):
                                
                                with open(os.path.join(path,"live.packages.json"), "w+") as livePackages:
                                    
                                    package_details = {
                                        
                                        'name': self.name,
                                        'version': jsonResponse['version']
                                        }

                                    json.dump(package_details, livePackages,ensure_ascii=False, indent=4)
                                    
                    except:
                        
                        print('live.package.json not found! Creating one.')
                            
                        with open(os.path.join(path,"live.packages.json"), "a") as livePackages:
                                
                                package_details = {
                                    
                                    'name': self.name,
                                    'version': jsonResponse['version']
                                            
                                            }

                                json.dump(package_details, livePackages)
                                
            # Dependency download
            def downloadDependencies(versions):
                
                for i in versions:

                    version = i['version']
                    packageName = i['package']
                    dependencyUrl = i['url']
                    dependencyPath = os.path.join(plugin_directory, packageName['name'] + '-' + i['version'])

                    # Add dependencies info in live.packages.json
                    with open(os.path.join(path,"live.packages.json"), "a") as livePackages:
                        
                        package_details = {

                          'dependencies': {

                            'name': i['package']['name'],

                            'version': i['version']

                          }

                        }

                        json.dump(package_details, livePackages, ensure_ascii=False, indent=4)
                        
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
