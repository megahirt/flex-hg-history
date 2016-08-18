# flex-hg-history

**Python script to show how many changes have been made to a FLEx project between two revisions.**

**Usage:**
```
python3 main.py <flex project location> <rev1> <rev2>
```

**Example:**
```
python3 main.py language_project/data/sena3 15 20
```

**Example output:**
```
Summary of changes to lexical entries from revision 15 to 20: 
    Added: 4
    Modified: 6
    Removed: 3
These changes were made by the following users: 
    Bob
    Alice
```

