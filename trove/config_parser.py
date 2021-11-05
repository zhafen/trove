'''Tools for building the pipeline.'''
import configparser
import copy
import os
import numpy as np
import warnings

import augment

import trove.management as management

########################################################################

class ConfigParser( configparser.ConfigParser ):

    @augment.store_parameters
    def __init__(
        self,
        fp = None,
        empty_lines_in_values = False,
        interpolation = configparser.ExtendedInterpolation(),
        global_variations_dirname = 'more_variations',
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

        # Super
        super().__init__(
            empty_lines_in_values = empty_lines_in_values,
            interpolation = interpolation,
            *args,
            **kwargs
        )

        # Read
        if fp is not None:
            self.read( fp )

        # Required parameter
        assert self.has_option( 'DEFAULT', 'root_data_dir' ), '"root_data_dir" parameter required.'

        # Dangerous parameter to use
        if self.has_option( 'DEFAULT', 'global' ):
            warnings.warn(
                'Found a parameter named "global" in the DEFAULT parameters.'
                'global is the name of a specal parameter that indicates if there are global variations.'
                'Please consider using a different parameter.'
            )

        # Setup the file format for a trove manager
        file_format = []
        file_format.append( self.get( 'DEFAULT', 'root_data_dir' ) )
        # First for global variations, second for variations, third for scripts
        file_format += [ '{}', '{}', '{}.troveflag' ]
        file_format = os.path.join( *file_format )

        # Setup a trove manager
        ids = list( self.variations )
        global_ids = [ self.format_global_variation( _ ) for _ in self.global_variations ]
        scripts = [
            _ for _ in self['SCRIPTS'].keys()
            if _ not in self.defaults()
        ]
        self.manager = management.Manager( file_format, global_ids, ids, scripts )
    
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
        self.special_sections = [ 'DEFAULT', 'SCRIPTS', 'DATA PRODUCTS' ]
        self.variations = []
        self.global_variations = [ '', ]
        for key in copy.deepcopy( self.keys() ):
            if key in self.special_sections:
                continue
            # Retrieve global variations
            if self.has_option( key, 'global' ):
                if self.get( key, 'global' ):
                    self.global_variations.append( key )
                    continue
            self.variations.append( key )

        # When no variations, just use the defaults
        if len( self.variations ) == 0:
            self.variations = [ 'DEFAULT', ]

        # Check that the config file is formatted correctly
        if len( self.sections() ) == 0:
            raise OSError(
                'Config at {} does not contain '.format( self.fp ) + \
                'any sections.\nPlease check the file/file location.'
            )
        self.required_sections = [ 'DEFAULT', 'SCRIPTS' ]
        for key in self.required_sections:
            if key not in self.sections():

                # Special rules for the default section
                if key == 'DEFAULT' and len( self.defaults() ) != 0:
                    continue

                raise NameError(
                    'Config at {} does not contain '.format( self.fp ) + \
                    'required section {}.\n'.format( key )
                )

    ########################################################################

    def get_next_variation( self, when_done='done_flag', *args, **kwargs ):

        variation = self.manager.get_next_args_to_use(
            when_done = when_done,
            *args,
            **kwargs
        )

        if variation == 'done_flag':
            return variation

        return variation[1:]

    def get_next_global_variation( self, when_done='done_flag', *args, **kwargs ):

        global_variation = self.manager.get_next_args_to_use(
            when_done = when_done,
            *args,
            **kwargs
        )

        if global_variation == 'done_flag':
            return global_variation

        return os.path.split( global_variation[0] )[-1]

    def format_global_variation( self, global_variation ):

        if global_variation != '':
            return os.path.join( self.global_variations_dirname, global_variation )
        else:
            return global_variation

    @property
    def data_dirs( self ):

        if not hasattr( self, '_data_dirs' ):
            self._data_dirs = [
                os.path.dirname( _ ) for _ in self.manager.data_files
             ]

        return self._data_dirs

    @property
    def unique_data_dirs( self ):

        if not hasattr( self, '_unique_data_dirs' ):
            self._unique_data_dirs = np.unique( self.data_dirs )

        return self._unique_data_dirs

    def get_next_data_dir( self, variation=None, global_variation=None ):
        '''Get the next data dir, and create it if it doesn't exist.
        '''

        if variation is None:
            variation = self.get_next_variation()

        if global_variation is None:
            global_variation = self.get_next_global_variation()
        global_id = self.format_global_variation( global_variation )

        next_dir = os.path.dirname(
            self.manager.get_file( global_id, variation, 'FOO' )
        )

        if not os.path.exists( next_dir ):
            print(
                'No data directory at {}\n'.format( next_dir ) + \
                'Creating one.'
            )
            os.makedirs( next_dir, exist_ok=True )

        return next_dir

    def get_flag_file( self, *args ):

        return self.manager.get_file( *args )
