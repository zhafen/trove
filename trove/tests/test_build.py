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

class TestUpdateParams( unittest.TestCase ):

    def test_update_params( self ):

        # Update parameters
        pm = trove_build.link_params_to_config(
            config_fp = './tests/examples/basic.trove',
            a = 2,
            dog = False,
            cat = 'not best',
            not_in_config = 'yeah',
            **{ 'bad dog': False, },
        )

        # Check
        assert pm['a'] == 1
        assert pm['dog']
        assert not pm['bad dog']
        assert pm['cat'] == 'the best'
        assert pm['not_in_config'] == 'yeah'