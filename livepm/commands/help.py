import argparse
import sys

from livepm.lib.command import Command

class HelpCommand(Command):
    name = 'help'
    description = 'Show this help'

    def __init__(self):
        pass

    def parse_args(self, argv):
        parser = argparse.ArgumentParser(prog = sys.argv[0] + ' ' + HelpCommand.name, description = 'Live package manager.')
        args = parser.parse_args(argv)

    def __call__(self):
        print()
        print('Live Package Manager')
        print()

        print('Usage:')
        print('   ' + sys.argv[0] + ' <command> [options]')
        print()

        from livepm.commands import stored_commands
        
        print('Commands:')
        for key, val in stored_commands.items():
            print('   ' + val.name + ' - ' + val.description)

        print()
        print('Use "' + sys.argv[0] + ' <command> --help" to view more details for a specific command.')