My partner takes a lot of photos. Since smartphones replaced compact cameras for taking photos, everything has been shovelled into Google Photos, but that still left her with thousands of images distributed in a messy filing system with hundreds of folders and no real organization. She owned several computers over that period and each one had a backup of the previous one, so duplication is rife. Everything is in there somewhere, but how does she find it?

There are two ways to deal with the problem. One is to find a tool that will do the job; the other is to write one. The problem with the first of these is that it will take time to find such a tool, largely because I can't figure a suitable question to ask. Having found a tool I then have to learn how to use it. Unless it's top-drawer commercial software it will lack a comprehensive manual, so this part could take hours of not days. Then there's finally the good chance that it won't actually do the job after all, so the whole exercise is wasted. And if the original search came up with several products, everything has to be repeated for each one.

So that leaves writing my own, and here it is. It's called unpick.py and it can be run as a Python command or added to a tools directory (such as /usr/bin for Linux folks).

Running the tool with no arguments outputs some basic help, as follows:
```
A tool to list extensions, copy/delete all files of a given type, remove duplicates etc.
Syntax:
unpick.py [options] [path]
Options (note that many of these are mutually exclusive):
   -types, -extensions, -ext -- list all file extensions
   -list  -- list all files with the given extension
   -duplicates, -dup  -- list all duplicates with the given extension
   -delete, -del -- delete all files with the given extension
   -remove, -rem -- delete all duplicates with the given extension
   -copy -- copy files to target directory
   -move -- move files to target directory
   -type, -extension, -ext -- specify an extension
   -target [path] -- copy/move to this target directory
   -flatten -- don't maintain directory structure in copy/move
   -ignore -- ignore duplicates in copy/move
   -help -- this help message
```
The tool walks any given directory recursively, taking appropriate actions as it goes. Here are some examples of how to use each option (at the time of writing). In each case, `<path>` is the path (absolute or relative) to the directory being scanned:
```
unpick -types <path>
```
Output a list of all the file types (extensions) found in the directory and its subdirectories, with the number of files of that type, sorted most to least.
```
unpick -duplicates -type jpg <path>
```
List all duplicate file names. The first one encountered is taken to be the original and all others duplicates. The fact that the names are the same doesn't necessarily mean they are the same file, of course, so if there's any doubt you'll need to examine the output carefully. Maybe a later version of this tool will examine the content as well as the name.
```
unpick -remove -type png <path>
```
Delete all duplicate files (files with the same name but in different directories). Use `duplicates` first to check these really are the same file. Also be aware that the first instance of any file discovered by unpick is assumed to be the master copy, which may cause the wrong copy to be deleted.
```
unpick -copy -type doc -target <target folder> <path>
```
Copy all files with the given extension, putting them into `target folder`. The same folder hierarchy will be maintained, or you can add the `-flatten` option to force everything to go into a single directory.
```
unpick -move -type pdf -target <target folder> <path>
```
Move all files with the given extension, putting them into `target folder`. This is the same as `copy` but the copied files will be deleted as they are moved.

With both `copy` and `move` you can also add the `-ignore` option to ignore duplicates.

So did it work? Well, after I ran the `copy` once for each wanted file type, the extracted files took up just over 100GB, compared to more than 500GB on the original backup disk. Most of the rest is old emails, ancient Windows executables and so on, none of which need to be kept, and it should now be a lot easier for my partner to find photos, videos or documents should the need arise. The results are far from perfect, as it can still take a while to burrow through the folder hierarchy or to pick the right file from a huge number in one directory, but at least it's an improvement and it does save a lot of space.

I hope others here may also find it useful in pruning the immense piles of clutter we fill our computers with. My next job is to check if a duplicate file name really means an identical file, but if someone else gets there before me I'm happy to use their code.
