'''
Created on Aug 5, 2016

@author: Nathaniel Paulus
'''
import unittest, diff

repo = '../data/sena3'

class TestDiff(unittest.TestCase):
    
    def test_diff_revisions(self):
        # Note: These tests are slow. Temporarily comment them out if they are 
        # slowing you down too much.
        
        self.assertEqual(diff.diff_revisions(repo, 13, 14), (0, 2, 1))
        self.assertEqual(diff.diff_revisions(repo, 17, 18), (0, 1, 0))
        self.assertEqual(diff.diff_revisions(repo, 18, 19), (1, 0, 0))
        self.assertEqual(diff.diff_revisions(repo, 19, 20), (0, 4, 0))

        # Oddly, the lexical entry with GUID 24deb938-d6b8-4827-b563-4bd1f7d18e23 
        # is removed in revision 14, but added in version 19. Not sure what the 
        # implications of that are. 
        self.assertEqual(diff.diff_revisions(repo, 13, 20), (0, 5, 0)) 

    def test_run_process(self):
        '''
        Should be able to run Python and exit successfully.
        '''
        output = diff.stdout(['python3', '-c', 'print("hello world")'], repo)
        self.assertEqual(output, 'hello world\n', )
        
    def test_status_code(self):
        self.assertEqual(diff.status_code(['python3', '--version']), 0)
    
    def test_hgcat(self):
        self.assertTrue(diff.hgcat('Linguistics/Lexicon/Lexicon_05.lexdb', 20, repo).endswith('</Lexicon>'))
    
    def test_guids(self):
        self.assertEqual(diff.guids(''), [])
        xml = '<Lexicon><LexEntry guid="fe3514ca-e963-4c15-9d26-badc670770f3"></LexEntry></Lexicon>'
        self.assertEqual(diff.guids(xml), ['fe3514ca-e963-4c15-9d26-badc670770f3'])
        
    def test_authors(self):
        self.assertEqual(diff.authors(repo, 12, 20), ['chris', 'www-data'])
        