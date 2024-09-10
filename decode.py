from PIL import Image
from textwrap import wrap
import sys
import os
import numpy as np

# we are able to recover data from pixels!
# idea: idk really know how YT comnpression works rn


def get_byte_arr(arr, blockSize):
    n, m, d = arr.shape
    assert n % blockSize == 0 and m % blockSize == 0 and d == 3
    # reshape array into square with edge length blockSize
    arr = arr.reshape(n//blockSize, blockSize, m//blockSize, blockSize, d)
    colors = arr[:,blockSize//2,:, blockSize//2,:]
    return colors.flatten()

def writeImageToFile(inputFile):
    with Image.open(inputFile) as im:
        arr = np.array(im)
        bytes = get_byte_arr(arr, 3)
        # for p in arr:
        #     print(chr(p), end='')
        
            
        
def main():
    inputFile = "new.png"
    outputFile = "testOutput.txt"
    arguments = sys.argv
    writeImageToFile(inputFile)


if __name__ == "__main__":
    main()
