'''Testing for building the pipeline
'''

import unittest
import trove
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

    def test_link_params_split( self ):

        # Update parameters
        pm, new_pm = trove_build.link_params_to_config(
            config_fp = './tests/examples/basic.trove',
            split_existing_and_new = True,
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
        assert 'data_dir' in new_pm
        assert 'data_dir' not in pm
        assert 'bird' in new_pm
        assert 'bird' not in pm

    ########################################################################

    def test_link_params_init( self ):

        # Update parameters
        pm = trove.link_params_to_config(
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

    def test_link_params_specify_variation( self ):

        # Update
        pm = trove_build.link_params_to_config(
            config_fp = './tests/examples/standard/standard.trove',
            variation = 'this_is_also_an_identifier',
            n = 100,
            high = 10,
            power = 0,
        )

        # Check
        assert pm['n'] == 1000
        assert pm['high'] == 1000
        assert pm['power'] == 3

        assert pm['data_dir'] == './tests/data/examples/standard/this_is_also_an_identifier'

    ########################################################################

    def test_link_params_global_variation( self ):

        # Update
        pm = trove_build.link_params_to_config(
            config_fp = './tests/examples/global_variations/global_variations.trove',
            n = 100,
            high = 10,
            power = 0,
        )

        # Check
        assert pm['n'] == 10
        assert pm['high'] == 1000
        assert pm['power'] == 1

        assert pm['data_dir'] == './tests/data/examples/global_variations/more_variations/low_n/identifier_A'