import numpy as np
from PIL import Image
from textwrap import wrap
import sys
import os
import io

# TODO: make sure resolution and block size jive 

def updateImgArr(imgArr, pixel, blockSize, write_index, resolutionX):
    startRow    = write_index // resolutionX
    startColumn = write_index % resolutionX
    # print(f'row: {startRow}-{startRow + blockSize} Col: {startColumn}-{startColumn+ blockSize}')
    for i in range(startRow, startRow + blockSize):
        for j in range(startColumn, startColumn + blockSize):
            imgArr[i][j] = pixel
    return imgArr


def bytesToRGB(x):
    # wrapper = TextWrapper(width = 2)
    red, green, blue = wrap(x.hex(), 2)
    return (int(red,16), int(green,16), int(blue,16))

def bytesToHexTriplets(x):
    red, green, blue = wrap(x.hex(), 2)
    return (red, green, blue,)

def arrToImg(arr, resolutionX, resolutionY):
    array = np.array(arr)
    array = np.reshape(array,(resolutionY,resolutionX,3))
    new_image = Image.fromarray(array.astype(np.uint8), mode='RGB')
    new_image.save('new.png')

def byteToBin(x):
    return bin(int(x.hex(), 16))[2:].zfill(8)

def binToAscii(x):
    return chr(int(x,2))

def extensionToNum(fileType):
    if fileType == 'pdf':
        return 2
    return 1

# file_type,resolution,blockSize
# for now txt = 1, pdf = 2, we'll formalize this later
# 4 ints which is
# writes header in pixels for the file
# !currently thinking about blocks of size 3 and 1 so adding in 2 blocks of buffer
def writeFileSpecs(imgArr, inputFile, resolutionX, resolutionY, blockSize):
    fileExtension = os.path.splitext(inputFile)[1]
    fileType = extensionToNum(fileExtension[1:])
    # for later reconstruction record type of file
    fileTuple = (fileType, 0, 0)
    # for later reconstruction record resolutions
    resXTuple = (resolutionX, 0, 0)
    resYTuple = (resolutionY, 0, 0)
    # for later reconstruction record blockSize
    blockSizeTuple = (blockSize, 0, 0)
    buffer = (255,255,255)
    for i, tup in enumerate([fileTuple, resXTuple, resYTuple, blockSizeTuple, buffer, buffer]):
        arr = updateImgArr(imgArr, tup, blockSize, i, resolutionX)
    return arr

# writes a file to an image given a file, resolution, and blockSize (num pixels per side of square)
def writeFileToImage(inputFile, resolutionX, resolutionY, blockSize):
    # initialize array of tuples to be converted into image
    imgArr = [[(0,0,0)] * resolutionX for _ in range(resolutionY)]
    # write some file metadata
    imgArr = writeFileSpecs(imgArr, inputFile, resolutionX, resolutionY, blockSize)
    # current metadata takes up first  postions
    # !this is a magic number because i'm working on other things
    write_index = 6
    # read 3 bytes at a time - RGB uses 3 bytes
    byte_size = 3
    with open(inputFile, 'rb') as f:
        # im = Image.open(io.BytesIO(f.read(3)))
        # im.close()
        while (byte := f.read(byte_size)):
            # convert bytes into
            pixel = bytesToRGB(byte.ljust(3,b'\x00'))
            imgArr = updateImgArr(imgArr, pixel, blockSize, write_index, resolutionX)
            # TODO: fix write index 
            write_index+=blockSize
    arrToImg(imgArr, resolutionX, resolutionY)
        

def main():
    inputFile = "testFiles/tutorial.pdf"
    outputFile = "testOutput.txt"
    # print("Please enter resolution and Pixel Block size. ex: \"(720,480) 4 \" ")
    arguments = sys.argv
    if len(arguments) < 2:
        resolutionX = 75
        resolutionY = 75
        blockSize = 1
    elif len(arguments) > 3:
        print("Too many arguments")
        sys.exit()
    else:
        resolutionX, resolutionY = int(arguments[1]), int(arguments[1])
        blockSize                = int(arguments[2])
    print(f"Resolution = {resolutionX}X{resolutionY}")
    writeFileToImage(inputFile, resolutionX, resolutionY, blockSize)


if __name__ == "__main__":
    main()

