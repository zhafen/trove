'''Testing for evaluating pipeline progress.
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

import trove.evaluate as evaluate

########################################################################

class TestEvaluate( unittest.TestCase ):

    def setUp( self ):

        self.config_fp = './tests/examples/standard/standard.trove'

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

    def test_evaluate( self ):

        # Main function
        evaluate.evaluate( self.config_fp )

        # Check
        for data_dir in self.data_dirs[:-1]:
            for troveflag in self.troveflags:
                flag_fp = os.path.join( data_dir, troveflag )
                assert os.path.exists( flag_fp )

    ########################################################################

    def test_evaluate_glob( self ):

        # Create the test for the glob
        pathlib.Path(
            os.path.join( self.data_dirs[0], 'post_abc.hdf5' )
        ).touch()

        # Main function
        evaluate.evaluate( self.config_fp )

        # Check
        for data_dir in self.data_dirs[:-1]:
            for troveflag in self.troveflags:
                flag_fp = os.path.join( data_dir, troveflag )
                assert os.path.exists( flag_fp )

########################################################################

class TestEvaluateControlledExecution( TestEvaluate ):

    def setUp( self ):

        self.config_fp = './tests/examples/controlled_execution/controlled_execution.trove'

        self.data_dirs = [
            # './tests/data/examples/controlled_execution/identifier_A' ,
            './tests/data/examples/controlled_execution/this_is_also_an_identifier' ,
            # './tests/data/examples/controlled_execution/more_variations/n_low/identifier_A' ,
            # './tests/data/examples/controlled_execution/more_variations/n_low/this_is_also_an_identifier' ,
            # './tests/data/examples/controlled_execution/more_variations/n_less_low/identifier_A' ,
            './tests/data/examples/controlled_execution/more_variations/n_less_low/this_is_also_an_identifier' ,
        ]
        self.troveflags = [ 'py.2.troveflag' ]
        self.existing = [ 'main.hdf5', ]
        
        # Create directories
        for data_dir in self.data_dirs[:-1]:
            os.makedirs( data_dir, exist_ok=True )
            for existing in self.existing:
                fp = os.path.join( data_dir, existing )
                pathlib.Path( fp ).touch()