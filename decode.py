from PIL import Image
from textwrap import wrap
import sys
import os
import numpy as np
from encode import index_to_coord

# we are able to recover data from pixels!

# explenation: basicly the metadata blocks, unlike the others, are one block to a byte. So if i want to record 20, let's say the resolution,
# then it would be (20,0,0). Which makes them 3 times as long. so i need to skip extra when going to read the actual data. 
MAGIC_META_NUMBER = 3

def index_to_center_coord(index, blockSize, resX):
    row, col = index_to_coord(index, blockSize, resX)
    halfSide = blockSize // 2
    return (row + halfSide, col + halfSide)

def get_byte_arr(arr, blockSize, metaDataSize):
    n, m, d = arr.shape
    assert n % blockSize == 0 and m % blockSize == 0 and d == 3
    # reshape array into square with edge length blockSize
    arr = arr.reshape(n//blockSize, blockSize, m//blockSize, blockSize, d)
    # todo: look over indexing
    colors = arr[:,blockSize//2,:, blockSize//2,:]
    flat =  colors.flatten()
    return flat[metaDataSize * MAGIC_META_NUMBER:]

# this is crude and would work if the pixels don't get messed up
def get_file_specs(imgArr):
    blockSizeGuess = get_block_size(imgArr)
    resX = len(imgArr[0])
    # first 2 block are used for getting block size
    read_index = 2
    # get the center of the 3rd block
    mdRow, mdCol = index_to_center_coord(read_index, blockSizeGuess, resX)
    # the metadatasize is the 3 block in the image
    metaDataSize = imgArr[mdRow][mdCol][0]
    # record the metadata info
    metaData = [0] * (metaDataSize - read_index)

    for i, _ in enumerate(metaData) :
        row, col = index_to_center_coord(read_index, blockSizeGuess, resX)
        metaData[i] = imgArr[row][col][0]
        read_index+=1
    return tuple(metaData)


# caution going in with guesses
# this is okay for now...
def get_block_size(imgArr):
    topRow = imgArr[0]
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
        imgArr = np.array(im)
    metaDataSize, fileNum, _, _, blockSize = get_file_specs(imgArr)
    bytes = get_byte_arr(imgArr, blockSize, metaDataSize)
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
