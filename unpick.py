#! /usr/bin/python3

# unpick.py

import sys, os, pathlib, shutil

extensions = dict()
files = dict()
duplicates = dict()
option_extension = None
option_target = None
option_types = False
option_list = False
option_duplicates = False
option_copy = False
option_move = False
option_delete = False
option_remove = False
option_flatten = False
option_ignore = False
option_help = False
path = None

###############################################################################
# List all the different extensions for files under the given path
def getExtensions(path):
    global extensions
    for f in os.listdir(path):
        if f[0] != '.':
            p = os.path.join(path, f)
            if os.path.isdir(p):
                getExtensions(p)
            else:
                parts = p.split('.')
                if len(parts) > 1:
                    ext = parts[len(parts) - 1].lower()
                    if len(ext.split('/')) == 1 and not ext.isnumeric():
                        if ext in extensions:
                            extensions[ext] = extensions[ext] + 1
                        else:
                            extensions[ext] = 1

###############################################################################
# List all files with a given extension
def listFiles(path):
    global extension, files, delete
    for f in os.listdir(path):
        if f[0] != '.':
            p = os.path.join(path, f)
            if os.path.isdir(p):
                listFiles(p)
                if len(os.listdir(path)) == 0:
                    pathlib.Path.rmdir(path)
            else:
                parts = p.split('.')
                if len(parts) > 0:
                    ext = parts[len(parts) - 1].lower()
                    if ext == option_extension:
                        print(p)

###############################################################################
# List all duplicate files with a given extension
def listDuplicates(path):
    global extension, files, delete
    for f in os.listdir(path):
        if f[0] != '.':
            p = os.path.join(path, f)
            if os.path.isdir(p):
                listDuplicates(p)
                if len(os.listdir(path)) == 0:
                    pathlib.Path.rmdir(path)
            else:
                parts = p.split('.')
                if len(parts) > 0:
                    ext = parts[len(parts) - 1].lower()
                    if ext == option_extension:
                        if f in files:
                            print(f'Original: {files[f]}')
                            print(f'Duplicate: {p}')
                        else:
                            files[f] = p

###############################################################################
# Copy a file to the target directory
def copyFile(f):
    global option_target
    parts = f.split('/')
    if option_flatten:
        if not os.path.exists(option_target):
            os.makedirs(option_target)
        cf = f'{option_target}/{parts[-1]}'
        print(f'Copy {f} to {cf}')
        shutil.copyfile(f, cf)
    else:
        cf = f'{option_target}/{f}'
        dirs = f'{option_target}/{"/".join(parts[:-1])}'
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        print(f'Copy {f}\nto {cf.replace("//", "/")}')
        shutil.copyfile(f, cf)

###############################################################################
# Copy all files with a given extension
def copy(path):
    global extension, files, ignore
    for f in os.listdir(path):
        if f[0] != '.':
            p = os.path.join(path, f)
            if os.path.isdir(p):
                copy(p)
            else:
                parts = p.split('.')
                if len(parts) > 0:
                    ext = parts[len(parts) - 1].lower()
                    if ext == option_extension:
                        if f in files:
                            if not option_ignore:
                                copyFile(p)
                        else:
                            files[f] = True
                            copyFile(p)

###############################################################################
# Move all files with a given extension
def move(path):
    global extension, files, target, ignore
    for f in os.listdir(path):
        if f[0] != '.':
            p = os.path.join(path, f)
            if os.path.isdir(p):
                move(p)
            else:
                parts = p.split('.')
                if len(parts) > 0:
                    ext = parts[len(parts) - 1].lower()
                    if ext == option_extension:
                        if f in files:
                            if not option_ignore:
                                copyFile(p)
                            os.unlink(p)
                        else:
                            files[f] = True
                            copyFile(p)
                            os.unlink(p)

###############################################################################
# Delete all files with a given extension
def deleteFiles(path):
    global extension, files, delete
    for f in os.listdir(path):
        if f[0] != '.':
            p = os.path.join(path, f)
            if os.path.isdir(p):
                deleteDuplicates(p)
                if len(os.listdir(path)) == 0:
                    pathlib.Path.rmdir(path)
            else:
                parts = p.split('.')
                if len(parts) > 0:
                    ext = parts[len(parts) - 1].lower()
                    if ext == option_extension:
                        print(f'Delete {p}')
                        os.unlink(p)

###############################################################################
# Delete all duplicate files with a given extension
def deleteDuplicates(path):
    global extension, files, delete
    for f in os.listdir(path):
        if f[0] != '.':
            p = os.path.join(path, f)
            if os.path.isdir(p):
                deleteDuplicates(p)
                if len(os.listdir(path)) == 0:
                    pathlib.Path.rmdir(path)
            else:
                parts = p.split('.')
                if len(parts) > 0:
                    ext = parts[len(parts) - 1].lower()
                    if ext == option_extension:
                        if f in files:
                            print(f'Delete {p}')
                            os.unlink(p)
                        else:
                            files[f] = True

###############################################################################
def showHelp():
    print('A recursive tool to list extensions, copy/delete all files\nof a given type, remove duplicates etc.')
    print('Syntax:\nunpick.py [options] [path]')
    print('Options (note that many of these are mutually exclusive):')
    print('   -types, -extensions, -ext -- list all file extensions')
    print('   -list  -- list all files with the given extension')
    print('   -duplicates, -dup  -- list all duplicates with the given extension')
    print('   -delete, -del -- delete all files with the given extension')
    print('   -remove, -rem -- delete all duplicates with the given extension')
    print('   -copy -- copy files to target directory')
    print('   -move -- move files to target directory')
    print('   -type, -extension, -ext -- specify the extension')
    print('   -target [path] -- copy/move to this target directory')
    print('   -flatten -- don\'t maintain directory structure in copy/move')
    print('   -ignore -- ignore duplicates in copy/move')
    print('   -help -- this help message')

###############################################################################
###############################################################################
# Program starts here
# Scan the command-line arguments
if len(sys.argv) == 1:
    option_help = True
else:
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg[0] == '-':
            option = arg[1:]
            if option == 'types' or option == 'extensions' or option == 'ext':
                option_types = True
            elif option == 'type' or option == 'extension' or option == 'ext':
                i = i + 1
                option_extension = sys.argv[i]
            elif option == 'target':
                i = i + 1
                option_target = sys.argv[i]
            elif option == 'list':
                option_list = True
            elif option == 'duplicates' or option == 'dup':
                option_duplicates = True
            elif option == 'copy':
                option_copy = True
            elif option == 'move':
                option_move = True
            elif option == 'delete' or option == 'del':
                option_delete = True
            elif option == 'remove' or option == 'rem':
                option_remove = True
            elif option == 'flatten':
                option_flatten = True
            elif option == 'ignore':
                option_ignore = True
            elif option == 'help':
                option_help = True
        else:
            path = arg
        i = i + 1

###############################################################################
# Perform the requested operation
if option_help:
    showHelp()
elif not option_types and not option_list and not option_duplicates and not option_delete and not option_remove and not option_copy and not option_move:
    print('No action (types, list, duplicates, delete, remove, copy or move) has been specified')
else:
    if option_types:
        if path == None:
            print('No path has been specified')
        else:
            getExtensions(path)
            tmp = []
            for ext, count in extensions.items():
                tmp.append((count, ext))
            tmp = sorted(tmp, reverse=True)
            for (count, ext) in tmp:
                print(f'{ext} {count}')

    elif option_list:
        if option_extension == None:
            print('No extension has been specified')
        else:
            listFiles(arg)

    elif option_duplicates:
        if option_extension == None:
            print('No extension has been specified')
        else:
            listDuplicates(arg)

    elif option_copy:
        if option_extension == None:
            print('No extension has been specified')
        elif option_target == None:
            print('No target directory has been specified')
        elif path == None:
            print('No path has been specified to copy from')
        else:
            target = f'{option_target}/{option_extension}'
            print(f'Copy from {path} to {target}')
            copy(path)

    elif option_move:
        if option_extension == None:
            print('No extension has been specified')
        elif option_target == None:
            print('No target directory has been specified')
        elif path == None:
            print('No path has been specified to move from')
        else:
            target = f'{option_target}/{option_extension}'
            print(f'Move from {path} to {target}')
            move(path)

    elif option_delete:
        if option_extension == None:
            print('No extension has been specified')
        elif path == None:
            print('No path has been specified')
        else:
            deleteFiles(path)

    elif option_remove:
        if option_extension == None:
            print('No extension has been specified')
        elif path == None:
            print('No path has been specified')
        else:
            deleteDuplicates(path)

    elif option_help:
        showHelp()
