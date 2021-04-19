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
        trove_build.link_params_to_config(
            a = 2,
            dog = False,
            cat = 'not best',
        )

        # Test
        assert a == 1
        assert dog
        assert cat == 'best'
