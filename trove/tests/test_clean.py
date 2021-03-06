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

        self.config_fp = './tests/examples/standard/standard.trove'

        self.data_dirs = [
            './tests/data/examples/standard/identifier_A' ,
            './tests/data/examples/standard/this_is_also_an_identifier' ,
        ]
        self.troveflags = [ 'py.1.troveflag', 'py.2.troveflag' ]
        self.data_products = [ 'pre.hdf5', 'main.hdf5', ]
        
        # Create directories
        for data_dir in self.data_dirs:
            os.makedirs( data_dir, exist_ok=True )
            for troveflag in self.troveflags:
                flag_fp = os.path.join( data_dir, troveflag )
                pathlib.Path( flag_fp ).touch()
            for data_product in self.data_products:
                data_fp = os.path.join( data_dir, data_product )
                pathlib.Path( data_fp ).touch()

    ########################################################################

    def tearDown( self ):

        # Full clean
        for data_dir in self.data_dirs:
            if os.path.exists( data_dir ):
                shutil.rmtree( data_dir )

    ########################################################################

    def test_clean( self ):

        # Main function
        clean.clean( self.config_fp )

        # Check
        for data_dir in self.data_dirs:
            for troveflag in self.troveflags:
                flag_fp = os.path.join( data_dir, troveflag )
                assert not os.path.exists( flag_fp )

            for data_product in self.data_products:
                data_fp = os.path.join( data_dir, data_product )
                assert os.path.exists( data_fp )

    ########################################################################

    def test_clean_jugdata( self ):

        # Create jugdata mockups
        for data_dir in self.data_dirs[:-1]:
            jugdata_fp = os.path.join( data_dir, 'test.jugdata' )
            os.makedirs( jugdata_fp, exist_ok=True )

        # Main function
        clean.clean(
            self.config_fp,
            clean_jug = True,
        )

        # Check
        for data_dir in self.data_dirs:
            jugdata_fp = os.path.join( data_dir, 'test.jugdata' )
            assert not os.path.exists( jugdata_fp )

    ########################################################################

    def test_clean_jugdata_commandline( self ):

        # Create jugdata mockups
        for data_dir in self.data_dirs[:-1]:
            jugdata_fp = os.path.join( data_dir, 'test.jugdata' )
            os.makedirs( jugdata_fp, exist_ok=True )

        subprocess.run([
            sys.executable,
            './clean.py',
            self.config_fp,
        ])

        # Check
        for data_dir in self.data_dirs:
            jugdata_fp = os.path.join( data_dir, 'test.jugdata' )
            assert not os.path.exists( jugdata_fp )

    ########################################################################

    def test_clean_data_products( self ):

        # Create mockups
        for data_dir in self.data_dirs[:-1]:
            fp = os.path.join( data_dir, 'pre.hdf5' )
            pathlib.Path( fp ).touch()

        # Main function
        clean.clean(
            self.config_fp,
            clean_data_products = True,
        )

        # Check
        for data_dir in self.data_dirs:
            for data_product in self.data_products:
                fp = os.path.join( data_dir, data_product )
                assert not os.path.exists( fp )

    ########################################################################

    def test_clean_data_products_command_line( self ):

        # Create mockups
        for data_dir in self.data_dirs[:-1]:
            fp = os.path.join( data_dir, 'pre.hdf5' )
            pathlib.Path( fp ).touch()

        # Main function
        subprocess.run([
            sys.executable,
            './clean.py',
            self.config_fp,
            '--clean_data'
        ])

        # Check
        for data_dir in self.data_dirs:
            for data_product in self.data_products:
                fp = os.path.join( data_dir, data_product )
                assert not os.path.exists( fp )


    ########################################################################

    def test_full_clean( self ):

        # Main function
        clean.clean(
            self.config_fp,
            full_clean = True
        )

        # Check
        for data_dir in self.data_dirs:
            assert not os.path.exists( data_dir )

    ########################################################################

    def test_full_clean_commandline( self ):

        subprocess.run([
            sys.executable,
            './clean.py',
            self.config_fp,
            '--full_clean'
        ])

        # Check
        for data_dir in self.data_dirs:
            assert not os.path.exists( data_dir )

    ########################################################################

    def test_full_clean_commandline_bin( self ):

        subprocess.run([
            sys.executable,
            './bin/trove',
            'clean',
            self.config_fp,
            '--full_clean'
        ])

        # Check
        for data_dir in self.data_dirs:
            assert not os.path.exists( data_dir )

########################################################################

class TestCleanControlledExecution( TestClean ):

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
        self.data_products = [ 'main.hdf5', ]
        
        # Create directories
        for data_dir in self.data_dirs:
            os.makedirs( data_dir, exist_ok=True )
            for troveflag in self.troveflags:
                flag_fp = os.path.join( data_dir, troveflag )
                pathlib.Path( flag_fp ).touch()
            for data_product in self.data_products:
                data_fp = os.path.join( data_dir, data_product )
                pathlib.Path( data_fp ).touch()
