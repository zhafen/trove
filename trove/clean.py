'''Tools for cleaning the pipeline.'''
import glob
import os
import shutil

import trove.config_parser as config_parser

########################################################################

def clean( config_fp, full_clean=False, clean_jug=True ):

    # As a precaution, convert to absolute path
    config_fp = os.path.abspath( config_fp )

    # Load the config
    tcp = config_parser.ConfigParser( config_fp )
    
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

