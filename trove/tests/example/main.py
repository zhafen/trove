import numpy as np
import h5py

# Params

# Load and process data
f = h5py.File( filepath, 'r' )
numbers = np.array( f['numbers'][...] )

# Fancy calculation
raised_numbers = numbers ** power

# Save
g = h5py.File( save_filepath, 'w' )
g.create_dataset( 'raised_numbers', data=raised_numbers )
g.close()

