from PIL import Image
from textwrap import wrap
import sys
import os
import numpy as np
from encode import update_write_index

# we are able to recover data from pixels!

def get_byte_arr(arr, blockSize):
    n, m, d = arr.shape
    assert n % blockSize == 0 and m % blockSize == 0 and d == 3
    # reshape array into square with edge length blockSize
    arr = arr.reshape(n//blockSize, blockSize, m//blockSize, blockSize, d)
    # todo: look over indexing
    colors = arr[:,blockSize//2,:, blockSize//2,:]
    return colors.flatten()

# this is crude and would work if the pixels don't get messed up
# TODO: fix two line metadata
def get_file_specs(imArr):
    blockSizeGuess = get_block_size(imArr)
    centerRow = imArr[blockSizeGuess // 2]
    resX = len(imArr[0])
    metaDataSize = centerRow[blockSizeGuess * 2 + blockSizeGuess//2][0]
    print(metaDataSize)
    metaData = [0] * metaDataSize
    read_index = 3 * blockSizeGuess
    for i in range(metaDataSize):
        print(read_index)

        metaData[i] = centerRow[read_index][0]
        read_index = update_write_index(read_index, blockSizeGuess, resX)
    print(f'blockSizeGuess = {blockSizeGuess}, centerRow = {centerRow}')
    return tuple(metaData)


# caution going in with guesses
# this is okay for now...
def get_block_size(imArr):
    topRow = imArr[0]
    firstColor = topRow[0]
    temp = firstColor
    index = 0
    while temp.all() == firstColor.all():
        temp = topRow[index]
        index+=1
    return index -1
# should make default dict to handle errors and file types
def num_to_extension(num):
    types = {
        1 : '.txt',
        2 : '.pdf'
    }
    return types[num]


def writeImageToFile(inputFile, outName):
    with Image.open(inputFile) as im:
        imArr = np.array(im)
    fileNum, resX, resY, blockSize = get_file_specs(imArr)
    bytes = get_byte_arr(imArr, blockSize)
    outFile = outName + num_to_extension(fileNum)
    with open(outFile, 'wb') as f:
        f.write(bytes)
            
        
def main():
    inputFile = "new.png"
    outName = "testOutput"
    arguments = sys.argv
    writeImageToFile(inputFile, outName)


if __name__ == "__main__":
    main()
