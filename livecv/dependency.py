from livecv.version import *

class Dependency:
    def __init__(self, options):
        self.name = options['name']
        self.version = options['version']
        self.repository = options['repository']
