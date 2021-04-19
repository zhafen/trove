'''Tools for building the pipeline.'''

import ast
import configparser

########################################################################

def link_params_to_config(
        config_fp,
        **pm
    ):
    '''Link the values of a set of existing params to those in a config,
    overwriting the existing values if the config has that value.
    '''

    # Read the config
    cp = configparser.ConfigParser()
    cp.read( config_fp )

    # Update loop
    for key, item in pm.items():

        # Loop through config sections
        for ckey, citem in cp.items():

            # Update value
            if key in citem:
                pm[key] = ast.literal_eval( citem[key] )

    return pm
