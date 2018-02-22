import os
import platform
import subprocess
from livepm.lib.process import *
from livepm.lib.filesystem import *

# Solves visual studio environment for windows builds

class VSEnvironment:

    def parse(envoutput):
        handle_line = lambda l: tuple(l.rstrip().split("=", 1))
        pairs = map(handle_line, envoutput)
        valid_pairs = filter(lambda x: len(x) == 2, pairs)
        valid_pairs = [(x[0].upper(), x[1]) for x in valid_pairs]
        return dict(valid_pairs)

    def overrideenv(newenv):
        old = os.environ.copy()
        removed = set(old) - set(newenv)
        for k in newenv.keys():
        	os.environ[k] = newenv[k]
        for k in removed:
        	os.environ.pop(k)
        return old

    def setupenv(vsver, vsparam = ''):
        cmd = r'cmd /s /c ""%VS{vsver}COMNTOOLS%/../../VC/vcvarsall.bat" {vsparam} & set"'.format(**locals())
        ret = subprocess.Popen(
        		cmd,
        		stdout=subprocess.PIPE,
        		stderr=subprocess.STDOUT,
        		stdin=subprocess.PIPE)
        output = ret.communicate()[0]
        outputsplit = output.decode('utf-8').split("\r\n")
        old = VSEnvironment.overrideenv(VSEnvironment.parse(outputsplit))
        return old
