import os
import pathlib
import shutil
import unittest
import trove.config_parser as config_parser

########################################################################

class TestConfigParser( unittest.TestCase ):

    def test_get_next_variation_args( self ):

        tcp = config_parser.ConfigParser(
            './tests/examples/standard/standard.trove'
        )

        actual = tcp.get_next_variation_args()

        assert actual == ( 'py.1', 'identifier_A', '' )

    ########################################################################

    def test_get_next_variation_midway( self ):

        tcp = config_parser.ConfigParser(
            './tests/examples/midway/midway.trove'
        )

        actual = tcp.get_next_variation_args()

        assert actual == (
            'py.1',
            'this_is_also_an_identifier',
            ''
        )

########################################################################

class TestGlobalVariation( unittest.TestCase ):

    def setUp( self ):
        
        self.flag_file = './tests/data/examples/global_variations/more_variations/low_n/identifier_A/py.1.troveflag'
        self.data_dir = os.path.dirname( self.flag_file )
        if os.path.isfile( self.flag_file ):
            os.remove( self.flag_file )
        if not os.path.isdir( self.data_dir ):
            os.makedirs( self.data_dir, exist_ok=True )

    ########################################################################

    def tearDown( self ):

        if os.path.isdir( self.data_dir ):
            shutil.rmtree( './tests/data/examples/global_variations/more_variations' )

    ########################################################################

    def test_get_next_variation( self ):

        tcp = config_parser.ConfigParser(
            './tests/examples/global_variations/global_variations.trove'
        )
        variation_args = tcp.get_next_variation_args()
        assert variation_args == ( 'py.1', 'identifier_A', 'low_n' )

    ########################################################################

    def test_get_next_variation_subsequent( self ):

        pathlib.Path( self.flag_file ).touch()

        tcp = config_parser.ConfigParser(
            './tests/examples/global_variations/global_variations.trove'
        )

        variation_args = tcp.get_next_variation_args()
        assert variation_args == ( 'py.2', 'identifier_A', 'low_n' )