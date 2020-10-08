import os
import platform
import fnmatch
import shutil
import sys
import stat
import uuid
import re

from macholib.ptypes import sizeof
from macholib.util import fsencoding
from macholib import MachO
from macholib import mach_o

# A set of functions used from machotools
#
# Copyright (c) 2013, Enthought, Inc.
# All rights reserved.
#

# Utilities
# ---------------------------------------------------------------------------------------

def macho_path_as_data(filename, pad_to=4):
    """ Encode a path as data for a MachO header.
    Namely, this will encode the text according to the filesystem
    encoding and zero-pad the result out to 4 bytes.
    Parameters
    ----------
    filename: str
        Path string to encode
    pad_to: int
        Number of bytes to pad the encoded string to
    """
    filename = fsencoding(filename) + b'\x00'
    rem = len(filename) % pad_to
    if rem > 0:
        filename += b'\x00' * (pad_to - rem)
    return filename

def rstrip_null_bytes(s):
    """Right-strip any null bytes at the end of the given string."""
    return s.rstrip(b'\x00')

def convert_to_string(data):
    data = rstrip_null_bytes(data)
    return data.decode(sys.getfilesystemencoding())

def safe_write(target, writer, mode="wt"):
    """a 'safe' way to write to files.
    Instead of writing directly into a file, this function writes to a
    temporary file in the same directory, and then rename the file to the
    target if no error occured.  On most platforms, rename is atomic, so this
    avoids leaving stale files in inconsistent states.
    Parameters
    ----------
    target: str
        destination to write to
    writer: callable or data
        if callable, assumed to be function which takes one argument, a file
        descriptor, and writes content to it. Otherwise, assumed to be data
        to be directly written to target.
    mode: str
        opening mode
    """
    if not callable(writer):
        data = writer
        writer = lambda fp: fp.write(data)

    file_mode = stat.S_IMODE(os.stat(target).st_mode)

    tmp_target = "%s.tmp%s" % (target, uuid.uuid4().hex)
    f = open(tmp_target, mode)
    try:
        writer(f)
    finally:
        f.close()
    os.chmod(tmp_target, file_mode)
    os.rename(tmp_target, target)

def safe_update(target, writer, mode="wt"):
    """a 'safe' way to update a file.
    Instead of writing directly into a file, this function first copies target
    to a temporary file and, writes to it, and then rename the file to the
    target if no error occured.  On most platforms, rename is atomic, so this
    avoids leaving stale files in inconsistent states.
    Parameters
    ----------
    target: str
        file to update
    writer: callable or data
        if callable, assumed to be function which takes one argument, a file
        descriptor, and writes content to it. Otherwise, assumed to be data
        to be directly written to target.
    mode: str
        opening mode
    """
    if 'b' in mode:
        target_mode = 'rb'
    else:
        target_mode = 'r'

    def writer_wrap(f):
        g = open(target, target_mode)
        try:
            shutil.copyfileobj(g, f)
        finally:
            g.close()
        return writer(f)
    return safe_write(target, writer_wrap, mode)


def _change_command_data_inplace(header, index, old_command, new_data):
    # We change the command 'in-place' to ensure the new dylib command is as
    # close as possible as the old one (same version, timestamp, etc...)
    (old_load_command, old_dylib_command, old_data) = old_command

    if header.header.magic in (mach_o.MH_MAGIC, mach_o.MH_CIGAM):
        pad_to = 4
    else:
        pad_to = 8
    data = macho_path_as_data(new_data, pad_to=pad_to)

    cmdsize_diff = len(data) - len(old_data)
    load_command = old_load_command
    load_command.cmdsize += cmdsize_diff

    dylib_command = old_dylib_command

    header.commands[index] = (load_command, dylib_command, data)
    header.changedHeaderSizeBy(cmdsize_diff)

def _find_lc_dylib_command(header, command_type):
    commands = []
    for command_index, (load_command, dylib_command, data) in enumerate(header.commands):
        if load_command.cmd == command_type:
            commands.append((command_index, (load_command, dylib_command, data)))

    return commands

# Dependencies
# -------------------------------------------------------------------------------

def _find_specific_lc_load_dylib(header, dependency_pattern):
    for index, (load_command, dylib_command, data) in \
            _find_lc_dylib_command(header, mach_o.LC_LOAD_DYLIB):
        m = dependency_pattern.search(convert_to_string(data))
        if m:
            return index, (load_command, dylib_command, data)

def _change_dependency_command(header, old_dependency_pattern, new_dependency):
    old_command = _find_specific_lc_load_dylib(header, old_dependency_pattern)
    if old_command is None:
        return
    command_index, command_tuple = old_command
    _change_command_data_inplace(header, command_index, command_tuple, new_dependency)

def dependencies(filename):
    """Returns the list of mach-o the given binary depends on.
    Parameters
    ----------
    filename: str
        Path to the mach-o to query
    Returns
    -------
    dependency_names: seq
        dependency_names[i] is the list of dependencies for the i-th header.
    """
    m = MachO.MachO(filename)
    return _list_dependencies_macho(m)

def _list_dependencies_macho(m):
    ret = []

    for header in m.headers:
        this_ret = []
        for load_command, dylib_command, data in header.commands:
            if load_command.cmd == mach_o.LC_LOAD_DYLIB:
                this_ret.append(convert_to_string(data))
        ret.append(this_ret)
    return ret

def change_dependency(filename, old_dependency_pattern, new_dependency):
    """Change the install name of a mach-o dylib file.
    For a multi-arch binary, every header is overwritten to the same install
    name
    Parameters
    ----------
    filename: str
        Path to the mach-o file to modify
    new_install_name: str
        New install name
    """
    _r_old_dependency = re.compile(old_dependency_pattern)
    m = MachO.MachO(filename)
    for header in m.headers:
        _change_dependency_command(header, _r_old_dependency, new_dependency)

    def writer(f):
        for header in m.headers:
            f.seek(0)
            header.write(f)
    safe_update(filename, writer, "wb")

# RPaths
# ---------------------------------------------------------------------------------------

def list_rpaths(filename):
    """Get the list of rpaths defined in the given mach-o binary.
    The returned value is a list rpaths such as rpaths[i] is the list of rpath
    in the i-th header.
    Note
    ----
    The '\0' padding at the end of each rpath is stripped
    Parameters
    ----------
    filename: str
        The path to the mach-o binary file to look at
    """
    m = MachO.MachO(filename)
    return _list_rpaths_macho(m)

def _list_rpaths_macho(m):
    rpaths = []

    for header in m.headers:
        header_rpaths = []
        rpath_commands = [command for command in header.commands if
                isinstance(command[1], mach_o.rpath_command)]
        for rpath_command in rpath_commands:
            rpath = rpath_command[2]
            if not rpath.endswith(b"\x00"):
                raise ValueError("Unexpected end character for rpath command value: %r".format(rpath))
            else:
                header_rpaths.append(convert_to_string(rpath))
        rpaths.append(header_rpaths)

    return rpaths

def add_rpaths(filename, rpaths):
    """Add the given list of path rpaths to all header in a MachO file.
    Parameters
    ----------
    filename: str
        The path to the macho-o binary file to add rpath to
    rpaths: seq
        List of paths to add as rpath to the mach-o binary
    """
    macho = MachO.MachO(filename)
    for header in macho.headers:
        for rpath in rpaths:
            _add_rpath_to_header(header, rpath)

    def writer(f):
        for header in macho.headers:
            f.seek(0)
            header.write(f)
    safe_update(filename, writer, "wb")

def _add_rpath_to_header(header, rpath):
    """Add an LC_RPATH load command to a MachOHeader.
    Parameters
    ----------
    header: MachOHeader instances
        A mach-o header to add rpath to
    rpath: str
        The rpath to add to the given header
    """
    if header.header.magic in (mach_o.MH_MAGIC, mach_o.MH_CIGAM):
        pad_to = 4
    else:
        pad_to = 8
    data = macho_path_as_data(rpath, pad_to=pad_to)
    header_size = sizeof(mach_o.load_command) + sizeof(mach_o.rpath_command)

    rem = (header_size + len(data)) % pad_to
    if rem > 0:
        data += b'\x00' * (pad_to - rem)

    command_size = header_size + len(data)

    cmd = mach_o.rpath_command(header_size, _endian_=header.endian)
    lc = mach_o.load_command(mach_o.LC_RPATH, command_size,
        _endian_=header.endian)
    header.commands.append((lc, cmd, data))
    header.header.ncmds += 1
    header.changedHeaderSizeBy(command_size)


# Library
# ---------------------------------------------------------------------------------------


class DylibLinkInfo:
    def __init__(self, path):
        self.path = path
        if ( not os.path.exists(path) ):
            raise Exception("Path does not exist:" + path)

        self.dependencies = []
        self.rpath_info = []

        m = MachO.MachO(path)
        deps = _list_dependencies_macho(m)
        if ( len(deps) > 0 ):
            if ( type(deps[0]) is list ):
                self.dependencies = [item for sublist in deps for item in sublist] # Flatten deps
            else:
                self.dependencies = deps

        rpaths = _list_rpaths_macho(m)
        if ( len(rpaths) > 0 ):
            if ( type(rpaths[0]) is list ):
                self.rpath_info = [item for sublist in rpaths for item in sublist] # Flatten rpaths
            else:
                self.rpath_info = rpaths


    def find_dependencies(self, pattern):
        result = []
        for l in self.dependencies:
            if ( fnmatch.fnmatch(l, pattern) ):
                result.append(l)

        return result

    def find_absolute_dependencies(self, pattern):
        result = []
        for l in self.dependencies:
            if ( fnmatch.fnmatch(self.absolute_dependency(l), pattern) ):
                result.append(l)
        return result

    def absolute_dependency(self, dependency):
        if dependency.startswith('@rpath'):
            for index, rp in enumerate(self.rpath_info):
                res = rp + dependency[6:]
                if os.path.exists(res):
                    return res
            return ''
        return dependency

    def add_rpath(self, path):
        add_rpaths(self.path, [path])
        return True

    def change_dependency(self, old, new):
        for index, dep in enumerate(self.dependencies):
            if dep == old:
                change_dependency(self.path, old, new)
                self.dependencies[index] = new
                return True
        return False

    def change_dependencies(self, structure):
        print('Using non external dylib.')
        for old, new in structure.items():
            self.change_dependency(old, new)
        return True

    # This sets the install name of the .dylib file itself and will be used as the prototype 
    # install name from that point forward when something links with the .dylib
    def change_id(self, old, new):
        for index, dep in enumerate(self.dependencies):
            if dep == old:
                changeproc = Process.run(
                    ['install_name_tool', '-id', dep, new, self.path], 
                    os.getcwd()
                )
                changeproc.wait()

                self.dependencies[index] = new
                return True

        return False