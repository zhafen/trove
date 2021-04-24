import jug
import numpy as np
import h5py
import os
from time import sleep

def is_prime(n):

    # Sleep for 1 second, this runs too fast and is not a good demo
    sleep(0.25)
    for j in range(2, n - 1):
        if (n % j) == 0:
            return False
    return True

@jug.TaskGenerator
def write_output( primes_bool ):

    filepath = os.path.join(
        pm['data_dir'],
        'primes.hdf5',
    )
    f = h5py.File( filepath, 'w' )
    f.create_dataset( 'primes', data=primes_bool )

# TROVE PARAMS
import trove.build
import sys
pm = trove.build.link_params_to_config(
    config_fp = sys.argv[1],
)

# Load and process data
filepath = os.path.join(
    pm['data_dir'],
    'pre.hdf5',
)
f = h5py.File( filepath, 'r' )
numbers = np.array( f['numbers'][...] )

# Run
primes_bool = []
for n in numbers:
    primes_bool.append( jug.Task( is_prime, n ) )

write_output( primes_bool )
