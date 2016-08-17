'''
Created on Aug 5, 2016

@author: Nathaniel Paulus
'''

import subprocess, os
from subprocess import CalledProcessError
import xml.etree.cElementTree as ET

def diff_revisions(path, a, b):
    '''
    Compare two revisions, a and b, of the FLEx dictionary at the specified 
    path.
    Return a tuple containing the number of entries added and removed (in that
     order). 
    '''
    command = ['hg', 'status', '--rev', str(a), '--rev', str(b)]
    status = run_process(command, path)
    if status.returncode != 0:
        raise CalledProcessError(status.returncode, command)
    
    changed_files = str(status.stdout).strip().splitlines()

    # Parse the line, which looks something like: M path/to/file.txt
    # Status is M when the file has been modified, A for added, and R for 
    # removed. Other options (https://selenic.com/hg/help/status) are C, !, 
    # ?, I, and the space character. Should only need M, A, and R (at least 
    # for now).
    
    files = []
    
    for file in changed_files:
        
        # Ignore files that don't end with .lexdb
        if not file.endswith('.lexdb'):
            continue
        
        status, name = file[0:1], file[2:]

        # Store the current and original versions of the file in a tuple
        if status == 'A':
            files.append(('', hgcat(name, b, path)))
        elif status == 'M':
            files.append((hgcat(name, a, path), hgcat(name, b, path)))
        elif status == 'R':
            files.append((hgcat(name, a, path)), '')
        else:
            raise Exception("Script currently only handles files modified, added, or removed.")
    
    original_guids, current_guids = [], []
    
    for file in files:
        # Add the original and current GUIDs to their respective lists
        original_guids.extend(guids(file[0]))
        current_guids.extend (guids(file[1]))

    original_guids, current_guids = set(original_guids), set(current_guids)
    
    # Return a tuple with the number of entries added and removed
    return len(current_guids - original_guids), len(original_guids - current_guids)

    

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

def run_process(args, cwd=None):
    '''
    Return the CompletedProcess instance resulting form running a subprocess 
    with the specified arguments, and with the specified CWD. Pipe stdout to 
    the Python process so it can be accessed via the returned CompletedProcess 
    object.
    '''
    # TODO change to using an older function for spawning subprocess
    return subprocess.run(args, cwd=cwd, env=env, stdout=subprocess.PIPE, universal_newlines=True)

def hgcat(file, rev, cwd):
    '''
    Run `hg cat` to find the given file at the given version.
    Use the cwd given as the path to the Mercurial repository.
    '''
    return run_process(['hg', 'cat', '--rev', str(rev), file], cwd).stdout
