#!/usr/bin/env python3

import os
import numpy as np

N_BITS = 24

def prepare_M(n_bits):

    if os.path.isfile("M.npy"):
        print("M.npy is already generated")
        return np.load("M.npy")

    print("M.npy not found, generating ...")
    M=[]
    l=len(bin(2**n_bits-1)[2:])
    for i in range(1, 2**n_bits):
        string=bin(i)[2:].zfill(l)
        V = np.array([int(c) for c in string]).astype('uint8')
        M.append(V)

    M=np.asarray(M, dtype=np.uint8).T

    np.save("M.npy", M)
    return M


if __name__ == "__main__":
    prepare_M(N_BITS)





