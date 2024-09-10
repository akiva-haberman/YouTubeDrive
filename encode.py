import numpy as np
from PIL import Image
from textwrap import wrap
import sys
import os
import io

# number of fields being recorded
metaDataSize = 6

def updateImgArr(imgArr, pixel, blockSize, write_index, resolutionX):
    startRow    = write_index // resolutionX
    startColumn = write_index % resolutionX
    # print(f'row: {startRow}-{startRow + blockSize -1} Col: {startColumn}-{startColumn + blockSize - 1}')
    for i in range(startRow, startRow + blockSize):
        for j in range(startColumn, startColumn + blockSize):
            imgArr[i][j] = pixel
    return imgArr

def get_min_resolution(fileSize, blockSize):
    # there are usually 4 metadata fields
    res = int((fileSize*blockSize**2/3)**(0.5)) + metaDataSize + 1
    while res % blockSize != 0:
        res+=1
    return res

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
    # want big dif in color truing experiment
    black, white = (0,0,0), (255,255,255)
    # record meta data as first blocks
    metaData = [black, white, fileTuple, resXTuple, resYTuple, blockSizeTuple]
    for i, tup in enumerate(metaData):
        arr = updateImgArr(imgArr, tup, blockSize, i*blockSize, resolutionX)
    return arr

# writes a file to an image given a file, resolution, and blockSize (num pixels per side of square)
def writeFileToImage(inputFile, resolutionX, resolutionY, blockSize):
    # initialize array of tuples to be converted into image
    imgArr = [[(0,0,0)] * resolutionX for _ in range(resolutionY)]
    # write some file metadata
    imgArr = writeFileSpecs(imgArr, inputFile, resolutionX, resolutionY, blockSize)
    # current metadata takes up first 4 postions
    # write_index = get_write_index(resolutionX, blockSize)
    write_index = metaDataSize * blockSize
    print(write_index)
    # read 3 bytes at a time - RGB uses 3 bytes
    byte_size = 3
    with open(inputFile, 'rb') as f:
        # im = Image.open(io.BytesIO(f.read(3)))
        # im.close()
        while (byte := f.read(byte_size)):
            # convert bytes into
            pixel = bytesToRGB(byte.ljust(3,b'\x00'))
            imgArr = updateImgArr(imgArr, pixel, blockSize, write_index, resolutionX)
            # TODO: make a little nicer if you have time 
            # moving forward the writeindex at the end of a row
            if (write_index + blockSize - 1) % resolutionX == resolutionX -1:
                write_index+=resolutionX * (blockSize - 1)
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
    elif len(arguments) == 2:
        blockSize = int(arguments[1])
        fileSize = os.path.getsize(inputFile)
        res = get_min_resolution(fileSize, blockSize)
        resolutionX, resolutionY = res, res
    elif len(arguments) > 3:
        print("Too many arguments")
        sys.exit()
    else:
        resolutionX, resolutionY = int(arguments[1]), int(arguments[1])
        blockSize                = int(arguments[2])
        if resolutionX % blockSize or resolutionY % blockSize:
            # todo: learn errors and raise this nicely
            print("blockSize must evenly divide resolution")
            return
    print(f"Resolution = {resolutionX}X{resolutionY}")
    writeFileToImage(inputFile, resolutionX, resolutionY, blockSize)


if __name__ == "__main__":
    main()

