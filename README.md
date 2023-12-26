My partner takes a lot of photos. Since smartphones replaced compact cameras for taking photos, everything has been shovelled into Google Photos, but that still left her wit thousands of images distributed in a messy filing system with hundreds of folders and no real organization. She owned several computers over that period and each one had a backup of the previous one, so duplication is rife. Everything is in there somewhere, but how does she find it?

There are two ways to deal with the problem. One is to find a tool that will do the job; the other is to write one. The problem with the first of these is that it will take time to find such a tool, largely because I can't figure a suitable question to ask. Having found a tool I then have to learn how to use it. Unless it's top-drawer commercial software it will lack a comprehensive manual, so this part could take hours of not days. Then there's finally the good chance that it won't actually do the job after all, so the whole exercise is wasted. And if the original search came up with several products, everything has to be repeated for each one.

So that leaves writing my own. It's the Christmas break right now, so what better time, with none of the usual work pressures. I decided to write the thing in command-line Python; you'll find the code in the EasyCoder repository at http://xxxxxxx. By the time you read this the repo version may well have moved on, so the documentation below may well be out of date.

Running the tool with no arguments outputs some basic help, as follows:
```
A tool to list extensions, copy/delete all files of a given type, remove duplicates etc.
Syntax:
pruner.py [options] [path]
Options:
   -mode types -- list all extensions
   -mode listdup  -- list all duplicates with the given extension
   -mode deldup -- delete all duplicates with the given extension
   -mode copy -- copy files to target directory
   -mode move -- move files to target directory
   -ext -- specify an extension
   -target [path] -- specify the target directory
   -flatten -- don't maintain directory structure in copy/move
   -ignore -- ignore duplicates in copy/move
   -help -- this help message
```
The tool walks any given directory recursively, taking appropriate actions as it goes. Here are examples of how to use each option (at the time of writing). In each case, `<path>` is the path (absolute or relative) to the directory bing scanned:
```
pruner.py -mode types <path>
```
Output a list of all the file types (extensions) found in the directory and its subdirectories, with the number of files of that type, sorted most to least.
```
pruner.py -mode listdup -ext jpg <path>
```
List all duplicate file names. The first one encountered is take to be the original and all others duplicates. The fact that tne names are the same doesn't necessarily mean they are the same file, of course, so if there's any doubt you'll need to examine the output carefully.
```
pruner.py -mode deldup -ext png <path>
```
Delete all duplicate files (files with the same name but in different directories). Use `listdup` first to check these really are duplicates.
```
pruner.py -mode copy -ext doc -target <target folder> <path>
```
Copy all files with the given extension, putting them into `target folder`. The same folder hierarchy will be maintained, or you can add the `-flatten` option to force everything to go into a single directory.
```
pruner.py -mode move -ext doc -target <target folder> <path>
```
move all files with the given extension, putting them into `target folder`. This is the same as `copy` but the copied files will be deleted as they are moved.

With both `copy` and `move` you can also add the `-ignore` option to ignore duplicates.

After I ran the `copy` once for each wanted file type, the extracted files took up just offer 100GB, compared to over 500GB on the original backup disk. Most of the rest is old emails, ancient Windows executables and so on, none of which need to be kept, and it should now be a lot easier for my partner to find photos, videos or documents should the need arise. I hope others here may also find it useful in pruning the immense piles of clutter we fill our computers with. My next job is to check if a duplicate file name really means an identical file, but if someone else gets there before me I'm happy to use their code.
