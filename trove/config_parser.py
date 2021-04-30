'''Tools for building the pipeline.'''
import configparser
import copy
import os

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

        # Setup a trove manager
        file_format = []
        if self.has_option( 'DEFAULT', 'root_data_dir' ):
            file_format.append( self.get( 'DEFAULT', 'root_data_dir' ) )
        file_format += [ '{}', '{}.troveflag' ]
        file_format = os.path.join( *file_format )
        ids = list( self.variations )
        scripts = [
            _ for _ in self['SCRIPTS'].keys()
            if _ not in self.defaults()
        ]
        self.manager = management.Manager( file_format, ids, scripts )
    
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
        self.special_sections = [ 'DEFAULT', 'SCRIPTS', 'CONVERSION' ]
        self.variations = []
        for key in copy.deepcopy( self.keys() ):
            if key in self.special_sections:
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

        return self.manager.get_next_args_to_use(
            when_done = when_done,
            *args,
            **kwargs
        )

    def get_data_dir_for_variation( self, variation ):

        return os.path.dirname( self.manager.get_file( variation ) )

    @property
    def data_dirs( self ):

        if not hasattr( self, '_data_dirs' ):
            self._data_dirs = [
                os.path.dirname( _ ) for _ in self.manager.data_files
             ]

        return self._data_dirs

    def get_next_data_dir( self, *args, **kwargs ):
        '''Get the next data dir, and create it if it doesn't exist.
        '''

        next_dir = os.path.dirname(
            self.manager.get_incomplete_data_files()[0]
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
