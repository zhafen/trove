#!/usr/bin/env python
'''Tools for running the pipeline.'''
import argparse
import jug
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os
import pathlib
import subprocess
import sys
import time
import warnings

import trove.config_parser as config_parser

########################################################################

def run( config_fp, n_procs=4, max_loops=1000, cell_timeout=1200 ):
    '''Run the trove pipeline specified in the given config.

    Args:
        config_fp (str):
            Configuration file to use.

        n_procs (int):
            Number of processors to use when running a jug file.

        max_loops (int):
            Maximum loops before forcibly exiting.

        cell_timeout (float or int):
            Allowed execution time per cell when executing notebooks.
    '''

    # As a precaution, convert to absolute path
    config_fp = os.path.abspath( config_fp )

    # Load the config
    tcp = config_parser.ConfigParser( config_fp )

    # Start run loop
    loop_count = 0
    start_time = time.time()
    while True:

        # Identify next to run
        next_variation = tcp.get_next_variation()
        next_global_variation = tcp.get_next_global_variation()

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
        script_id = next_variation[-1]
        current_script = tcp.get( 'SCRIPTS', script_id )
        global_id = tcp.format_global_variation( next_global_variation )
        current_flag_file = tcp.get_flag_file( global_id, *next_variation )

        # Run start announcement
        loop_time = time.time()
        print(
            '\n####################################' + \
            '####################################\n' + \
            'Running {}\n'.format( current_script ) + \
            '    Variation: {}'.format( next_variation[:-1] ) + \
            '\n----------------------------------' + \
            '------------------------------------\n'
        )

        # Run
        prefix = script_id.split( '.' )[0]
        if prefix == 'py':
            run_output = run_python(
                current_script,
                config_fp,
            )
        elif prefix == 'nb':
            run_output = run_python_notebook(
                current_script,
                config_fp,
                tcp.get_next_data_dir(),
                timeout = cell_timeout,
            )
        elif prefix == 'jug':
            run_output = run_jug(
                current_script,
                config_fp,
                tcp.get_next_data_dir(),
                script_id,
                n_procs,
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

def run_python( script_fp, config_fp ):
    '''Code for running a python program.

    Args:
        script_fp (str):
            Python script to run.

        config_fp (str):
            Config filepath, passed as a commandline arg to the script.

    Returns:
        subprocess.SubProcess:
            Subprocess output.
    '''

    sp = subprocess.run(
        [
            sys.executable,
            script_fp,
            config_fp,
        ]
    )

    return sp

def run_python_notebook( script_fp, config_fp, output_dir, timeout=1200 ):
    '''Code for running a python notebook.

    Args:
        script_fp (str):
            Python script to run.

        config_fp (str):
            Config filepath, passed as a commandline arg to the script.

        output_dir (str):
            Where to store any products from running the script.

    Returns:
        subprocess.SubProcess:
            Subprocess output.
    '''

    # Read
    with open( script_fp ) as f:
        nb = nbformat.read( f, as_version=4 )

    # Run
    ep = ExecutePreprocessor( timeout=timeout )
    ep.preprocess( nb, {'metadata': {'path': os.getcwd() }} )

    # Save executed notebook
    executed_filename = 'executed_' + os.path.basename( script_fp )
    executed_fp = os.path.join( output_dir,  executed_filename )
    with open( executed_fp, 'w', encoding='utf-8' ) as f:
        nbformat.write( nb, f )

    return nb

def run_jug( script_fp, config_fp, output_dir, script_id, n_procs ):
    '''Code for running a python program.

    Args:
        script_fp (str):
            Python script to run.

        config_fp (str):
            Config filepath, passed as a commandline arg to the script.

        output_dir (str):
            Where to store any products from running the script.
            Not currently used, but included for compatibility with other
            run functions.

    Returns:
        subprocess.SubProcess:
            Subprocess output.
    '''

    # Setup args
    jug_dir = os.path.join(
        output_dir,
        os.path.basename( script_id ) + '.jugdir',
    )
    sp_args = [
        'jug',
        'execute',
        script_fp,
        config_fp,
        '--jugdir=' + jug_dir,
    ]

    # Run parallel
    for i in range( n_procs-1 ):
        sp = subprocess.Popen( sp_args )
    # Finish with one we wait for
    sp = subprocess.run( sp_args )

    return sp

########################################################################

if __name__ == '__main__':

    # Parse args
    parser = argparse.ArgumentParser(
        description='Run your trove pipeline.'
    )
    parser.add_argument(
        'config_fp',
        type = str,
        help = 'Location of your config file used to guide cleaning.',
    )
    parser.add_argument(
        '-n',
        '--n_processors',
        type = int,
        help = 'Number of processors to use when performing multiprocessing.',
        default = 4,
    )
    parser.add_argument(
        '-max_loops',
        type = int,
        help = 'Maximum number of times to run scripts.',
        default = 1000,
    )
    parser.add_argument(
        '--cell_timeout',
        type = float,
        help = 'Allowed execution time per cell in seconds.',
        default = 1200,
    )
    args = parser.parse_args()

    # Run
    run(
        args.config_fp,
        args.n_processors,
        args.max_loops,
        args.cell_timeout,
    )

