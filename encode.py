import numpy as np
from PIL import Image
from textwrap import wrap
import sys
import os
import io


# number of fields being recorded
metaDataSize = 7

def update_write_index(write_index, blockSize, resX):
    if (write_index + blockSize - 1) % resX == resX -1:
        write_index+=resX * (blockSize - 1)
    write_index+=blockSize
    return write_index

# writing pixels from the top left corner
def updateImgArr(imgArr, pixel, blockSize, write_index, resX):
    startRow    = write_index // resX
    startColumn = write_index % resX
    print(f'row: {startRow}-{startRow + blockSize -1} Col: {startColumn}-{startColumn + blockSize - 1}')
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

def arrToImg(arr, resX, resY):
    array = np.array(arr)
    array = np.reshape(array,(resY,resX,3))
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
def writeFileSpecs(imgArr, inputFile, resX, resY, blockSize):

    fileExtension = os.path.splitext(inputFile)[1]
    fileType = extensionToNum(fileExtension[1:])

    metaDataTuple = (metaDataSize, 0, 0)
    # for later reconstruction record type of file
    fileTuple = (fileType, 0, 0)
    # for later reconstruction record resolutions
    resXTuple = (resX, 0, 0)
    resYTuple = (resY, 0, 0)
    # for later reconstruction record blockSize
    blockSizeTuple = (blockSize, 0, 0)
    # want big dif in color truing experiment
    black, white = (0,0,0), (255,255,255)
    # record meta data as first blocks
    metaData = [black, white, metaDataTuple, fileTuple, resXTuple, resYTuple, blockSizeTuple]
    write_index = 0
    for i, tup in enumerate(metaData):
        arr = updateImgArr(imgArr, tup, blockSize, write_index, resX)
        write_index = update_write_index(write_index, blockSize, resX)
    write_index = update_write_index(write_index, blockSize, resX)

    return (arr, write_index)

# writes a file to an image given a file, resolution, and blockSize (num pixels per side of square)
def writeFileToImage(inputFile, resX, resY, blockSize):
    # initialize array of tuples to be converted into image
    imgArr = [[(0,0,0)] * resX for _ in range(resY)]
    # write some file metadata
    imgArr, write_index = writeFileSpecs(imgArr, inputFile, resX, resY, blockSize)
    # current metadata takes up first 4 postions
    # write_index = get_write_index(resX, blockSize)
    # write_index = metaDataSize * blockSize
    print(write_index)
    # read 3 bytes at a time - RGB uses 3 bytes
    byte_size = 3
    with open(inputFile, 'rb') as f:
        # im = Image.open(io.BytesIO(f.read(3)))
        # im.close()
        while (byte := f.read(byte_size)):
            # convert bytes into
            pixel = bytesToRGB(byte.ljust(3,b'\x00'))
            imgArr = updateImgArr(imgArr, pixel, blockSize, write_index, resX)
            # TODO: make a little nicer if you have time 
            write_index = update_write_index(write_index, blockSize, resX)
            
    arrToImg(imgArr, resX, resY)
        

def main():
    inputFile = "testInput.txt"
    outputFile = "testOutput.txt"
    # print("Please enter resolution and Pixel Block size. ex: \"(720,480) 4 \" ")
    arguments = sys.argv
    if len(arguments) < 2:
        resX = 75
        resY = 75
        blockSize = 1
    elif len(arguments) == 2:
        blockSize = int(arguments[1])
        fileSize = os.path.getsize(inputFile)
        res = get_min_resolution(fileSize, blockSize)
        resX, resY = res, res
    elif len(arguments) > 3:
        print("Too many arguments")
        sys.exit()
    else:
        resX, resY = int(arguments[1]), int(arguments[1])
        blockSize                = int(arguments[2])
        if resX % blockSize or resY % blockSize:
            # todo: learn errors and raise this nicely
            print("blockSize must evenly divide resolution")
            return
    print(f"Resolution = {resX}X{resY}")
    writeFileToImage(inputFile, resX, resY, blockSize)


if __name__ == "__main__":
    main()

