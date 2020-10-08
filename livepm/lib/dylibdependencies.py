import os
import platform
import fnmatch
import shutil

from livepm.lib.process import Process
from livepm.lib.filesystem import FileSystem
from livepm.lib.dylibexternal import DylibLinkInfoExternal
from livepm.lib.dylib import DylibLinkInfo

# DyLibUsed = DylibLinkInfoExternal
DyLibUsed = DylibLinkInfo

class DylibDependencyMap:

    def __init__(self, filesToScan):

        self.hierarchy = {}

        for index, path in enumerate(filesToScan):
            realpath = os.path.realpath(path)
            if realpath not in self.hierarchy:
                self.hierarchy[realpath] = { 'dependencies': [] }
                self.recurse_dependencies(realpath)

    def recurse_dependencies(self, path):
        linfo = DyLibUsed(path)
        deps = linfo.find_absolute_dependencies('/usr/local/*')
        for i, dep in enumerate(deps):
            full_dep = linfo.absolute_dependency(dep)
            if full_dep != '':
                real_dep = os.path.realpath(full_dep)
                if real_dep != path:
                    self.hierarchy[path]['dependencies'].append([dep, real_dep])
                else:
                    self.hierarchy[path]['self'] = [dep, real_dep]

                if real_dep not in self.hierarchy:
                    self.hierarchy[real_dep] = { 'dependencies': [] }
                    self.recurse_dependencies(real_dep)

    def tostring(self):
        s = ''
        for key, value in self.hierarchy.items():
            s += key + '\n'
            if 'self' in value:
                s += '   Self ' + value['self'][0] + ' -> ' + value['self'][1] + '\n'
            for i, dep in enumerate(value['dependencies']):
                s += '   ' + dep[0]  + ' -> ' + dep[1] + '\n'

        return s

class DylibDependencyTransfer:

    def __init__(self, options):
        self.library_map = DylibDependencyMap(FileSystem.listEntries(options['files']))
        self.custom_copy = options['custom']
        self.copy_from = options['dependencies'] + '/'
        self.copy_to = options['destination']

        for key, value in self.library_map.hierarchy.items():
            copy_info = {}

            new_path = key.replace(self.copy_from, '')
            last_slash = new_path.rfind('/')
            if last_slash > 0:
                lib_name = new_path[last_slash + 1:]

                for custom_search, overwrite_path in self.custom_copy.items():
                    if fnmatch.fnmatch(new_path, custom_search):
                        last_slash = len(overwrite_path)
                        new_path = overwrite_path + '/' + lib_name


                copy_info['old_path'] = key
                copy_info['path']     = new_path
                copy_info['path_dir'] = new_path[0:last_slash]
                copy_info['lib_name'] = lib_name
                copy_info['path_out'] = '/'.join(map(lambda s: '..', copy_info['path_dir'].split('/'))) 

                value['path_info'] = copy_info

    def run(self, print_call):
        for key, value in self.library_map.hierarchy.items():

            copy_info = value['path_info']

            if not os.path.exists(self.copy_to + '/' + copy_info['path_dir']):
                os.makedirs(self.copy_to + '/' + copy_info['path_dir'])
                print_call('Made dir: ' + self.copy_to + '/' + copy_info['path_dir'])

            shutil.copyfile(key, self.copy_to + '/' + copy_info['path'])
            print_call('Copied: ' + self.copy_to + '/' + copy_info['path'])

            linfo = DyLibUsed(self.copy_to + '/' + copy_info['path'])

            total_deps = 0

            dependency_change_structure = {}

            # Change dependencies
            for key, dep in enumerate(value['dependencies']):
                # print('    Dep ' + str(dep)) # [id, path]
                # Find library
                rel_dependency_path = self.library_map.hierarchy[dep[1]]['path_info']['path']
                rel_from_here_path = copy_info['path_out'] + '/' + rel_dependency_path

                # linfo.change_dependency(dep[0], '@rpath/' + rel_from_here_path)
                dependency_change_structure[dep[0]] = '@rpath/' + rel_from_here_path
                # print('    Changed: ' + dep[0] + ' -> ' + '@rpath/' + rel_from_here_path)

                total_deps += 1

            linfo.change_dependencies(dependency_change_structure)

            print_call('    Changed ' + str(total_deps) + ' dependencies.')
            linfo.add_rpath('@loader_path')