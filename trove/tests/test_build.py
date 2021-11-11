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

    ########################################################################

    def test_link_params_specify_global_variation( self ):

        # Update
        pm = trove_build.link_params_to_config(
            config_fp = './tests/examples/global_variations/global_variations.trove',
            script_id = 'py.1',
            variation = 'identifier_A',
            global_variation = 'plotting_change',
            n = 100,
            high = 10,
            power = 0,
        )

        # Check
        assert pm['n'] == 1000
        assert pm['high'] == 1000
        assert pm['power'] == 1

        assert pm['script_id'] == 'py.1'
        assert pm['data_dir'] == './tests/data/examples/global_variations/identifier_A'
        assert pm['used_figure_dir'] == './tests/figures/more_variations/plotting_change'
