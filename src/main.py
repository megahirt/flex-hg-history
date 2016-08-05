'''
Created on Aug 5, 2016

@author: Nathaniel Paulus
'''

import sys, os

def invalid_usage(msg):
    '''
    Print the supplied error message (if it exists), print usage instructions, 
    and then exit the script with exit status 1.
    '''
    
    if msg: print('Error: ' + msg)
    print('Usage: python3 [path to Mercurial repository] [start revision] [end revision]\n'
          'For example: python3 data/sena3/ 18 20')
    sys.exit(1);

def main(args):
    if len(args) != 4:
        invalid_usage('Wrong number of arguments.')
        sys.exit()
    
    path, start, end = args[1:4]
    
    # Validate directory path
    if not os.path.isdir(path):
        invalid_usage('The path {} is not a directory.'.format(path))

    # Validate start and end revisions
    if not start.isdigit() or not end.isdigit():
        invalid_usage('Start and end revisions must be integers.')
    else:
        start, end = int(start), int(end)
        print('Reached end successfully.')

if __name__ == '__main__':
    main(sys.argv);
    