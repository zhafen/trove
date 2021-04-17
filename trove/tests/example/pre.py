import numpy as np
import h5py

def generate_base_numbers( low, high, n ):

    return np.random.uniform( low, high, n )

def save_base_numbers( filepath, numbers ):

    f = h5py.File( filepath, 'w' )
    f.create_dataset( 'numbers', data=numbers )
    f.close()
    
if __name__ == '__main__':

    # Params
    # (as these would usually look)
    seed = 123
    low = 0
    high = 10
    n = 10

    # TROVE PARAMS
    # (as these would look wrapped in a trove call)
    import trove
    trove.update_parameters(
        config_fp = sys.argv[1],
        seed = 123,
        low = 0,
        high = 10,
        n = 10,
    )

    # Execution
    np.random.seed( seed )
    generate_base_numbers( low, high, n )
    save_base_numbers( filepath, numbers )
