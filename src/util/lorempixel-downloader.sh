#!/bin/bash

# small script that allows you to download some random images from lorempixel

download_images(){
    # args:
    #   $1: initial number
    #   $2: final number
    #   $3: image width
    #   $4: image height
    for n in $(seq -w $1 $2); do wget http://lorempixel.com/$3/$4/ -O $n.jpg; done
}

# download a set of images from 01..30

# 5 images 640x480
download_images 01 05 640 480

# 5 images 1280x720
download_images 05 10 1280 720

# 5 images 1920x1080
download_images 10 15 1920 1080
