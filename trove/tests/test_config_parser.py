import unittest
import trove.config_parser as config_parser

########################################################################

class TestConfigParser( unittest.TestCase ):

    def test_get_next_variation( self ):

        tcp = config_parser.ConfigParser(
            './tests/examples/standard/standard.trove'
        )

        actual = tcp.get_next_variation()

        assert actual == ( 'identifier_A', 'py.1' )

    ########################################################################

    def test_get_next_variation_midway( self ):

        tcp = config_parser.ConfigParser(
            './tests/examples/midway/midway.trove'
        )

        actual = tcp.get_next_variation()

        assert actual == (
            'this_is_also_an_identifier',
            'py.1'
        )
