from livecv.version import *

class Component:
    def __init__(self, name, itemob):
        self.name    = name
        self.version = Version(itemob['version'])
        self.versionsyncs = {}
        if 'versionsync' in itemob:
            for key, value in itemob['versionsync'].items():
                strvalue = ''
                if isinstance(value, list):
                    for s in value:
                        strvalue += s
                else:
                    strvalue = value
                self.versionsyncs[key] = strvalue

    def __str__(self):
        return self.name + '(' + str(self.version) + ')'
