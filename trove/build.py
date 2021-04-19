'''Tools for building the pipeline.'''

import ast
import configparser
import copy

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
    tcp = TroveConfigParser( config_fp )

    # Update loop
    for key, item in pm.items():

        # Loop through config sections
        for ckey, citem in tcp.items():

            # Update value
            if key in citem:
                pm[key] = ast.literal_eval( citem[key] )

    return pm

########################################################################

class ConfigParser( configparser.ConfigParser ):

    def __init__(
        self,
        fp = None,
        empty_lines_in_values = False,
            *args,
            **kwargs
    ):
        '''Same init as configparser.ConfigParser, but includes the read step.

        Args:
            fp (str):
                Filepath to config file.

            empty_lines_in_values (bool):
                Whether or not empty lines following a value should be
                included as part of that value.

        Returns:
            TroveConfigParser
        '''

        super().__init__(
            empty_lines_in_values = empty_lines_in_values,
            *args,
            **kwargs
        )

        if fp is not None:
            self.read( fp )
    
    ########################################################################

    def read( self, *args, **kwargs ):
        '''Read a file, with extra processing for the trove format.

        Args:
            Passed to configparser.ConfigParser.

        Kwargs:
            Passed to configparser.ConfigParser.
        '''

        # Default
        super().read( *args, **kwargs )

        # Parse for variations on the parameters
        self.variations = {}
        for key, item in copy.deepcopy( self.items() ):

            # Identify variations
            if key[:3] == 'ID ':
                self.variations[key[3:]] = item
                self.remove_section( key )

    ########################################################################

