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
            split_updated_from_new = True,
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

