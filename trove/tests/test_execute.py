'''Testing for running the full pipeline and executables.
'''

import h5py
import numpy as np
import numpy.testing as npt
import os
import shutil
import subprocess
import sys
import time
import unittest

import trove.execute as execute

########################################################################

class TestExecutable( unittest.TestCase ):

    def tearDown( self ):

        data_dirs = [
            './tests/data/examples/standard/identifier_A' ,
            './tests/data/examples/standard/this_is_also_an_identifier' ,
            './tests/data/examples/midway/this_is_also_an_identifier' ,
            './tests/figures',
        ]
        for data_dir in data_dirs:
            if os.path.exists( data_dir ):
                shutil.rmtree( data_dir )

    def check( self ):

        # Check
        pre_fp = './tests/data/examples/standard/this_is_also_an_identifier/pre.hdf5'
        pre = h5py.File( pre_fp, 'r' )
        main_fp = './tests/data/examples/standard/this_is_also_an_identifier/main.hdf5'
        main = h5py.File( main_fp, 'r' )
        assert main['raised_numbers'][...].size == 1000
        power = (
            np.log10( main['raised_numbers'][...] ) / 
            np.log10( pre['numbers'][...] )
        )
        npt.assert_allclose( power, np.full( 1000, 3. ) )

        # Check more
        for ident in [ 'identifier_A', 'this_is_also_an_identifier' ]:
            for script in [ 'py.1', 'py.2' ]:

                ofp = './tests/data/examples/standard/{}/{}.troveflag'.format(
                    ident,
                    script,
                )
                assert os.path.exists( ofp )

        # Check figures
        for ident in [ 'identifier_A', 'this_is_also_an_identifier' ]:
            ffp = './tests/figures/last_digits_{}.pdf'.format( ident )
            assert os.path.exists( ffp )

    ########################################################################

    def test_executable_fn( self ):

        execute.run( './tests/examples/standard/standard.trove' )

        self.check()

    ########################################################################

    def test_executable( self ):

        subprocess.run([
            sys.executable,
            './execute.py',
            './tests/examples/standard/standard.trove',
        ])

        self.check()

    ########################################################################

    def test_executable_bin( self ):

        subprocess.run([
            sys.executable,
            './bin/trove',
            'execute',
            './tests/examples/standard/standard.trove',
        ])

        self.check()
 
    ########################################################################

    def test_executable_midway( self ):

        subprocess.run([
            sys.executable,
            './execute.py',
            './tests/examples/midway/midway.trove',
        ])

        # Check
        fp = './tests/data/examples/midway/this_is_also_an_identifier/main.hdf5'
        f = h5py.File( fp, 'r' )
        assert f['raised_numbers'][...].size == 1000

        # Check more
        for ident in [ 'identifier_A', 'this_is_also_an_identifier' ]:
            for script in [ 'py.1', 'py.2' ]:

                ofp = './tests/data/examples/midway/{}/{}.troveflag'.format(
                    ident,
                    script,
                )
                assert os.path.exists( ofp )

########################################################################

class TestExecutableJug( unittest.TestCase ):

    def tearDown( self ):

        data_dirs = [
            './tests/data/examples/jug' ,
        ]
        for data_dir in data_dirs:
            if os.path.exists( data_dir ):
                shutil.rmtree( data_dir )

    ########################################################################

    def test_executable( self ):

        start_time = time.time()

        execute.run( './tests/examples/jug/jug.trove' )

        time_taken = time.time() - start_time

        assert time_taken < 5, "Parallelization is not functioning."

        # Check
        main_fp = './tests/data/examples/jug/less_low/primes.hdf5'
        main = h5py.File( main_fp, 'r' )
        assert main['primes'][...].size == 100

        # Check more
        for ident in [ 'low', 'less_low' ]:
            for script in [ 'py.1', 'jug.2' ]:
                ofp = './tests/data/examples/jug/{}/{}.troveflag'.format(
                    ident,
                    script,
                )
                assert os.path.exists( ofp )

########################################################################

class TestScript( unittest.TestCase ):

    def tearDown( self ):

        data_dir = './tests/data/examples/standard/identifier_A' 
        if os.path.exists( data_dir ):
            shutil.rmtree( data_dir )

    ########################################################################

    def test_script( self ):

        sp = subprocess.run(
            [
                sys.executable,
                './tests/examples/standard/pre.py',
                './tests/examples/standard/standard.trove',
            ],
            capture_output = True,
        )
        print( 'STDOUT:\n' + sp.stdout.decode( 'utf-8' ) )
        print( 'STDERR:\n' + sp.stderr.decode( 'utf-8' ) )

        fp = './tests/data/examples/standard/identifier_A/pre.hdf5'
        f = h5py.File( fp, 'r' )
        assert f['numbers'][...].size == 1000


