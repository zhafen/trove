import h5py
import numpy as np
import os

# TROVE PARAMS
# (wrapping the parameters in a trove call)
import trove
import sys
pm = trove.link_params_to_config(
    config_fp = sys.argv[1],
)

# Load and process data
filepath = os.path.join(
    pm['data_dir'],
    'pre.hdf5',
)
f = h5py.File( filepath, 'r' )
numbers = np.array( f['numbers'][...] )

# Fancy calculation
raised_numbers = numbers ** pm['power']

# Save
save_filepath = os.path.join(
    pm['data_dir'],
    'main.hdf5',
)
g = h5py.File( save_filepath, 'w' )
print( 'Saving at {}'.format( save_filepath ) )
g.create_dataset( 'raised_numbers', data=raised_numbers )
g.close()

