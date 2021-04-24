'''Tools for converting existing code to a trove-compatible format.'''
import os
import pathlib

import trove.config_parser as config_parser

########################################################################

def convert( config_fp ):
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

    # Mapping between ids and possible files
    ids = [
        _ for _ in tcp['CONVERSION'].keys()
        if _ not in tcp.defaults()
    ]
    possible_files = [ tcp.get( 'CONVERSION', _ ) for _ in ids ]

    # Loop and look for existing files
    for data_dir in tcp.data_dirs:
        for i, filename in enumerate( possible_files ):
            if os.path.exists( os.path.join( data_dir, filename ) ):
                troveflag_fp = os.path.join( data_dir, ids[i] + '.troveflag' )
                pathlib.Path( troveflag_fp ).touch()

########################################################################

if __name__ == '__main__':

    # Run
    convert( *sys.argv[1:] )

