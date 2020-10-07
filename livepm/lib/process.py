import sys
import subprocess
import os
from shutil import which

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

    def exists(name):
        return which(name) is not None

    def scriptdir():
        return os.path.dirname(os.path.realpath(__file__))

    def back_tick(cmd, cwd, environment=None, ret_err=False, as_str=True, raise_err=None):
        if raise_err is None:
            raise_err = False if ret_err else True
        cmd_is_seq = isinstance(cmd, (list, tuple))
            
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, cwd=cwd,  shell=not cmd_is_seq,
            stderr=subprocess.PIPE, env=environment)
        out, err = proc.communicate()
        retcode = proc.returncode
        cmd_str = ' '.join(cmd) if cmd_is_seq else cmd
        if retcode is None:
            proc.terminate()
            raise RuntimeError(cmd_str + ' process did not terminate')
        if raise_err and retcode != 0:
            raise RuntimeError('{0} returned code {1} with error {2}'.format(
                            cmd_str, retcode, err.decode('latin-1')))
        out = out.strip()
        if as_str:
            out = out.decode('latin-1')
        if not ret_err:
            return out

        err = err.strip()
        if as_str:
            err = err.decode('latin-1')
        return out, err
