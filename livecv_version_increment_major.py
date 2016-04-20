import os
import sys
import re
import string
from scriptcommon import Version

v = Version(
    '../application/src/qlivecv.h',
    r'(?:\s*#define LIVECV_VERSION_MAJOR)\s*([0-9]*)\s*\n'
     '(?:\s*#define LIVECV_VERSION_MINOR)\s*([0-9]*)\s*\n'
     '\s*(?:#define LIVECV_VERSION_PATCH)\s*([0-9]*)\s*')

v.versionPatch = 0
v.versionMinor = 0
v.versionMajor = v.versionMajor + 1
v.save({'../README.md': r'\s*(?:\* \*\*Version\*\*\:)\s*([0-9]*)\.{1}([0-9]*)\.{1}([0-9]*)\s*'})
