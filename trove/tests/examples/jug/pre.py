import h5py
import numpy as np
import os

def generate_base_numbers( low, high, ):

    return np.arange( low, high + 1., 1. ).astype( int )

def save_base_numbers( filepath, numbers ):

    print( 'Saving at {}'.format( filepath ) )
    f = h5py.File( filepath, 'w' )
    f.create_dataset( 'numbers', data=numbers )
    f.close()
    
if __name__ == '__main__':

    # Params
    # (how the parameters would usually look)
    pm = dict(
        low = 0,
        high = 10,
    )

    # TROVE PARAMS
    # (wrapping the parameters in a trove call)
    import trove.build
    import sys
    pm = trove.build.link_params_to_config(
        config_fp = sys.argv[1],
        **pm
    )

    # Execution
    numbers = generate_base_numbers( pm['low'], pm['high'], )
    filepath = os.path.join(
        pm['data_dir'],
        'pre.hdf5',
    )
    save_base_numbers( filepath, numbers )
