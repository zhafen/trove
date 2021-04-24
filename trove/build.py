'''Tools for building the pipeline.'''

import ast
import trove.config_parser as config_parser

########################################################################

def link_params_to_config(
        config_fp,
        **pm
    ):
    '''Link the values of a set of existing params to those in a config,
    overwriting the existing values if the config has that value.

    Args:
        config_fp (str):
            Location of the config file to use for updating the parameters.

    Kwargs:
        All parameters to update.
    '''

    # Read the config
    tcp = config_parser.ConfigParser( config_fp )

    # Identify which variation is next
    variation_args = tcp.get_next_variation()
    variation = variation_args[0]
    # Account for different formatting
    if variation == 'DEFAULT':
        options = tcp.defaults()
    else:
        options = tcp.options( variation )
    pm['data_dir'] = tcp.get_next_data_dir()

    # Update loop
    for key in options:

        # Loop through config sections
        value_str = tcp.get( variation, key, fallback=None )
        if value_str is not None:
            # We'll try to evaluate the argument, but fallback to the str rep
            try:
                pm[key] = ast.literal_eval( value_str )
            except SyntaxError:
                pm[key] = value_str

    return pm
