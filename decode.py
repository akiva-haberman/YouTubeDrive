from PIL import Image
from textwrap import wrap
import sys
import os
import numpy as np


def writeImageToFile(inputFile):
    with Image.open(inputFile) as im:
        arr = np.array(im).flatten().flatten()
        for p in arr:
            print(chr(p), end='')
        
        
            # specs = im.read(1)
            # print(specs, chr(int.from_bytes(specs, byteorder='little', signed=False)))
            

        
        # while (byte := im.read(3)):
        #     print(byte, byte.decode('ascii'))
            
        
def main():
    inputFile = "new.png"
    outputFile = "testOutput.txt"
    arguments = sys.argv
    writeImageToFile(inputFile)


if __name__ == "__main__":
    main()
