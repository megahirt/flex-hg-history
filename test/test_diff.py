'''
Created on Aug 5, 2016

@author: Nathaniel Paulus
'''
import unittest, diff

class TestDiff(unittest.TestCase):
    
    def test_diff_revisions(self):
        # Note: These tests are slow. Temporarily comment them out if they are 
        # slowing you down too much.
        
        self.assertEqual(diff.diff_revisions('../data/sena3', 13, 14), (0, 1))
        self.assertEqual(diff.diff_revisions('../data/sena3', 17, 18), (0, 0))
        self.assertEqual(diff.diff_revisions('../data/sena3', 18, 19), (1, 0))
        self.assertEqual(diff.diff_revisions('../data/sena3', 19, 20), (0, 0))

        # The following test incorrectly assumes that a GUID removed will not 
        # be re-added. It so happens that 24deb938-d6b8-4827-b563-4bd1f7d18e23 
        # is removed in revision 14, but added in version 19. Not sure what the 
        # implications of that are. 
        #self.assertEqual(diff.diff_revisions('../data/sena3', 13, 20), (1, 1))        

    def test_run_process(self):
        '''
        Should be able to run Python and exit successfully.
        '''
        completed = diff.run_process(['python', '--version'])
        self.assertEqual(completed.returncode, 0)
    
    def test_hgcat(self):
        self.assertTrue(diff.hgcat('Linguistics/Lexicon/Lexicon_05.lexdb', 20, '../data/sena3').endswith('</Lexicon>'))
    
    def test_guids(self):
        self.assertEqual(diff.guids(''), [])
        xml = '<Lexicon><LexEntry guid="fe3514ca-e963-4c15-9d26-badc670770f3"></LexEntry></Lexicon>'
        self.assertEqual(diff.guids(xml), ['fe3514ca-e963-4c15-9d26-badc670770f3'])