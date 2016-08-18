'''
Created on Aug 5, 2016

@author: Nathaniel Paulus
'''

import subprocess, os
import xml.etree.cElementTree as ET
from lexentry import LexEntry
from lexentry import Lexicon

def diff_revisions(cwd, a, b):
    '''
    Compare two revisions, a and b, of the FLEx dictionary at the path specified 
    by cwd.
    Return a tuple containing the number of entries (added, modified, removed). 
    '''
    command = ['hg', 'status', '--rev', str(a), '--rev', str(b)]
    hg_status = stdout(command, cwd)
    
    changed_files = hg_status.strip().splitlines()

    # The old and new lexicons, to be diffed later
    old, new = Lexicon(), Lexicon()
    
    for file in changed_files:
        
        # Ignore files that don't end with .lexdb
        if not file.endswith('.lexdb'):
            continue
        
        # Parse the line, which looks something like: M path/to/file.txt
        # Status is M when the file has been modified, A for added, and R for 
        # removed. Other options (https://selenic.com/hg/help/status) are C, !, 
        # ?, I, and the space character. Should only need M, A, and R (at least 
        # for now).    
        status, name = file[0:1], file[2:]

        if status != 'A' and status != 'M' and status != 'R':
            raise Exception("Script currently only handles files modified, added, or removed.")
        
        # If the file wasn't added between revisions, then the original exists
        # Add the entries to the lexicon
        if status != 'A':
            for child in ET.fromstring(hgcat(name, a, cwd)):
                if child.tag != "LexEntry": continue
                old.addEntry(LexEntry(child))
        # And, if it wasn't removed, there must be a current version
        if status != 'R':
            for child in ET.fromstring(hgcat(name, b, cwd)):
                if child.tag != "LexEntry": continue
                new.addEntry(LexEntry(child))
    
    return old.compare(new)
    

def authors(cwd, a, b):
    '''
    List the users who made changes between revisions a and b, in the repo
    specified by cwd.
    '''
    changes = stdout(['hg', 'log', '--rev', '{}:{}'.format(a+1, b)], cwd)
    users = []
    
    for line in changes.strip().splitlines():
        if line.startswith('user:        '):
            users.append(line[len('user:        '):])
    
    # Remove duplicates (using a set wouldn't preserve order)
    unique_users = []
    for user in users:
        if user in unique_users: continue
        else: unique_users.append(user)
    
    return list(unique_users)

# Declare the environment for subprocesses, removing PYTHONPATH. This is 
# Necessary when PYTHONPATH is set for Python 3 (not always the case), because
# Mercurial is written in Python 2.
env = os.environ.copy()
if 'PYTHONPATH' in env: del env['PYTHONPATH']

def guids(xml):
    '''
    Find and return the GUIDs of the LexEntry's in the given XML.
    
    If the specified XML is an empty string, return an empty array. Otherwise 
    return a list of GUIDs that are on LexEntry tags. 
    '''
    
    if xml == '':
        return []
    
    ids = []
    root = ET.fromstring(xml)
    for child in root:
        if child.tag == "LexEntry":
            ids.append(child.attrib['guid'])
            
    return ids

def stdout(args, cwd=None):
    '''
    Return the stdout form running a subprocess with the specified arguments, 
    and with the specified CWD. Raise a CalledProcessError if the return code 
    is not 0.
    '''
    return subprocess.check_output(args, cwd=cwd, env=env, universal_newlines=True)
    
def status_code(args, cwd=None):
    '''
    Run a process with the specified args and return the status code. Use cwd
    as the CWD for the child process.
    '''
    return subprocess.call(args, cwd=cwd, env=env, stdout=subprocess.DEVNULL)

def hgcat(file, rev, cwd):
    '''
    Run `hg cat` to find the given file at the given version.
    Use the cwd given as the path to the Mercurial repository.
    '''
    return stdout(['hg', 'cat', '--rev', str(rev), file], cwd)
