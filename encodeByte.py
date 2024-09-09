
# TODO: what if bytes aren't properly divisable -> error lol??
from PIL import Image
from textwrap import wrap
import sys
import os
import numpy as np
import png

def updateImgArr(imgArr, pixel, blockSize, write_index, resolutionX):
    startRow    = write_index // resolutionX
    startColumn = write_index % resolutionX
    for i in range(startRow, startRow + blockSize):
        for j in range(startColumn, startColumn + blockSize):
            imgArr[i][j] = pixel
    return imgArr
    
def bytesToRGB(x):
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
def writeFileSpecs(imgArr, inputFile, resolutionX, resolutionY, blockSize):
    fileExtension = os.path.splitext(inputFile)[1]
    fileType = extensionToNum(fileExtension[1:])
    fileTuple = (fileType, fileType, fileType)
    resXTuple = (resolutionX, resolutionX, resolutionX)
    resYTuple = (resolutionY, resolutionY, resolutionY)
    blockSizeTuple = (blockSize, blockSize, blockSize)
    for i, tup in  enumerate([fileTuple, resXTuple, resYTuple, blockSizeTuple]):
        arr = updateImgArr(imgArr, tup, blockSize, i, resolutionX)
    return arr
    
def writeFileToImage(inputFile, resolutionX, resolutionY, blockSize):
    imgArr = [[(0,0,0)] * resolutionX for _ in range(resolutionY)]
    imgArr = writeFileSpecs(imgArr, inputFile, resolutionX, resolutionY, blockSize)
    write_index = 4
    with open(inputFile, 'rb') as f:
        with open('newByte.png','wb'):
            while (byte := f.read(3)):
                pixel = bytesToRGB(byte.ljust(3,b'\x00'))
                imgArr = updateImgArr(imgArr, pixel, blockSize, write_index, resolutionX)
                write_index+=blockSize
    arrToImg(imgArr, resolutionX, resolutionY)
        

def main():
    inputFile = "testInput.txt"
    outputFile = "testOutput.txt"
    # print("Please enter resolution and Pixel Block size. ex: \"(720,480) 4 \" ")
    arguments = sys.argv
    if len(arguments) < 2:
        resolutionX = 10
        resolutionY = 10
        blockSize = 1
    elif len(arguments) > 3:
        print("Too many arguments")
        sys.exit()
    else:
        resolutionX, resolutionY = arguments[1]
        blockSize                = arguments[2]
    print(f"Resolution = {resolutionX}X{resolutionY}")
    writeFileToImage(inputFile, resolutionX, resolutionY, blockSize)


if __name__ == "__main__":
    main()

