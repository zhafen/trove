'''Tools for building the pipeline.'''

import ast
import trove.config_parser as config_parser

########################################################################

def link_params_to_config(
        config_fp,
        split_existing_and_new = False,
        **pm
    ):
    '''Link the values of a set of existing params to those in a config,
    overwriting the existing values if the config has that value.

    Args:
        config_fp (str):
            Location of the config file to use for updating the parameters.

        split_existing_and_new (bool):
            If True return two dictionaries, one for parameters that already    
            existed and may have been updated, and one for new parameters
            that were added.

    Kwargs:
        All parameters to update.

    Returns:
        pm (dict), [pm_new (dict)]
            Dictionaries containing new/updated parameters.
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

    # Update loop
    pm_new = {}
    for key in options:

        # Get value from config
        value_str = tcp.get( variation, key, fallback=None )
        if value_str is not None:
            # We'll try to evaluate the argument, but fallback to the str rep
            try:
                value = ast.literal_eval( value_str )
            except ( SyntaxError, ValueError ) as e:
                value = value_str

        # Assign
        if not split_existing_and_new:
            pm[key] = value

        else:
            if key in pm:
                pm[key] = value
            else:
                pm_new[key] = value

    # Return
    if split_existing_and_new:
        pm_new['data_dir'] = tcp.get_next_data_dir()
        pm_new['variation'] = variation
        return pm, pm_new
    pm['data_dir'] = tcp.get_next_data_dir()
    pm['variation'] = variation
    return pm
