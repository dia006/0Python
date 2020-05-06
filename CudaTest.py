# After installing CudaToolkit from NVidia install numba package from pip
# 
# https://github.com/numba/conda-recipe-cudatoolkit/issues/17
# For windows system, you can download and install Cuda Toolkit from CUDA Toolkit Archive.
# and install numba by pip install numba
# According to the searching order of Numba for a CUDA toolkit installation, you # could add an enviroment of CUDA_HOME=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.2.

import numpy as np
import time

import os

from numba import vectorize, cuda

# Check if environment variable for numba exists
# if(os.environ.get("CUDA_HOME", False)==False):
#     os.environ["CUDA_HOME"] = os.environ["CUDA_PATH_V9_2"]

def VectorAdd(a, b, c):
    for i in range(a.size):
        c[i] = a[i] + b[i]

def VectorAddOptimized(a, b):
    return( a + b )

@vectorize(["float32(float32, float32)"], target="cuda")
def VectorAddCuda(a, b):
    return( a + b )

def main():
    N = 32000000

    A = np.ones(N, dtype=np.float32)
    B = np.ones(N, dtype=np.float32)
    C = np.zeros(N, dtype=np.float32)

    start = time.time()
    VectorAdd(A, B, C)
    vector_add_time = time.time() - start
    print("C[:5] = " + str(C[:5]))
    print("C[-5:] = " + str(C[-5:]))
    print("VectorAdd took for {} seconds".format(vector_add_time))

    start = time.time()
    C = VectorAddOptimized(A, B)
    vector_add_time = time.time() - start
    print("C[:5] = " + str(C[:5]))
    print("C[-5:] = " + str(C[-5:]))
    print("VectorAddOptimized took for {} seconds".format(vector_add_time))

    start = time.time()
    C = VectorAddCuda(A, B)
    vector_add_time = time.time() - start
    print("C[:5] = " + str(C[:5]))
    print("C[-5:] = " + str(C[-5:]))
    print("VectorAddCuda took for {} seconds".format(vector_add_time))

if __name__=="__main__":
    main()