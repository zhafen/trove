'''Tools for building the pipeline.'''
import ast
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
        global_ids = list( self.global_variations )
        self.scripts = [
            _ for _ in self['SCRIPTS'].keys()
            if _ not in self.defaults()
        ]
        self.manager = management.Manager( file_format, global_ids, ids, self.scripts )
        self.manager.get_file = self.get_flag_file
    
    ########################################################################

    def options(self, section, exclude_defaults=False ):
        """Return a list of option names for the given section name."""
        try:
            opts = self._sections[section].copy()
        except KeyError:
            raise configparser.NoSectionError(section) from None
        if not exclude_defaults:
            opts.update(self._defaults)
        return list(opts.keys())

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

    def get_next_variation_args(
        self,
        script_id = None,
        variation = None,
        global_variation = None,
        when_done = 'done_flag'
    ):

        variation_args = self.manager.get_next_args_to_use(
            when_done = when_done,
        )

        if variation_args == 'done_flag':
            return variation_args

        if script_id is None:
            script_id = variation_args[2]
        if variation is None:
            variation = variation_args[1]
        if global_variation is None:
            global_variation = variation_args[0]

        return script_id, variation, global_variation

    ########################################################################

    def get_global_variation_dir( self, global_variation ):

        if global_variation != '':
            return os.path.join( self.global_variations_dirname, global_variation )
        else:
            return global_variation

    ########################################################################

    def get_data_dir( self, variation, global_variation, script_id ):
        '''Get the next data dir, and create it if it doesn't exist.
        '''

        # Get the dir
        flag_file = self.get_flag_file( global_variation, variation, script_id )
        next_dir = os.path.dirname( flag_file )

        # Make sure it exists
        if not os.path.exists( next_dir ):
            print(
                'No data directory at {}\n'.format( next_dir ) + \
                'Creating one.'
            )
            os.makedirs( next_dir, exist_ok=True )

        return next_dir

    ########################################################################

    def get_flag_file( self, global_variation, variation, script_id ):

        # Get the global variation used for the data dir.
        if self.has_option( global_variation, 'use_variation_data_dir' ):
            use_variation_data_dir = self.get( global_variation, 'use_variation_data_dir' )
            use_variation_data_dir = ast.literal_eval( use_variation_data_dir )
            if script_id in use_variation_data_dir:
                global_variation = ''
        global_variation_dir = self.get_global_variation_dir( global_variation )

        flag_file = self.manager.file_format.format(
            global_variation_dir,
            variation,
            script_id
        )

        # Account for empty dirs
        flag_file =  os.path.join( *flag_file.split( '/' ) )

        return flag_file

    ########################################################################

    @property
    def data_dirs( self ):

        if not hasattr( self, '_data_dirs' ):
            self._data_dirs = [
                os.path.dirname( _ ) for _ in self.manager.data_files
             ]

        return self._data_dirs

    ########################################################################

    @property
    def unique_data_dirs( self ):

        if not hasattr( self, '_unique_data_dirs' ):
            self._unique_data_dirs = np.unique( self.data_dirs )

        return self._unique_data_dirs