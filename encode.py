import numpy as np
from PIL import Image
from textwrap import wrap
import sys
import os
# from toVideo import FPS
# from decode import MAGIC_META_NUMBER


# number of fields being recorded
metaDataSize = 7
# will fix when i'm not lazy (cicular imports)
MAGIC_META_NUMBER = 3


def get_new_file_name(base_name, extension):
    filename = f"{base_name}.{extension}"
    counter = 1
    while os.path.exists(filename):
        filename = f"{base_name}{counter}.{extension}"
        counter+=1
    return filename

# gives the top left pixel in blockSide
def index_to_coord(index, blockSide, resX):
    row = (index * blockSide // resX ) * blockSide
    col = (index * blockSide % resX) 
    return (row, col)

def update_img_arr(imgArr, pixel, blockSide, write_index, resX):
    # this feels weird, but may be necessary
    startRow, startColumn    = index_to_coord(write_index, blockSide, resX)
    # print(f' write_index = {write_index} row: {startRow}-{startRow + blockSide -1} Col: {startColumn}-{startColumn + blockSide - 1}')
    for i in range(startRow, startRow + blockSide):
        for j in range(startColumn, startColumn + blockSide):
            imgArr[i][j] = pixel
    return imgArr

# currently assuming square resolution
# this is a dumb func, we only need pagebytes
def bytes_per_png(blockSide, resX):
    pagePixels = resX ** 2
    blockSize = blockSide ** 2
    # nice thinking dog
    bytesPerPixel = 3
    pageBytes = (pagePixels / blockSize) * bytesPerPixel
    return int(pageBytes)

def get_min_resolution(fileSize, blockSide):
    # there are usually 4 metadata fields
    res = int((fileSize * blockSide**2 /3)**(0.5)) + metaDataSize + 1
    while res % blockSide != 0:
        res+=1
    return res

def bytesToRGB(x):
    # todo: comeback to this i think we can do it more effeciently 
    # wrapper = TextWrapper(width = 2)
    red, green, blue = wrap(x.hex(), 2)
    return (int(red,16), int(green,16), int(blue,16))

def bytesToHexTriplets(x):
    red, green, blue = wrap(x.hex(), 2)
    return (red, green, blue,)

def arrToImg(arr, resX, resY, outFile):
    array = np.array(arr)
    array = np.reshape(array, (resY, resX, 3))
    new_image = Image.fromarray(array.astype(np.uint8), mode='RGB')
    new_image.save(outFile)

def byteToBin(x):
    return bin(int(x.hex(), 16))[2:].zfill(8)

def binToAscii(x):
    return chr(int(x,2))

def extensionToNum(fileType):
    if fileType == 'pdf':
        return 2
    return 1

# file_type,resolution,blockSide
# for now txt = 1, pdf = 2, we'll formalize this later
# 4 ints which is
# writes header in pixels for the file
def writeFileSpecs(imgArr, inputFile, resX, resY, blockSide):

    fileExtension = os.path.splitext(inputFile)[1]
    fileType = extensionToNum(fileExtension[1:])

    metaDataTuple = (metaDataSize, 0, 0)
    # for later reconstruction record type of file
    fileTuple = (fileType, 0, 0)
    # for later reconstruction record resolutions
    resXTuple = (resX, 0, 0)
    resYTuple = (resY, 0, 0)
    # for later reconstruction record blockSide
    blockSideTuple = (blockSide, 0, 0)
    # want big dif in color truing experiment
    black, white = (0,0,0), (255,255,255)
    # record meta data as first blocks
    metaData = [black, white, metaDataTuple, fileTuple, resXTuple, resYTuple, blockSideTuple]
    write_index = 0
    for i, tup in enumerate(metaData):
        arr = update_img_arr(imgArr, tup, blockSide, write_index, resX)
        write_index+=1
    return (arr, write_index)

# writes a file to an image given a file, resolution, and blockSide (num pixels per side of square)
def writeFileToImage(inputFile, resX, resY, blockSide, outName, bytesPerPng):
    # initialize array of tuples to be converted into image
    imgArr = [[(0,0,0)] * resX for _ in range(resY)]
    # write some file metadata
    imgArr, write_index = writeFileSpecs(imgArr, inputFile, resX, resY, blockSide)
    # current metadata takes up first 4 postions
    # write_index = 7
    # read 3 bytes at a time - RGB uses 3 bytes
    chunk_size = 3
    with open(inputFile, 'rb') as f:
        while (byte := f.read(chunk_size)):
            # TODO: explain this
            if 3 * write_index // bytesPerPng > 0:
                outFile = get_new_file_name(outName, 'png')
                arrToImg(imgArr, resX, resY, outFile)
                write_index = 0
            # convert bytes into
            pixel = bytesToRGB(byte.ljust(3,b'\x00'))
            imgArr = update_img_arr(imgArr, pixel, blockSide, write_index, resX)
            write_index+=1
        outFile = get_new_file_name(outName, 'png')
        arrToImg(imgArr, resX, resY, outFile)
            
        

def main():
    inputFile = "testFiles/tutorial.pdf"
    outName = "./outDir/testOutput"
    fileSize = os.path.getsize(inputFile)
    arguments = sys.argv
    if len(arguments) == 1:
        resX = 75
        resY = 75
        blockSide = 1
    elif len(arguments) == 2:
        blockSide = int(arguments[1])
        res = get_min_resolution(fileSize, blockSide)
        resX, resY = res, res
    elif len(arguments) > 3:
        print("Too many arguments")
        sys.exit()
    else: # ==3 are you dumb?
        resX, resY = int(arguments[1]), int(arguments[1])
        blockSide                = int(arguments[2])
        if resX % blockSide or resY % blockSide:
            # todo: learn errors and raise this nicely
            print("blockSide must evenly divide resolution")
            return
    print(f"Resolution = {resX}X{resY}")
    bpp = bytes_per_png(blockSide, resX)
    print(bpp)
    writeFileToImage(inputFile, resX, resY, blockSide, outName, bpp)


if __name__ == "__main__":
    main()

