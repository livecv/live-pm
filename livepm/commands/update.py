import sys,time
import os
import platform
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

class UpdateCommand(Command):

    name = 'update'
    description = 'Update a live package'

    def __init__(self):
        pass

    def parse_args(self, argv):
        parser = argparse.ArgumentParser(description='Update a live package')
        parser.add_argument('name', default=None, nargs="?", help='Name of the package')
        parser.add_argument('--server_url', '-sU', default=server_url, help='Change server url.')
        parser.add_argument('--update_globally', '-g' ,default=False, action='store_true', help="Update globally")

        args = parser.parse_args(argv)

        self.name   = args.name
        self.server_url   = args.server_url
        self.current_version = ''
  
        # Directory construction
        if args.update_globally:
            
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

        # Get the os for release extension
        if platform.system() == 'Linux':
            release = 'linux'

        elif platform.system() == 'Darwin':

            release = 'macos'

        elif platform.system() == 'Windows':

            release = 'win'

        # progress bar
        def update_progress(title, progress):
            length = 40
            block = int(round(length*progress))
            msg = "\r{0}: [{1}] {2}%".format(title, "#"*block + "-"*(length-block), round(progress*100, 2))
            if progress >=1: 
                msg += "DONE\r\n"
            sys.stdout.write(msg)
            sys.stdout.flush()

        # Dependency download
        def downloadDependencies(versions):

            for i in versions:
                
                version = i['version']
                packageName = i['package']['name']
                dependencyUrl = i['url']
                dependencyPath = os.path.join(plugin_directory, packageName + '-' + version)

                package = {packageName:version}
                
                # Check if the live.package.json exist
                if os.path.exists(os.path.join(plugin_directory, 'live.package.json')):
                    
                    # Read from file if exists
                    with open(os.path.join(plugin_directory,"live.package.json")) as livePackages:
                        data = json.load(livePackages)
                        current = data['dependencies']
                        current.update(package)

                        # Write updated data
                        with open(os.path.join(plugin_directory,"live.package.json"), "w") as livePackages:
                            
                            json.dump(data, livePackages,ensure_ascii=False, indent=4)
                            
                else:
                    # Create live.package.json and write default data
                    with open(os.path.join(plugin_directory,"live.package.json"), 'w') as livePackages:
                        
                        package_details = {
                            
                            "name": os.path.basename(plugin_directory), 
                            "version": self.current_version,
                            "dependencies": package
                            }

                        json.dump(package_details, livePackages,ensure_ascii=False, indent=4)

                # Download dependency
                open( dependencyPath + '.zip' , 'wb').write(getZip.content)
                # unzip main package and remove zip file
                zipPath = (dependencyPath + '.zip')
                zip = zipfile.ZipFile(zipPath)
                zip.extractall(dependencyPath)
                zip.close()
                os.remove(dependencyPath + '.zip')
                downloadDependencies(i['dependencies'])

        # Update packages from json.packages.json
        if not self.name:

            if os.path.exists(os.path.join(os.getcwd(), 'live.package.json')):
                # read json
                with open(os.path.join(os.getcwd(),"live.package.json")) as livePackages:
                    data = json.load(livePackages)

                    for package, version in data['dependencies'].items():
                        # urlParams = 'package/' + package + '/release/' + version + '/' + release
                        urlParams = 'package/' + package + '/' + 'latest/' + release
                        url = urllib.parse.urljoin(self.server_url, urlParams)
                        r = re.get(url, allow_redirects=True)
                        resp = json.loads(r.text)

                        currentPackage = package + '-' + version
                        latestPackage = package + '-' + resp['version']

                        # Compare installed and newest version
                        if currentPackage == latestPackage:
                            
                            print('Package: ' + package + ' ' + version + ' is up to date.')
                            continue

                        else:
                            print('Updating '+ package)
                            pass

                        if r.ok:

                            data = r.text
                            resp = json.loads(data)

                            # current package dependencies
                            dependencies = resp['dependencies']

                            # Request the zip file
                            getZip = re.get(resp['url'])
                            
                            # # install main packages
                            plugin_directory= os.path.join(self.dir, self.folder, package )

                            if not os.path.exists(plugin_directory):
                                os.makedirs(plugin_directory)

                            else:
                                pass

                            package_path = os.path.join(plugin_directory, package + '-' + version)

                            open( package_path + '.zip', 'wb').write(getZip.content)

                            # # unzip main package and remove zip file
                            zipPath = (package_path + '.zip')
                            zip = zipfile.ZipFile(zipPath)
                            zip.extractall(package_path)
                            zip.close()
                            os.remove(package_path + '.zip')

                            # Read live.package.json
                            with open(os.path.join(os.getcwd(),"live.package.json")) as livePackages:
                                data = json.load(livePackages)
                                current = data['dependencies']
                                # add new version to live.package.json
                                current.update({package:resp['version']})

                            # Write updated data
                            with open(os.path.join(os.getcwd(),"live.package.json"), "w") as livePackages:
                                    
                                json.dump(data, livePackages,ensure_ascii=False, indent=4)

                            downloadDependencies(dependencies)
                            
                        # Note if the package is not found
                        else:
                            print('Package ' + package + ' not found.')

            # live.package.json missing
            else:

                print('live.package.json not found.')
                sys.exit(1)
        else:
                    
            # Construct url
            urlParams = 'package/' + self.name + '/' + 'latest/' + release
            url = urllib.parse.urljoin(self.server_url, urlParams)
            # Send request
            r = re.get(url, allow_redirects=True)

            # Package path construction
            plugin_directory= os.path.join(self.dir, self.folder, self.name)

            with open(os.path.join(plugin_directory,"live.package.json")) as livePackages:
                data = json.load(livePackages)
                jsonResponse = json.loads(r.text)
                # check if latest version is installed
                if data['version'] == jsonResponse['version']:
                    print(self.name + " up to date.")

                else:         
                    # Check the url
                    if r.ok:

                        # Check if the package.lock exist and create one if not
                        if not os.path.exists(os.path.join(os.getcwd(), 'live.package.lock')):
                            open(os.path.join(os.getcwd(), 'live.package.lock'),'w')

                        else:
                            print('Already running!')
                            sys.exit(1)

                        # Request the zip file
                        getZip = re.get(jsonResponse['url'])
                            
                        # Read dependencies
                        versions = jsonResponse['dependencies']

                        # install main package
                        package_path = os.path.join(plugin_directory, self.name + '-' + jsonResponse['version']  )
                        open( package_path + '.zip', 'wb').write(getZip.content)

                        # unzip main package and remove zip file
                        zipPath = (package_path + '.zip')
                        zip = zipfile.ZipFile(zipPath)
                        zip.extractall(package_path)
                        zip.close()
                        os.remove(package_path + '.zip')
                        # Create live.package.json for project
                        self.current_version = jsonResponse['version']
                        package = {self.name:jsonResponse['version']}
                        if os.path.exists(os.path.join(os.getcwd(), 'live.package.json')):
                                
                            # Read live.package.json
                            with open(os.path.join(os.getcwd(),"live.package.json")) as livePackages:
                                data = json.load(livePackages)
                                current = data['dependencies']
                                current.update(package)

                            # Write updated data
                            with open(os.path.join(os.getcwd(),"live.package.json"), "w") as livePackages:
                                    
                                json.dump(data, livePackages,ensure_ascii=False, indent=4)

                        else:
                            # Create live.package.json and write default data
                            with open(os.path.join(os.getcwd(),"live.package.json"), 'w') as livePackages:
                                package_details = {
                                        
                                    "name": os.path.basename(os.getcwd()), 
                                    "version": '0.1.0',
                                    "dependencies": package

                                    }
                                json.dump(package_details, livePackages,ensure_ascii=False, indent=4)
                            
                        downloadDependencies(versions)

                        # remove package.lock
                        os.remove(os.path.join(os.getcwd(), 'live.package.lock'))

                    else:

                        print("Package not found")