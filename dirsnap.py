

#!/usr/bin/env python

#import sys
import os
from os.path import join, getsize
import datetime

from Tkinter import *
import ttk
import tkFileDialog


class Config:
    def __init__(self):
        self.sep = ''
        self.path = ''
        self.out = {}
        self.fileType = ''
        self.timeStamp = False

def setUpAndRecurse(config): 
    # get config values
    config.sep = indentEntry.get()
    config.path = inDirEntry.get()
    config.out = open(outFileEntry.get(), 'w')
    if fileTypeEntry.get() == defaultFileType or fileTypeEntry.get() == 'all':
        config.fileType = '*'
    else:
        config.fileType = fileTypeEntry.get().replace(' ','')
        if config.fileType.find(',') == -1:
            config.fileType = config.fileType.split(',')
    config.includeSize = includeSize.get()

    # begin writing
    if timeStamp.get():
        config.out.write(os.path.basename(config.path))
        config.out.write(' - {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
        config.out.write('\n')
    else:
        config.out.write(os.path.basename(config.path))
        config.out.write('\n')

    recurse(1, config.path, config)

    config.out.close();

    statusBar['text'] = 'Done'


def recurse(dep, path, config):
    dirs, files = dirHelper(path, config)
    if not dirs:
        printFiles(dep, path, files, config)
        return 0


    for item in dirs:
        config.out.write(config.sep * dep)
        config.out.write(item)
        config.out.write('\n')
        recurse(dep + 1, os.path.join(path,item), config)
    
    printFiles(dep, path, files, config)


def dirHelper(path, config):
    dirs = []
    files = []
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            dirs.append(item)
        if os.path.isfile(os.path.join(path, item)):
            if config.fileType != '*':
                if item[item.rfind('.'):] in config.fileType:
                    files.append(item)
            else:
                files.append(item)
    return dirs, files


def printFiles(dep, path, files, config):
    for unit in files:
        if unit != '.DS_Store':
            config.out.write(config.sep * dep)
            config.out.write(unit)
            if config.includeSize:
                config.out.write(' - ' + str(os.path.getsize(os.path.join(path, unit))) + ' bytes')
            config.out.write('\n')





root = Tk()
root.title('Directory Snapshot')
# root.geometry('{}x{}'.format(460, 350))

mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)


# input setup
inDir = ''

def browseFolder():
    from tkFileDialog import askdirectory

    inDir = tkFileDialog.askdirectory()

    inDirEntry.delete(0,END)
    inDirEntry.insert(0,inDir)

    if not outFileEntry.get():
        outFileEntry.insert(0, inDir + '/snapshot.txt')

ttk.Label(mainframe, text='Input Folder').grid(column=1, row=1, sticky=E)

inDirEntry = ttk.Entry(mainframe, width=40, textvariable=inDir)
inDirEntry.grid(column=2, row=1, sticky=(W, E))

ttk.Button(mainframe, text='Browse', command=browseFolder).grid(column=3, row=1, sticky=W)

# output setup
outFile = ''

def browseFile():
    from tkFileDialog import askopenfilename

    outFile = tkFileDialog.askopenfilename()

    outFileEntry.delete(0,END)
    outFileEntry.insert(0,outFile)

ttk.Label(mainframe, text='Output File').grid(column=1, row=2, sticky=E)

outFileEntry = ttk.Entry(mainframe, width=40, textvariable=outFile)
outFileEntry.grid(column=2, row=2, sticky=(W,E))

ttk.Button(mainframe, text='Browse', command=browseFile).grid(column=3, row=2, sticky=W)

# Snap button

def snapshot():
    if not inDirEntry.get():
        inDirEntry.focus()
        statusBar['text'] = 'Missing Input Folder'
        return

    if not outFileEntry.get():
        outFileEntry.focus()
        statusBar['text'] = 'Missing Output File'
        return

    config = Config()

    setUpAndRecurse(config)



ttk.Button(mainframe, text='Snap', width=20, command=snapshot).grid(column=2, row=3)


# Options --------------

optionsFrame = ttk.Labelframe(root, text='Options', padding=(5,5,5,5))
optionsFrame.grid(column=0, row=1, sticky=(N,E,S,W))
optionsFrame.columnconfigure(0, weight=1)
optionsFrame.columnconfigure(1, weight=1)
optionsFrame.columnconfigure(2, weight=1)
optionsFrame.columnconfigure(3, weight=1)


ttk.Label(optionsFrame, text='Indent').grid(column=0,row=0, sticky=E)
indentEntry = ttk.Entry(optionsFrame, width=10)
indentEntry.grid(column=1, row=0, sticky=W)
indentEntry.insert(0,'   ')

ttk.Label(optionsFrame, text='Include Timestamp').grid(column=2, row=0, sticky=E)
timeStamp=BooleanVar()
timeStamp.set(True)
timestampButton = ttk.Checkbutton(optionsFrame, text='', variable=timeStamp)
timestampButton.grid(column=3, row=0, sticky=W)


ttk.Label(optionsFrame, text='Filter by Type').grid(column=0, row=1, sticky=E)
defaultFileType = 'Eg. \'all\' or \'.txt,.jpg\''
fileTypeEntry = ttk.Entry(optionsFrame, width=15)
fileTypeEntry.grid(column=1, row=1, sticky=W)
fileTypeEntry.insert(0,defaultFileType)

ttk.Label(optionsFrame, text='Include Size').grid(column=2, row=1, sticky=E)
includeSize=BooleanVar()
includeSize.set(False)
includeSizeButton = ttk.Checkbutton(optionsFrame, text='', variable=includeSize)
includeSizeButton.grid(column=3, row=1, sticky=W)


statusBar = ttk.Label(root, padding=(10,10,10,5), text='Enter Input Folder and Output File, then Hit Snap')
statusBar.grid(column=0, row=2, sticky=(W,E))


for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

for child in optionsFrame.winfo_children(): child.grid_configure(padx=5, pady=5)

inDirEntry.focus()
# root.bind('<Return>', calculate)

root.mainloop()


