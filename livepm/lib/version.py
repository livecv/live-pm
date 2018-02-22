import re

class Version:

    def __init__(self, versionstring):
        self.versionmajor = 0
        self.versionminor = 0
        self.versionpatch = 0
        versionlist = versionstring.split('.')
        if ( len(versionlist) > 0 ):
            self.versionmajor = versionlist[0]
        if ( len(versionlist) > 1 ):
            self.versionminor = versionlist[1]
        if ( len(versionlist) > 2 ):
            self.versionpatch = versionlist[2]

    def __str__(self):
        return str(self.versionmajor) + '.' + str(self.versionminor) + '.' + str(self.versionpatch)

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
            return (fcontent[0:versionmajorstart] + str(self.versionmajor)
            + fcontent[versionmajorend:versionminorstart]
            + str(self.versionminor) + fcontent[versionminorend:versionpatchstart]
            + str(self.versionpatch) + fcontent[versionpatchend:])

    def savetofile(self, filepath, versionpattern):
        fcontent = self.generatefilecontents(filepath, versionpattern)
        with open(filepath, 'w') as fwrite:
            fwrite.write(fcontent)
            print('        Saved version ' + str(self.versionmajor) + '.' + str(self.versionminor)
            + '.' + str(self.versionpatch) + ' to file: ' + filepath)
    #
    # def save(self, changes = {}):
    #     self.savetofile(self.versionpath, self.versionpattern)
    #     for key, value in changes.items():
    #         self.savetofile(key, value)
