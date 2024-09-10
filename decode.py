from PIL import Image
from textwrap import wrap
import sys
import os
import numpy as np

# we are able to recover data from pixels!

def get_byte_arr(arr, blockSize):
    n, m, d = arr.shape
    assert n % blockSize == 0 and m % blockSize == 0 and d == 3
    # reshape array into square with edge length blockSize
    arr = arr.reshape(n//blockSize, blockSize, m//blockSize, blockSize, d)
    # todo: look over indexing
    colors = arr[:,blockSize//2,:, blockSize//2,:]
    return colors.flatten()

# def get_file_specs(arr):


def writeImageToFile(inputFile, outFile):
    with Image.open(inputFile) as im:
        arr = np.array(im)
    bytes = get_byte_arr(arr, 3)
    with open(outFile, 'wb') as f:
        f.write(bytes)
            
        
def main():
    inputFile = "new.png"
    outFile = "testOutput.pdf"
    arguments = sys.argv
    writeImageToFile(inputFile, outFile)


if __name__ == "__main__":
    main()
