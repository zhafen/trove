'''Tools for cleaning the pipeline.'''
import glob
import os
import shutil
import sys

import trove.config_parser as config_parser

########################################################################

def clean( config_fp, clean_jug=True, full_clean=False ):
    '''Function for cleaning up pipeline data.

    Args:
        config_fp (str):
            Config to base the cleaning on.

        clean_jug (bool):
            If True remove any *.jugdir that were created.

        full_clean (bool):
            If True remove the entire data_dirs that were created.
            Use with caution!
    '''

    # As a precaution, convert to absolute path
    config_fp = os.path.abspath( config_fp )

    # Load the config
    tcp = config_parser.ConfigParser( config_fp )

    # Full clean
    if full_clean:
        for data_dir in tcp.data_dirs:
            if os.path.exists( data_dir ):
                shutil.rmtree( data_dir )

        return
    
    # Clean
    for data_filepath in tcp.manager.data_files:
        if os.path.exists( data_filepath ):
            os.remove( data_filepath )

    # Clean jugdirs
    for data_dir in tcp.data_dirs:
        jugdir_glob = os.path.join( data_dir, '*.jugdir' )
        for jugdir in glob.glob( jugdir_glob ):
            shutil.rmtree( jugdir )

########################################################################

if __name__ == '__main__':

    # Run
    clean( *sys.argv[1:] )

