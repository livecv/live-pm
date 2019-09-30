import sys
import os
import argparse
import json

from livepm.lib.command import Command
from livepm.lib.configuration import Configuration
from livepm.lib.filesystem import FileSystem
from livepm.lib.projecttemplate import ProjectTemplate

class NewCommand(Command):
    name = 'new'
    description = (
        'Create a plugin for Live CV. The plugin will be created in a new directory '
        'unless the directory is specified. If there\'s already a project within the specified '
        'directory the plugin is appended to the project, otherwise the project is created. The '
        'plugin can be specified as a path, (i.e. opencv.contrib.core), which will be part of the '
        'project, unless otherwise speciifed'
    )

    def __init__(self):
        pass

    def parse_args(self, argv):
        parser = argparse.ArgumentParser(description = NewCommand.description)
        parser.add_argument('plugin', default=None, help="Plugin name and uri. (i.e. opencv.contrib.core)")
        parser.add_argument('--dir', default=None, help="Directory where the plugin will be created.")
        parser.add_argument('--project-uri', default=None, help="Project uri.")

        args = parser.parse_args(argv)

        self.plugin_uri = args.plugin
        self.segments = self.plugin_uri.split('.')
        self.plugin_segments = []
        self.project_segments = []

        if len(self.segments) > 1:
            self.project_segments = self.segments[:-1]
            if args.project_uri:
                self.project_segments = []
                project_given_segments = args.project_uri.split('.')
                for i, val in enumerate(self.segments):
                    if i >= len(project_given_segments):
                        self.plugin_segments.append(val)
                    elif val != project_given_segments[i]:
                        raise Exception('Project uri does not match the plugin uri.')
                    else:
                        self.project_segments.append(val)

            if len(self.plugin_segments) == 0:
                raise Exception('Plugin uri matches project uri.')

        else:
            self.plugin_segments = self.segments
            self.project_segments = self.segments

        if args.dir:
            self.project_dir = os.path.abspath(args.dir)
        else:
            self.project_dir = os.path.abspath(''.join(self.project_segments))

        if not os.path.exists(self.project_dir):
            os.makedirs(self.project_dir)

        print('Looking up package in:' + self.project_dir)

        try:
            self.package = Configuration.findpackage(self.project_dir)
            print('Package found: ' + self.package)
        except Exception as e:
            print('No package in ' + self.project_dir)
            self.create_package()

        self.create_plugin()

    def create_package(self):
        print('Creating package...')
        template = os.path.abspath(FileSystem.scriptdir() + '/../../templates/project')
        dest = self.project_dir
        NewCommand.copy_template(template, dest, {
            "project_name" : '.'.join(self.project_segments),
            "project_name_clean" : ''.join(self.project_segments),
            "plugin_name": self.plugin_segments[-1],
            "_plugin_name": '_' + self.plugin_segments[-1],
            "plugin_name_upper": self.plugin_segments[-1].upper(),
            "plugin_name_capital": self.plugin_segments[-1].title(),
            "plugin_name_plugin": self.plugin_segments[-1] + '_plugin',
            "plugin_uri": '.'.join(self.plugin_segments),
            "plugin_path": '/'.join(self.plugin_segments)
        })

        self.package = os.path.join(dest, 'live.' + '.'.join(self.project_segments) + '.json')

        c = Configuration.create('.'.join(self.project_segments))
        configuration_data = c.to_json()
        fw = open(self.package, "w")
        fw.write(json.dumps(configuration_data, indent=4, sort_keys=False))
        print()

    def copy_template(template, to, options):
        for subdir, dirs, files in os.walk(template):
            for file in files:
                filepath = os.path.join(subdir, file)
                filename, extension = os.path.splitext(file)
                if extension == '.tpl':
                    s = ProjectTemplate(filename)
                    solved_filename = s.safe_substitute(options)
                    relative_dest_dir = subdir.replace(template, '')
                    if relative_dest_dir.startswith('/') or relative_dest_dir.startswith('\\'):
                        relative_dest_dir = relative_dest_dir[1:]
                    destdir = os.path.join(to, relative_dest_dir)

                    if not os.path.exists(destdir):
                        os.makedirs(destdir)

                    fr = open(filepath, "r")
                    contents = fr.read()
                    template_object = ProjectTemplate(contents)
                    resolved_contents = template_object.safe_substitute(options)

                    fw = open(os.path.join(destdir, solved_filename), "w")
                    fw.write(resolved_contents)
                    print(' * Wrote file: ' + os.path.join(destdir, solved_filename))

    def create_plugin(self):
        print('Creating plugin...')

        with open(self.package) as jsonfile:
            packagejson = json.load(jsonfile)

        conf = Configuration(packagejson)
        c_segments = conf.name.split('.')
        self.plugin_segments = []
        self.project_segments = []
        
        if len(self.segments) > 1:
            for i, val in enumerate(self.segments):
                if i >= len(c_segments):
                    self.plugin_segments.append(val)
                elif val != c_segments[i]:
                    raise Exception('Project uri does not match the plugin uri.')
                else:
                    self.project_segments.append(val)

            if len(self.plugin_segments) == 0:
                raise Exception('Plugin uri matches project uri.')

        else:
            self.plugin_segments = self.segments
            self.project_segments = self.segments

        conf.add_component('.'.join(self.plugin_segments), {"version": "0.1.0"})
        configuration_data = conf.to_json()
        fw = open(self.package, "w")
        fw.write(json.dumps(configuration_data, indent=4, sort_keys=False))

        plugin_path = os.path.join(self.project_dir, '/'.join(self.plugin_segments))
        if not os.path.exists(plugin_path):
            os.makedirs(plugin_path)

        template = os.path.abspath(FileSystem.scriptdir() + '/../../templates/cpp-plugin')

        NewCommand.copy_template(template, plugin_path, {
            "project_name" : '.'.join(self.project_segments),
            "project_name_clean" : ''.join(self.project_segments),
            "plugin_name": self.plugin_segments[-1],
            "_plugin_name": '_' + self.plugin_segments[-1],
            "plugin_name_upper": self.plugin_segments[-1].upper(),
            "plugin_name_capital": self.plugin_segments[-1].title(),
            "plugin_name_plugin": self.plugin_segments[-1] + '_plugin',
            "plugin_uri": '.'.join(self.plugin_segments),
            "plugin_path": '/'.join(self.plugin_segments)
        })

        qmake_file = os.path.join(self.project_dir, ''.join(self.project_segments) + '.pro')
        if not os.path.exists(qmake_file):
            print("Warning: Failed to write to \'" + qmake_file + "\', file does not exist.")
            return

        qf = open(qmake_file, 'r+')
        qdata = qf.read()

        template_def_index = qdata.find('TEMPLATE = subdirs')
        if template_def_index == -1:
            print("Warning: Failed to write to \'" + qmake_file + "\', file does not contain template declaration.")
            return

        qmake_subdir = 'SUBDIRS += ' + ('_'.join(self.plugin_segments)) + '\n' + '_'.join(self.plugin_segments) + '.subdir = ' + '/'.join(self.plugin_segments)
        qdata = qdata.replace('TEMPLATE = subdirs', 'TEMPLATE = subdirs\n' + qmake_subdir)
        qdata = qdata.replace('livekeys.subdir = $$PWD/livekeys', 'livekeys.subdir = $$PWD/livekeys\n    ' + '_'.join(self.plugin_segments) + '.depends = livekeys')

        qf.seek(0)
        qf.write(qdata)
        qf.truncate()

        print()


