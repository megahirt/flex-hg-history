'''
Created on Aug 17, 2016

@author: Nathaniel Paulus
'''
import unittest

from lexentry import LexEntry, equal_xml_nodes
from lexentry import Lexicon
import xml.etree.cElementTree as ET

# Test helper data
root = ET.fromstring('<Lexicon><LexEntry guid="fe3514ca-e963-4c15-9d26-badc670770f3">'
                     '<SomeRandomElement></SomeRandomElement></LexEntry></Lexicon>')
node = list(root)[0]

entries = [
'<LexEntry guid="8e45de56-5105-48dc-b302-05985432e1e7"><Elm></Elm></LexEntry>',
'<LexEntry guid="fe3514ca-e963-4c15-9d26-badc670770f3"><SomeRandomElement></SomeRandomElement></LexEntry>',
'<LexEntry guid="d7f713e5-e8cf-11d3-9764-00c04f186933"><C></C></LexEntry>',
'<LexEntry guid="3ecbfcc8-76d7-43bc-a5ff-3c47fabf355c"><Erm></Erm></LexEntry>',
# This entry will reuse a GUID be differ in other ways
'<LexEntry guid="fe3514ca-e963-4c15-9d26-badc670770f3"><A></A></LexEntry>',
'<LexEntry guid="868bdd38-b9c2-4e82-86f6-b479c67f628c"><B></B></LexEntry>'
]


class TestLexEntry(unittest.TestCase):

    def test_lexentry(self):
        entry = LexEntry(node)
        self.assertEqual(entry.guid, node.attrib['guid'])

class TestLexicon(unittest.TestCase):
    
    def test_lexicon(self):
        lex = Lexicon()
        entry = LexEntry(node)
        lex.addEntry(entry)
        self.assertEqual(len(lex.entries), 1)
        
    def test_compare(self):
        # Construct two lexicons that differ slightly
        
        old = Lexicon()
        for entry in entries[:4]:
            old.addEntry(LexEntry(ET.fromstring(entry)))
        
        new = Lexicon()
        for entry in entries[2:]:
            new.addEntry(LexEntry(ET.fromstring(entry)))
        
        self.assertEqual(old.compare(new), (1,1,1))


class TestEqualXMLNodes(unittest.TestCase):
    
    def test_equal_xml_nodes(self):
        for entry in entries:
            # Using == would result in False
            self.assertTrue(equal_xml_nodes(ET.fromstring(entry), ET.fromstring(entry)))
