'''Testing for running the full pipeline
'''

import h5py
import numpy as np
import numpy.testing as npt
import subprocess
import time
import unittest

class TestComplete( unittest.TestCase ):

    def test_example( self ):

        # Run
        subprocess.run( [ './run.py', './tests/example/trove.config' ] )
        subprocess.run( [ './run.py', './tests/example/trove.config' ] )
        subprocess.run( [ './run.py', './tests/example/trove.config' ] )
        subprocess.run( [ './run.py', './tests/example/trove.config' ] )
        # time.sleep( 5 )

        # Check results
        fps = [
            './examples/data/power2/high10' ,
            './examples/data/power2/high100' ,
            './examples/data/power3/high10' ,
            './examples/data/power3/high100' ,
        ]
        for fp in fps:
            f = h5py.File( fp, 'r' )
            assert len( f['raised_numbers'][...].size ) == 1000

########################################################################

class TestExecutable( unittest.TestCase ):

    def test_executable( self ):

        subprocess.run([
            './tests/example/built_exec.sh',
            './tests/example/built.config',
        ])

        f = h5py.File( './tests/example/data/output_for_built.hdf5', 'r' )
        assert len( f['raised_numbers'][...].size ) == 1000

########################################################################

class TestScript( unittest.TestCase ):

    def test_script( self ):

        subprocess.run([
            'python',
            './tests/example/pre.py',
            './tests/example/built.config',
        ])

        f = h5py.File( './tests/example/data/preoutput_for_built.hdf5', 'r' )
        assert len( f['raised_numbers'][...].size ) == 1000
