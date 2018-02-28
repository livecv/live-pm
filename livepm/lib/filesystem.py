import os
import shutil
import fnmatch

class FileSystem:

    def scriptdir():
        return os.path.dirname(os.path.realpath(__file__))

    def find(name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)
        return ''

    def copyfile(src, dst):
        if os.path.islink(src):
            linkto = os.readlink(src)
            os.symlink(linkto, dst)
        else:
            shutil.copyfile(src, dst)

    def listEntries(src):
        entries = []
        srcfilename = os.path.basename(src)
        if "*" in srcfilename or "?" in srcfilename:
            d = os.path.dirname(src)
            for file in os.listdir(d):
                if fnmatch.fnmatch(file, srcfilename):
                    entries.append(os.path.join(d, file))
        return entries

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
                copiedFiles = 0
                for file in os.listdir(os.path.dirname(src)):
                    if fnmatch.fnmatch(file, srcfilename):
                        dstfile = dst
                        if os.path.basename(os.path.normpath(dst)) == "-":
                            dstfile = dst[0:len(dst) - 1] + file
                        src = os.path.join(os.path.dirname(src), file)
                        print('Copying: \'' + src + '\'\n      -> \'' + dstfile + '\'')
                        FileSystem.copyfile(src, dstfile)
                        copiedFiles += 1

                if ( copiedFiles == 0 ):
                    print('Warning: No files copied for pattern: ' + src)
            else:
                if os.path.basename(os.path.normpath(dst)) == "-":
                    dst = dst[0:len(dst) - 1] + os.path.basename(os.path.normpath(src))
                FileSystem.copyfile(src, dst)
                print('Copying: \'' + src + '\'\n      -> \'' + dst + '\'')

    def copyFileStructure(releaseDir, structure, structurePaths, structurePrefix = ""):
        for key, value in structure.items():
            keywithpath   = key.format_map(structurePaths)
            if isinstance(value, dict):
                FileSystem.copyFileStructure(releaseDir, value, structurePaths, os.path.join(structurePrefix, keywithpath))
            else:
                valuewithpath = value.format(structurePaths)
                FileSystem.copyFileOrDirectory(os.path.join(structurePrefix, keywithpath), releaseDir + valuewithpath)
