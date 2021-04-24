'''Tools for cleaning the pipeline.'''
import os

import trove.config_parser as config_parser

########################################################################

def clean( config_fp ):

    # As a precaution, convert to absolute path
    config_fp = os.path.abspath( config_fp )

    # Load the config
    tcp = config_parser.ConfigParser( config_fp )
    
    # Clean
    for data_filepath in tcp.manager.data_files:
        if os.path.exists( data_filepath ):
            os.remove( data_filepath )

if __name__ == '__main__':

    # Run
    clean( *sys.argv[1:] )

