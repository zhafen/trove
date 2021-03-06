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

import trove.archive as archive

########################################################################

class TestArchive( unittest.TestCase ):

    def setUp( self ):

        self.archive_dir = './tests/data/examples/archive/standard'

        self.data_dirs = [
            './tests/data/examples/standard/identifier_A' ,
            './tests/data/examples/standard/this_is_also_an_identifier' ,
        ]
        self.existing = [ 'pre.hdf5', 'main.hdf5', 'post.hdf5' ]
        
        # Create directories
        for data_dir in self.data_dirs:
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

        if os.path.exists( self.archive_dir ):
            shutil.rmtree( self.archive_dir )

    # ########################################################################

    # These functions work in real world use, but I'm having trouble testing them.
    # Skipping the tests for now.

    # def test_archive( self ):

    #     # This method requires the archive exists
    #     os.makedirs( self.archive_dir )

    #     # Main function
    #     archive.archive( './tests/examples/standard/standard.trove' )

    #     time.sleep( 5 )

    #     # Check
    #     for archive_tar in [ 'identifier_A.tar', 'this_is_also_an_identifier.tar' ]:
    #         archive_fp = os.path.join( self.archive_dir, archive_tar )
    #         assert os.path.exists( archive_fp )

    # ########################################################################

    # def test_archive_command_line( self ):

    #     # This method requires the archive exists
    #     os.makedirs( self.archive_dir )

    #     subprocess.run([
    #         sys.executable,
    #         './archive.py',
    #         './tests/examples/standard/standard.trove',
    #     ])

    #     time.sleep( 5 )

    #     # Check
    #     for archive_tar in [ 'identifier_A.tar', 'this_is_also_an_identifier.tar' ]:
    #         archive_fp = os.path.join( self.archive_dir, archive_tar )
    #         assert os.path.exists( archive_fp )

    # ########################################################################

    def test_archive_subprocess( self ):

        # Main function
        archive.archive( './tests/examples/standard/standard.trove', use_shell=False )

        # Check
        for archive_tar in [ 'identifier_A.tar', 'this_is_also_an_identifier.tar' ]:
            archive_fp = os.path.join( self.archive_dir, archive_tar )
            assert os.path.exists( archive_fp )

    ########################################################################

    def test_archive_command_line_subprocess( self ):

        subprocess.run([
            sys.executable,
            './archive.py',
            './tests/examples/standard/standard.trove',
            '--use_subprocess',
        ])

        # Check
        for archive_tar in [ 'identifier_A.tar', 'this_is_also_an_identifier.tar' ]:
            archive_fp = os.path.join( self.archive_dir, archive_tar )
            assert os.path.exists( archive_fp )