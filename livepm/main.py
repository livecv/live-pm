import sys
import io
import os
import argparse

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

from livepm.commands import stored_commands

def main(argv):

    command = 'help'
    if ( len(argv) > 0 and (argv[0] in stored_commands) ):
        command = argv[0]

    command_object = stored_commands[command]()
    command_object.parse_args(argv[1:])
    command_object()

if __name__ == "__main__":
    main(sys.argv[1:])
