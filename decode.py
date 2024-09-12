from PIL import Image
from textwrap import wrap
import sys
import os
import numpy as np
from encode import index_to_coord
import cv2 as cv

# we are able to recover data from pixels!

# explenation: basicly the metadata blocks, unlike the others, are one block to a byte. So if i want to record 20, let's say the resolution,
# then it would be (20,0,0). Which makes them 3 times as long. so i need to skip extra when going to read the actual data. 
MAGIC_META_NUMBER = 3

def to_images(path):
    capture = cv.VideoCapture(cv.samples.findFileOrKeep(path))
    if not capture.isOpened():
        print('Unable to open: ' + path)
        exit(0)
    frames = 0
    while False:
        ret, frame = capture.read()
        if frame is None:
            break
        frames+=1
    ret, frame = capture.read()
    for i in range(0,len(frame[0]),100):
        print(frame[0][i])
    print(frames)

def get_median_color(index, blockSide):
    print("getting there")


def index_to_center_coord(index, blockSide, resX):
    row, col = index_to_coord(index, blockSide, resX)
    halfSide = blockSide // 2
    return (row + halfSide, col + halfSide)

# rn just cutting of all trailing 0's on a file ... could lead to trouble down the line
def get_EOF(colors):
    index = len(colors) - 1
    while colors[index] == 0:
        index -=1 
    return index + 1

def get_byte_arr(arr, blockSide, metaDataSize):
    n, m, d = arr.shape
    assert n % blockSide == 0 and m % blockSide == 0 and d == 3
    # reshape array into square with edge length blockSide
    arr = arr.reshape(n//blockSide, blockSide, m//blockSide, blockSide, d)
    # todo: look over indexing
    colors = arr[:,blockSide//2,:, blockSide//2,:]
    flat =  colors.flatten()
    eof = get_EOF(flat)
    return flat[metaDataSize * MAGIC_META_NUMBER:eof]

# this is crude and would work if the pixels don't get messed up
def get_file_specs(imgArr):
    blockSideGuess = get_block_size(imgArr)
    resX = len(imgArr[0])
    # first 2 block are used for getting block size
    read_index = 2
    # get the center of the 3rd block
    mdRow, mdCol = index_to_center_coord(read_index, blockSideGuess, resX)
    # the metadatasize is the 3 block in the image
    metaDataSize = imgArr[mdRow][mdCol][0]
    # record the metadata info
    metaData = [0] * (metaDataSize - read_index)

    for i, _ in enumerate(metaData) :
        row, col = index_to_center_coord(read_index, blockSideGuess, resX)
        metaData[i] = imgArr[row][col][0]
        read_index+=1
    print(metaData)
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


def writeImageToFile(inFile, outName):
    with Image.open(inFile) as im:
        imgArr = np.array(im)
    metaDataSize, fileNum, _, _, blockSide = get_file_specs(imgArr)
    bytes = get_byte_arr(imgArr, blockSide, metaDataSize)
    print(bytes)
    outFile = outName + num_to_extension(fileNum)
    with open(outFile, 'wb') as f:
        f.write(bytes)
            
        
def main():
    inFile = "mygeneratedvideo.avi"
    outName = "testOutput"
    arguments = sys.argv
    to_images(inFile)
    writeImageToFile("outDir/testOutput.png", outName)


if __name__ == "__main__":
    main()
