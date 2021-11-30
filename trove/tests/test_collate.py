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

import trove.collate as collate

########################################################################

class TestCollate( unittest.TestCase ):

    def setUp( self ):

        self.config_fp = './tests/examples/collate/collate.trove'

        self.destination_dir = './tests/data/temp_collated'
        if os.path.exists( self.destination_dir ):
            shutil.rmtree( self.destination_dir )

    ########################################################################

    def tearDown( self ):

        if os.path.exists( self.destination_dir ):
            shutil.rmtree( self.destination_dir )

    ########################################################################

    def check( self ):

        files = [
            'plot_combined.png',
            'plot_combined.low_n.png',
            'plot_identifier_A.png',
            'plot_identifier_A.low_n.png',
            'plot_identifier_A.low_n_alternative_seed.png',
            'plot_this_is_also_an_identifier.png',
            'plot_this_is_also_an_identifier.low_n.png',
            'unique_plot.low_n_alternative_seed.png',
        ]
        for f in files:
            fp = os.path.join( self.destination_dir, f ) 
            assert os.path.isfile( fp )

    ########################################################################

    def test_collate( self ):

        # Main function
        collate.collate( self.config_fp, 'figure_dir', self.destination_dir )

        self.check()

    ########################################################################

    def test_collate_commandline( self ):

        subprocess.run([
            sys.executable,
            './collate.py',
            self.config_fp,
            'figure_dir',
            self.destination_dir,
        ])

        self.check()

    ########################################################################

    def test_collate_commandline_bin( self ):

        subprocess.run([
            sys.executable,
            './bin/trove',
            'clean',
            self.config_fp,
            'figure_dir',
            self.destination_dir,
        ])

        self.check()