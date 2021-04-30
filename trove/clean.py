'''Tools for cleaning the pipeline.'''
import argparse
import glob
import os
import shutil
import sys

import trove.config_parser as config_parser

########################################################################

def clean( config_fp, clean_jug=True, full_clean=False, verbose=True ):
    '''Function for cleaning up pipeline data.

    Args:
        config_fp (str):
            Config to base the cleaning on.

        clean_jug (bool):
            If True remove any *.jugdata that were created.

        full_clean (bool):
            If True remove the entire data_dirs that were created.
            Use with caution!
    '''

    # As a precaution, convert to absolute path
    config_fp = os.path.abspath( config_fp )

    # Load the config
    tcp = config_parser.ConfigParser( config_fp )

    if verbose: print( 'Cleaning...' )

    # Full clean
    if full_clean:
        if verbose: print( 'Performing full clean...' )
        for data_dir in tcp.data_dirs:
            if os.path.exists( data_dir ):
                if verbose: print( '    Removing {}'.format( data_dir ) )
                shutil.rmtree( data_dir )

        return
    
    # Clean
    for data_filepath in tcp.manager.data_files:
        if os.path.exists( data_filepath ):
            if verbose: print( '    Removing {}'.format( data_filepath ) )
            os.remove( data_filepath )

    # Clean jugdatas
    if clean_jug:
        for data_dir in tcp.data_dirs:
            for extension in [ '*.jugdata', '*.jugdir' ]:
                jugdata_glob = os.path.join( data_dir, extension )
                for jugdata in glob.glob( jugdata_glob ):
                    if verbose: print( '    Removing {}'.format( jugdata ) )
                    shutil.rmtree( jugdata )

########################################################################

if __name__ == '__main__':

    # Parse args
    parser = argparse.ArgumentParser(
        description='Clean and reset your pipeline.'
    )
    parser.add_argument(
        'config_fp',
        type = str,
        help = 'Location of your config file used to guide cleaning.',
    )
    parser.add_argument(
        '--dont_clean_jug',
        help = 'Do not remove .jugdata dirs.',
        action = 'store_true',
    )
    parser.add_argument(
        '--full_clean',
        help = 'Use with caution: fully deletes all data directories!',
        action = 'store_true',
    )
    parser.add_argument(
        '--quiet',
        help = 'Quiet down the output.',
        action = 'store_true',
    )
    args = parser.parse_args()

    # Run
    clean(
        args.config_fp,
        not args.dont_clean_jug,
        args.full_clean,
        not args.quiet,
    )

