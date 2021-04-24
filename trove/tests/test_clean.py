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

import trove.clean as clean

########################################################################

class TestClean( unittest.TestCase ):

    def setUp( self ):

        self.data_dirs = [
            './tests/data/examples/standard/identifier_A' ,
            './tests/data/examples/standard/this_is_also_an_identifier' ,
        ]
        self.troveflags = [ 'py.1.troveflag', 'py.2.troveflag' ]
        
        # Create directories
        for data_dir in self.data_dirs:
            os.makedirs( data_dir, exist_ok=True )
            for troveflag in self.troveflags:
                flag_fp = os.path.join( data_dir, troveflag )
                pathlib.Path( flag_fp ).touch()

    ########################################################################

    def tearDown( self ):

        # Full clean
        for data_dir in self.data_dirs:
            if os.path.exists( data_dir ):
                shutil.rmtree( data_dir )

    ########################################################################

    def test_clean( self ):

        # Main function
        clean.clean( './tests/examples/standard/standard.trove' )

        # Check
        for data_dir in self.data_dirs:
            for troveflag in self.troveflags:
                flag_fp = os.path.join( data_dir, troveflag )
                assert not os.path.exists( flag_fp )

    ########################################################################

    def test_clean_jugdir( self ):

        # Create jugdir mockups
        for data_dir in self.data_dirs[:-1]:
            jugdir_fp = os.path.join( data_dir, 'test.jugdir' )
            os.makedirs( jugdir_fp, exist_ok=True )

        # Main function
        clean.clean(
            './tests/examples/standard/standard.trove',
            clean_jug = True,
        )

        # Check
        for data_dir in self.data_dirs:
            jugdir_fp = os.path.join( data_dir, 'test.jugdir' )
            assert not os.path.exists( jugdir_fp )

    ########################################################################

    def test_full_clean( self ):

        # Main function
        clean.clean(
            './tests/examples/standard/standard.trove',
            full_clean = True
        )

        # Check
        for data_dir in self.data_dirs:
            assert not os.path.exists( data_dir )
