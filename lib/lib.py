import numpy as np


def get_slope(target:np.array, radius:int=1) -> np.array:
   
    kernel = _get_slope_kernel(radius)
    slope = _convolve2d(target, kernel)
    return slope
    
    
def _get_slope_kernel(radius:int=1) -> np.array:
    
    
    klist = []
    for sn in range(radius, (radius +1) *-1, -1):
        row = []
        sn = float(sn)
        for ew in range(radius * -1, radius + 1):
            ew = float(ew)
            cell = ew + sn * 1j
            length = (ew ** 2.0 +  sn ** 2.0 ) ** 0.5
            if length != 0.0:
                          
                cell /= length
            row.append(cell)
        klist.append(row)
    kernel = np.array(klist)
    
    return kernel * -1.0


def _convolve2d(target:np.array, kernel:np.array) -> np.array:

        

    sub_shape = tuple(np.subtract(target.shape, kernel.shape) + 1)

    
    strd = np.lib.stride_tricks.as_strided


    submatrices = strd(target, kernel.shape + sub_shape, target.strides * 2)

    
    convolved_matrix = np.einsum('ij,ijkl->kl', kernel, submatrices)

    return convolved_matrix
