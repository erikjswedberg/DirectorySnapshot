## Directory Snapshot

A nifty python program to record directory trees.  Useful for recording versions of libaries as they change and grow

### Usage

Open with `python dirsnap.py` or `/path/to/python /path/to/dirsnap.py`

Required: Input Folder to scan and Output File to save the folder/file tree to (default for output is Input Folder)

### Features

- Indent, choose which characters denote folder levels (default: `   `)
- Timestamp of snapshot
- Filter by File Type
   - Leave as is for all file types (or use `all`)
   - `.txt` would include only text files (as well as the folder structure)
   - `.txt,.jpg,.png` would include text, jpeg, and png files (as well as the folder structure)
- Include File Size 


### Todo

- Include created date (multi platform issues)
- Order By, drop down (A-Z, size, createddate)
- Folders First Checkbox (listing files then folders, or folders then files)
  - (files, then recurse vs recurse, then files)
- Package application with python to make multiplatform executable
  - cx_freeze? other
- Specialty Metadata
  - Packages for images or video files
  - Options -> General Options, then panes for Image Options, Video Options
- Order By Size
  - Trivial solution: at each stage, use os.walk and sum the os.path.getsize bytes.  Highly inefficient as this would be O(nlogn) time
    - current structure cannot backtrack.  Once visited, printed.
  - Better solution: restructure code to recurse to recreate the tree in memory, then as recursion bubbles up add byte sum member to the in-memory tree node.  Then, once complete, recurse to simply print out the tree keeping O(n) time
- Restructure code to be non global. Classify, organize, componentize, etc
