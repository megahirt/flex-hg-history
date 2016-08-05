'''
Created on Aug 5, 2016

@author: Nathaniel Paulus
'''

import unittest, main

class TestMain(unittest.TestCase):
    
    def test_main(self):
        '''
        Script should exit when supplied with invalid arguments.
        '''
        with self.assertRaises(SystemExit):
            main.main([]);
        with self.assertRaises(SystemExit):
            main.main(['python3', '/path/to/dir', '19', '20'])
        # Relies on existence of Fieldworks Language Explorer database in the 
        # project directory.
        with self.assertRaises(SystemExit):
            main.main(['python3', '../data/sena3', '18', '24.6'])
            