'''Testing for building the pipeline
'''

import h5py
import numpy as np
import numpy.testing as npt
import subprocess
import time
import unittest
import trove.build as trove_build

########################################################################

class TestLinkParams( unittest.TestCase ):

    def test_link_params( self ):

        # Update parameters
        pm = trove_build.link_params_to_config(
            config_fp = './tests/examples/basic.trove',
            a = 2,
            dog = False,
            cat = 'not best',
            not_in_config = 'yeah',
            errors = 100,
            **{ 'bad dog': False, },
        )

        # Check
        assert pm['a'] == 1
        assert pm['dog']
        assert not pm['bad dog']
        assert pm['cat'] == 'the best'
        assert pm['not_in_config'] == 'yeah'
        assert pm['errors'] == None

    ########################################################################

    def test_link_params_queue( self ):

        # Update
        pm = trove_build.link_params_to_config(
            config_fp = './tests/examples/standard/standard.trove',
            n = 100,
            high = 10,
            power = 0,
        )

        # Check
        assert pm['n'] == 1000
        assert pm['high'] == 1000
        assert pm['power'] == 1

########################################################################

class TestConfigParser( unittest.TestCase ):

    def test_get_next_variation( self ):

        tcp = trove_build.ConfigParser(
            './tests/examples/standard/standard.trove'
        )

        actual = tcp.get_next_variation()

        assert actual == ( 'identifier_A', 's01' )

    ########################################################################

    def test_get_next_variation_midway( self ):

        tcp = trove_build.ConfigParser(
            './tests/examples/midway/midway.trove'
        )

        actual = tcp.get_next_variation()

        assert actual == (
            'identifier_A',
            's02'
        )
