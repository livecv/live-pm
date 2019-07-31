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
        parser.add_argument('name', default=None, help='Name of the package')
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

            # Dependency installation progress bar
            num_of_packages = []
            # Append id's of versions for package count
            for i in versions:
                num_of_packages.append(i['_id'])

            # use number of packages for iteration
            for i in range(len(num_of_packages)):
                update_progress("updating dependencies: ", i/len(num_of_packages))

            # finished
            update_progress("updating dependencies:", 1)

            for i in versions:
                
                version = i['version']
                packageName = i['package']['name']
                dependencyUrl = i['url']
                dependencyPath = os.path.join(plugin_directory, packageName + '-' + version)

                package = {packageName:version}
                
                # Check if the live.packages.json exist
                if os.path.exists(os.path.join(plugin_directory, 'live.packages.json')):
                    
                    # Read from file if exists
                    with open(os.path.join(plugin_directory,"live.packages.json")) as livePackages:
                        data = json.load(livePackages)
                        current = data['dependencies']
                        current.update(package)

                        # Write updated data
                        with open(os.path.join(plugin_directory,"live.packages.json"), "w") as livePackages:
                            
                            json.dump(data, livePackages,ensure_ascii=False, indent=4)
                            
                else:
                    # Create live.packages.json and write default data
                    with open(os.path.join(plugin_directory,"live.packages.json"), 'w') as livePackages:
                        
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

        
        # Get the os for release extension
        if platform.system() == 'Linux':
            release = 'linux'

        elif platform.system() == 'Darwin':
            release = 'macos'

        elif platform.system() == 'Windows':
            release = 'win'
                    
        # Construct url
        urlParams = 'package/' + self.name + '/' + 'latest/' + release
        url = urllib.parse.urljoin(self.server_url, urlParams)
        # Send request
        r = re.get(url, allow_redirects=True)

        # check version of package here

        # Package path construction
        plugin_directory= os.path.join(self.dir, self.folder, self.name)

        with open(os.path.join(plugin_directory,"live.packages.json")) as livePackages:
            data = json.load(livePackages)
            jsonResponse = json.loads(r.text)
            if data['version'] == jsonResponse['version']:
                print("Everything up to date.")

            else:
                print(jsonResponse['package']['name'])            
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

                    # Package installation progress bar
                    num_of_packages = []
                    # Append id's of packages for package count
                    num_of_packages.append(jsonResponse['package'])
                    # # use number of packages for iteration
                    for i in range(len(num_of_packages)):
                        update_progress("updating packages: ", i/len(num_of_packages))

                    # Finished
                    update_progress("updating packages: ", 1)

                    # install main packages
                    package_path = os.path.join(plugin_directory, self.name + '-' + jsonResponse['version']  )
                    open( package_path + '.zip', 'wb').write(getZip.content)

                    # unzip main package and remove zip file
                    zipPath = (package_path + '.zip')
                    zip = zipfile.ZipFile(zipPath)
                    zip.extractall(package_path)
                    zip.close()
                    os.remove(package_path + '.zip')
                    # Create live.packages.json for project
                    self.current_version = jsonResponse['version']
                    package = {self.name:jsonResponse['version']}
                    if os.path.exists(os.path.join(os.getcwd(), 'live.packages.json')):
                            
                        # Read live.packages.json
                        with open(os.path.join(os.getcwd(),"live.packages.json")) as livePackages:
                            data = json.load(livePackages)
                            current = data['dependencies']
                            current.update(package)

                        # Write updated data
                        with open(os.path.join(os.getcwd(),"live.packages.json"), "w") as livePackages:
                                
                            json.dump(data, livePackages,ensure_ascii=False, indent=4)

                    else:
                        # Create live.packages.json and write default data
                        with open(os.path.join(os.getcwd(),"live.packages.json"), 'w') as livePackages:
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