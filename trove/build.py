'''Tools for building the pipeline.'''

import ast
import copy
import os
import trove.config_parser as config_parser

########################################################################

def link_params_to_config(
        config_fp,
        variation = None,
        global_variation = None,
        **pm
    ):
    '''Link the values of a set of existing params to those in a config,
    overwriting the existing values if the config has that value.

    Args:
        config_fp (str):
            Location of the config file to use for updating the parameters.

        variation (str):
            Specific variation to select from the config.
            If None, defaults to the next in the trove.

    Kwargs:
        All parameters to update.

    Returns:
        pm (dict), [pm_new (dict)]
            Dictionaries containing new/updated parameters.
    '''

    # Read the config
    tcp = config_parser.ConfigParser( config_fp )

    # Identify which variation is next
    if variation is None:
        variation_args = tcp.get_next_variation()
        variation = variation_args[0]

    if global_variation is None:
        global_variation = tcp.get_next_global_variation()
        if global_variation != '':
            global_variation_dir = os.path.join( tcp.global_variations_dirname, global_variation )
        else:
            global_variation_dir = ''

    # Defaults
    pm_new = copy.deepcopy( tcp._defaults )

    # Global variation options
    if global_variation != '':
        pm_new.update( tcp._sections[global_variation] )

    # Variation options
    if variation != 'DEFAULT':
        pm_new.update( tcp._sections[variation] )

    # Interpret strings
    for key, item in pm_new.items():
        if item is not None:
            # We'll try to evaluate the argument, but fallback to the str rep
            try:
                pm_new[key] = ast.literal_eval( item )
            except ( SyntaxError, ValueError ) as e:
                pass

    # Store data dir and variation name
    pm_new['variation'] = variation
    pm_new['data_dir'] = os.path.dirname(
        tcp.manager.get_file( global_variation_dir, variation, 'FOO' )
    )

    # Update and return
    pm.update( pm_new )
    return pm
