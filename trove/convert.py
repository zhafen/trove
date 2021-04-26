'''Tools for converting existing code to a trove-compatible format.'''
import glob
import os
import pathlib
import sys

import trove.config_parser as config_parser

########################################################################

def convert( config_fp, verbose=True ):
    '''Look for data files that mark a part of the trove process as complete
    and mark them as done.

    Args:
        config_fp (str):
            Config to use for the conversion process. Must contain a section
            titled "CONVERSION".
    '''

    # As a precaution, convert to absolute path
    config_fp = os.path.abspath( config_fp )

    # Load the config
    tcp = config_parser.ConfigParser( config_fp )

    if verbose:
        print( 'Determining progress. Found data products for the following:' )

    # Loop and look for existing files
    for filepath in tcp.manager.data_files:
        # Split into parameters
        data_dir, troveflag = os.path.split( filepath )
        script_id = '.'.join( troveflag.split( '.' )[:-1] )

        # Skip files we're not given an option for
        if not tcp.has_option( 'CONVERSION', script_id ):
            continue

        # Find what to search for
        filename = tcp.get( 'CONVERSION', script_id )
        filepath = os.path.join( data_dir, filename )

        # Check if it exists
        filepath = os.path.join( data_dir, filename )
        if len( glob.glob( filepath ) ) > 0:
            if verbose: print( '    {} | {}'.format( script_id, data_dir ) )
            troveflag_fp = os.path.join( data_dir, script_id + '.troveflag' )
            pathlib.Path( troveflag_fp ).touch()

########################################################################

if __name__ == '__main__':

    # Run
    convert( *sys.argv[1:] )

