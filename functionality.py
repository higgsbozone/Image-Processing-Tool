import numpy as np

def greyscale (array) :
    grey = np.mean(array, axis = 2).astype(np.uint8)
    grey = np.stack((grey, grey, grey), axis=2)

    return grey

def invert (array) :

    invert = 255 - array

    return invert

def brightness (array, nums) :

    bright = array
    bright = bright.astype(np.int16)
    bright += nums
    bright = np.clip(bright, 0, 255)
    bright = bright.astype(np.uint8)

    return bright

def flipped_array(array, op) :

    if op == "horizontal" :
        array = array[:,::-1,:]
    elif op == "vertical" :
        array = array[::-1,:,:]

    return array




