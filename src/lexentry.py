'''
Created on Aug 17, 2016

@author: Nathaniel Paulus

'''

class LexEntry(object):
    '''
    Represents a lexical entry in a .lexdb file.
    '''

    def __init__(self, node):
        '''
        Constructs a lexical entry.
        
        The parameter node is the XML node from which to construct the lexical 
        entry.
        '''
        assert node.tag == "LexEntry"
        self.guid = node.attrib['guid']
        self.data = node

class Lexicon:
    '''
    Represents a group of lexical entries (class LexEntry).
    Primary purpose is to track additions, deletions, and modifications to 
    lexical entries in the lexicon.
    '''
    
    def __init__(self):
        self.entries = dict()
    
    def addEntry(self, entry):
        '''
        Add the given LexEntry to the lexicon.
        '''
        # Map entry to GUID (even though the entry contains its GUID)
        self.entries[entry.guid] = entry
    
    def compare(self, other):
        '''
        Compare this lexicon with another one.
        Return a tuple of entries (added, modified, removed). Assume this 
        lexicon is the original, and that entries present in it but not present 
        in the other lexicon have been removed, and vice-versa. Consider an
        entry modified if an entry with the same GUID may be found in the other 
        lexicon, but the entries are not identical.
        '''
        
        # Create sets of GUIDs
        a, b = set(self.entries.keys()), set(other.entries.keys())
        
        # Calculate added and removed entries
        added = len(b - a)
        removed = len(a - b)
        
        # Calculate modified entries
        modified = 0
        
        for guid in a & b:
            if not equal_xml_nodes(self.entries[guid].data, other.entries[guid].data):
                modified += 1
        
        return (added, modified, removed)

def equal_xml_nodes(a, b):
    '''
    Compare two XML nodes and return true if they're semantically equal, 
    otherwise return false. Simply comparing with == will return false 
    whether they're identical or not.
    '''
    if a.tag    != b.tag:    return False
    if a.text   != b.text:   return False
    if a.tail   != b.tail:   return False
    if a.attrib != b.attrib: return False
    if len(a)   != len(b):   return False
    for a2, b2 in zip(a, b):
        if not equal_xml_nodes(a2, b2): return False
    
    return True
