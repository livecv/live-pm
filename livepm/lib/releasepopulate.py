import os
import shutil
import fnmatch
import json

from livepm.lib.releaseaction import *

class ReleasePopulate(ReleaseAction):

    def __init__(self, parent, step, options = None):
        super().__init__('populate', parent, step)
        self.options = options

    def __call__(self, sourcedir, releasedir, environment = os.environ):
        for key, value in self.options.items():
            if not os.path.isabs(key):
                key = os.path.join(self.run_dir(releasedir), key)

            print("POPULATE: " + key)

            fdata = {}

            with open(key, 'r') as f:
                fdata = json.load(f)

            for populatekey, populatevalue in value.items():
                print("         * " + populatekey + ' -> ' + populatevalue)
                fdata[populatekey] = populatevalue

            with open(key, 'w') as fw:
                json.dump(fdata, fw, indent=4)

    def is_match(name, values):
        for value in values:
            if ( fnmatch.fnmatch(name, value) ):
                return True
        return False