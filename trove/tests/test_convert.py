'''Testing for cleaning up the pipeline.
'''

import h5py
import numpy as np
import numpy.testing as npt
import os
import pathlib
import shutil
import subprocess
import sys
import time
import unittest

import trove.convert as convert

########################################################################

class TestConvert( unittest.TestCase ):

    def setUp( self ):

        self.data_dirs = [
            './tests/data/examples/standard/identifier_A' ,
            './tests/data/examples/standard/this_is_also_an_identifier' ,
        ]
        self.troveflags = [ 'py.1.troveflag', 'py.2.troveflag' ]
        self.existing = [ 'pre.hdf5', 'main.hdf5' ]
        
        # Create directories
        for data_dir in self.data_dirs[:-1]:
            os.makedirs( data_dir, exist_ok=True )
            for existing in self.existing:
                fp = os.path.join( data_dir, existing )
                pathlib.Path( fp ).touch()

    ########################################################################

    def tearDown( self ):

        # Full clean
        for data_dir in self.data_dirs:
            if os.path.exists( data_dir ):
                shutil.rmtree( data_dir )

    ########################################################################

    def test_convert( self ):

        # Main function
        convert.convert( './tests/examples/standard/standard.trove' )

        # Check
        for data_dir in self.data_dirs[:-1]:
            for troveflag in self.troveflags:
                flag_fp = os.path.join( data_dir, troveflag )
                assert os.path.exists( flag_fp )

    ########################################################################

    def test_convert_glob( self ):

        # Create the test for the glob
        pathlib.Path(
            './tests/data/examples/standard/identifier_A/post_abc.hdf5'
        ).touch()

        # Main function
        convert.convert( './tests/examples/standard/standard.trove' )

        # Check
        for data_dir in self.data_dirs[:-1]:
            for troveflag in self.troveflags:
                flag_fp = os.path.join( data_dir, troveflag )
                assert os.path.exists( flag_fp )
        assert os.path.exists(
            './tests/data/examples/standard/identifier_A/nb.3.troveflag'
        )
