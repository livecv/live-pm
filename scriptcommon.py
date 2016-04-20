import os
import sys
import re
import string
import shutil
import subprocess
import fnmatch
from subprocess import Popen

class Version:
    def __init__(self, versionpath, versionpattern):
        self.versionpath    = versionpath
        self.versionpattern = versionpattern
        versionparser = re.compile(versionpattern)

        with open(versionpath, 'r') as f:
            fcontent = f.read()
            m = versionparser.search(fcontent)
            if m:
                self.versionMajor = int(m.group(1))
                self.versionMinor = int(m.group(2))
                self.versionPatch = int(m.group(3))

    def generatefilecontents(self, filepath, versionpattern):
        versionparser = re.compile(versionpattern)
        with open(filepath, 'r') as f:
            fcontent = f.read()
            m = versionparser.search(fcontent)
            if m:
                versionmajorstart = m.start(1)
                versionmajorend   = m.end(1)
                versionminorstart = m.start(2)
                versionminorend   = m.end(2)
                versionpatchstart = m.start(3)
                versionpatchend   = m.end(3)
            return (fcontent[0:versionmajorstart] + str(self.versionMajor)
            + fcontent[versionmajorend:versionminorstart]
            + str(self.versionMinor) + fcontent[versionminorend:versionpatchstart]
            + str(self.versionPatch) + fcontent[versionpatchend:])

    def savetofile(self, filepath, versionpattern):
        fcontent = self.generatefilecontents(filepath, versionpattern)
        with open(filepath, 'w') as fwrite:
            fwrite.write(fcontent)
            print('Saved version ' + str(self.versionMajor) + '.' + str(self.versionMinor)
            + '.' + str(self.versionPatch) + ' to file: ' + filepath)

    def save(self, changes = {}):
        self.savetofile(self.versionpath, self.versionpattern)
        for key, value in changes.items():
            self.savetofile(key, value)


class OSOperations:

    def run(command, cwd, environment=None):
        proc = subprocess.Popen(
            command, bufsize=1, stdout=subprocess.PIPE, cwd=cwd,
            stderr=subprocess.STDOUT, universal_newlines=True, env=environment)
        return proc

    def trace(preffix, proc, end='\n'):
        while proc.poll() is None:
            line = proc.stdout.readline()
            if line:
                print(preffix + line, end=end)

    def find(name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)
        return ''

    def scriptdir():
        return os.path.dirname(os.path.realpath(__file__))


    def copyFileOrDirectory(src, dst):

        if os.path.isdir(src):
            if os.path.basename(os.path.normpath(dst)) == "-":
                dst = dst[0:len(dst) - 1] + os.path.basename(os.path.normpath(src))
            shutil.copytree(src, dst)
        else:
            filedir  = os.path.dirname(dst)
            if not os.path.exists(filedir):
                os.makedirs(filedir)

            srcfilename = os.path.basename(src)
            if "*" in srcfilename or "?" in srcfilename:
                for file in os.listdir(os.path.dirname(src)):
                    if fnmatch.fnmatch(file, srcfilename):
                        dstfile = dst
                        if os.path.basename(os.path.normpath(dst)) == "-":
                            dstfile = dst[0:len(dst) - 1] + file
                        shutil.copyfile(
                            os.path.join(os.path.dirname(src), file),
                            dstfile
                        )
            else:
                if os.path.basename(os.path.normpath(dst)) == "-":
                    dst = dst[0:len(dst) - 1] + os.path.basename(os.path.normpath(src))
                shutil.copyfile(src, dst)

    def copyFileStructure(releaseDir, structure, structurePrefix = ""):
        for key, value in structure.items():
            if isinstance(value, dict):
                OSOperations.copyFileStructure(releaseDir, value, os.path.join(structurePrefix, key))
            else:
                OSOperations.copyFileOrDirectory(os.path.join(structurePrefix, key), releaseDir + value)


class Build:
    def __init__(self, sourcedir, releasedir, qmake, make):
        self.sourcedir  = sourcedir
        self.releasedir = releasedir
        self.qmake      = qmake
        self.make       = make

    def cleandir(self):
        if os.path.isdir(self.releasedir):
            shutil.rmtree(self.releasedir)
        os.makedirs(self.releasedir)

    def createmakefile(self, environment = os.environ):
        proc = OSOperations.run([self.qmake, "-recursive", self.sourcedir], self.releasedir, environment)
        OSOperations.trace("QMAKE:", proc, end='')

    def runmake(self, environment = None):
        proc = OSOperations.run([self.make], self.releasedir, environment)
        OSOperations.trace("MAKE:", proc, end='')


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
		ret = Popen(
				cmd,
				stdout=subprocess.PIPE,
				stderr=subprocess.STDOUT,
				stdin=subprocess.PIPE)
		output = ret.communicate()[0]
		outputsplit = output.decode('utf-8').split("\r\n")
		old = VSEnvironment.overrideenv(VSEnvironment.parse(outputsplit))
		return old

class License:

	def __init__(self, sourcedir, extensions):
		self.sourcedir  = sourcedir
		self.extensions = extensions

	def update(self, newlicense, oldlicense = ''):
		for subdir, dirs, files in os.walk(self.sourcedir):
			for file in files:
				filename, fileextension = os.path.splitext(subdir + '/' + file)
				if ( len(fileextension) > 0 ):
					if ( fileextension[0] == '.' ):
						fileextension = fileextension[1:]
					if any(fileextension in s for s in self.extensions):
						if( oldlicense != '' ):
							self.updatelicense(subdir + '/' + file, newlicense, oldlicense)
						else:
							self.addlicense(subdir + '/' + file, newlicense)

	def addlicense(self, file, license):
		fileresr = open(file, 'r')
		filecontents = fileresr.read()
		if(filecontents.find(license) != -1):
			fileresr.close()
			return

		fileresw = open(file, 'w')
		fileresw.write(license + '\n\n' + filecontents)
		fileresw.close()
		print('Added license to ' + file + '\n')

	def updatelicense(self, file, newlicense, oldlicense):
		fileresr = open(file, 'r')
		filecontents = fileresr.read()
		if(filecontents.find(newlicense) != -1):
			fileresr.close()
			return

		licensetext = re.search(oldlicense, filecontents, re.DOTALL)
		if ( licensetext ):
			filecontents = filecontents.replace(licensetext.group(0), newlicense)
			fileresw = open(file, 'w')
			fileresw.write(filecontents)
			fileresw.close()
			print('Updated license in ' + file + '\n')
		else:
			fileresw = open(file, 'w')
			fileresw.write(newlicense + '\n\n' + filecontents)
			fileresw.close()
			print('Added license to ' + file + '\n')
