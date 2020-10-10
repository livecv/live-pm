import os
from livepm.lib.process import Process
from livepm.lib.dylib import DylibLinkInfo

linfo = DylibLinkInfo('/Users/dinu/Projects/livekeys/livekeys/build/livekeys-1.7.0-macos-clang-64/livekeys.app/Contents/Frameworks/OpenCV.framework/Libraries//libopencv_videoio.4.4.0.dylib')
print(linfo.dependencies)
print(linfo.rpath_info)

# linfo.add_rpath('path/to/dinu')
# linfo.change_dependencies({ "/usr/lib/libSystem.B.dylib" : "/path/to/dinu" })