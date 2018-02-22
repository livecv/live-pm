import sys
import subprocess
import os

class Process:

    def run(command, cwd, environment=None, shell=False):
        proc = subprocess.Popen(
            command, bufsize=1, stdout=subprocess.PIPE, cwd=cwd, shell=shell,
            stderr=subprocess.STDOUT, universal_newlines=True, env=environment)
        return proc

    def trace(preffix, proc, end='\n'):
        while proc.poll() is None:
            line = proc.stdout.readline()
            if line:
                print(preffix + line, end=end)
        line = proc.stdout.readline()
        while( line ):
            print(preffix + line, end=end)
            line = proc.stdout.readline()

    def scriptdir():
        return os.path.dirname(os.path.realpath(__file__))
