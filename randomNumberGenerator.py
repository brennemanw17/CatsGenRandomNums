"""
@Author: William Samuel Brenneman
@Github: https://github.com/brennemanw17

This program is used to generate random numbers, to do so it uses image data.
Currently the random images are supplied from the link found in getimg() and are images of cats.

@Usage:
    genrandom() - random integer generation
    genrandom(min,max) - random integer between min and max including min and max
"""
import hashlib
import io
import json
import requests
from PIL import Image
from bitstring import BitArray


# getimg() return url to random image in this case cats
# return: image URL
def getimg():
    catURL = 'http://aws.random.cat/meow'
    imageURL = json.loads(requests.get(catURL).content)["file"]
    return imageURL


# Return binary image hashed with MD5
# @args: binary image
# @return: image binary hashed with MD5
def getmd5(binary):
    result = hashlib.md5(binary)
    return BitArray(result.digest()).bin


# Return binary image hashed with SHA-256
# @args: binary image
# @return: image binary hashed with SHA-256
def getsha256(binary):
    result = hashlib.sha256(binary)
    return BitArray(result.digest()).bin


# Returns a given list of images with images as strings of binary
# @args: images, a list of images
# @return: a list of images as binary strings
def imagetobin():
    url = getimg()
    img = Image.open(requests.get(url, stream=True).raw, mode="r")
    imgbytes = io.BytesIO()
    img.save(imgbytes, format=img.format)
    imgbytes = imgbytes.getvalue()
    return BitArray(imgbytes).bin


# Returns first half of the SHA hash XOR'd with the MD5 concatinated with
# the second half of the SHA hash XOR'd with the MD5 hash
# @args: sha: sha256 hash, md5: md5 hash
# @returns: (sha[0:128] XOR md5) + (sha[128:] XOR md5)
def XOR(sha, md5):
    sha1 = sha[0:128]
    sha2 = sha[128:]
    gen1 = ""
    gen2 = ""
    for x in range(0,128):
        if sha1[x] == md5[x]:
            gen1 = gen1 + "1"
        else:
            gen1 = gen1 + "0"
        if sha2[x] == md5[x]:
            gen2 = gen2 + "1"
        else:
            gen2 = gen2 + "0"
    return gen1 + gen2


# Generates random numbers
# @args: none or min amount and maximum amount
# @returns: random integer, if max/min given it is constrained by these
def genrandom(min = 0, max = 0):
    # Generate 1 random number
    if max == 0 and min == 0:
        img = imagetobin().encode('utf-8')
        num = XOR(getsha256(img), getmd5(img))
        return int(num, 2)
    # Generate random number between min and max
    else:
        max = max + 1
        img = imagetobin().encode('utf-8')
        num = XOR(getsha256(img), getmd5(img))
        num = int(num, 2) % max
        while num < min:
            if num + min < max:
                return num + min
            else:
                num = (num + min) % max
        return num




