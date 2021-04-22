#!/usr/bin/env python
'''Tools for running the pipeline.'''

import os
import pathlib
import subprocess
import sys
import time
import warnings

import trove.build as build

########################################################################

def run( config_fp, max_loops=1000, *args, **kwargs ):

    # As a precaution
    config_fp = os.path.abspath( config_fp )

    # Load the config
    tcp = build.ConfigParser( config_fp )

    # Start run loop
    loop_count = 0
    start_time = time.time()
    while True:

        # Identify next to run
        next_variation = tcp.get_next_variation()

        # Check if done
        loop_count += 1
        if next_variation == 'done_flag':
            print(
                '\n####################################' + \
                '####################################\n' + \
                'trove finished in {:.3g} seconds!'.format(
                    time.time() - start_time 
                ) + \
                '\n####################################' + \
                '####################################\n'
            )
            break
        if loop_count >= max_loops:
            warnings.warn(
                'Reached maximum number of loops, {} loops. Exiting.'.format(
                    loop_count,
                )
            )
            break

        # Get filepaths
        current_script = tcp.get( 'SCRIPTS', next_variation[-1] )
        current_flag_file = tcp.get_flag_file( *next_variation )

        # Run
        loop_time = time.time()
        print(
            '\n####################################' + \
            '####################################\n' + \
            'Running {}\n'.format( current_script ) + \
            '    Variation: {}'.format( next_variation[:-1] ) + \
            '\n----------------------------------' + \
            '------------------------------------\n'
        )
        sp = subprocess.run(
            [
                sys.executable,
                current_script,
                config_fp,
            ]
        )

        # When done running mark as done
        print(
            '\n----------------------------------' + \
            '------------------------------------' +
            '\nFinished running {} in {:.3g} seconds\n'.format(
                current_script,
                time.time() - loop_time,
            ) + \
            '    Variation: {}\n'.format( next_variation[:-1] ) + \
            '####################################' + \
            '####################################\n'
        )
        pathlib.Path( current_flag_file ).touch()

########################################################################

if __name__ == '__main__':

    # Run
    run( *sys.argv[1:] )

