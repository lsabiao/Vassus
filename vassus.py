#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from PIL import Image

import os
import sys
import tempfile
import argparse

try:
	#python3
	from urllib.request import urlopen
except:
	#python2
	from urllib2 import urlopen


def printImage(imagePath,fit=True):
	px = "▄"
	
	terY,terX = os.popen('stty size','r').read().split()
	terX = int(terX)
	terY = int(terY)
	terX-=1
	terY=terY*2
	im = prepareImage(imagePath).convert("RGB")


	if(fit):
		im.thumbnail((terX,terY))
	for y in range(0,im.size[1],2):
		for x in range(im.size[0]):
			r,g,b = im.getpixel((x,y))
			try:
				rr,gg,bb = im.getpixel((x,y+1))
			except:
				rr,gg,bb = (0,0,0)
			#TODO render transparency
			print("\033[48;2;{rb};{gb};{bb}m\033[38;2;{rf};{gf};{bf}m{px}".format(rb=r,gb=g,bb=b,rf=rr,gf=gg,bf=bb,px=px),end='')
		print("\033[0m ")


def prepareImage(path):
	prefix = ["http://","https://","ftp://"]
	local = True
	for p in prefix:
		if(path.startswith(p)):
			local = False
	if(local):
		try:
			im = Image.open(os.path.realpath(path))
		except:
			print("Image cannot be loaded")
			sys.exit(1)
	else:
		try:
			downloaded = urlopen(path)
			pre = tempfile.SpooledTemporaryFile()
			pre.write(downloaded.read())
			im = Image.open(pre)
		except:
			print("Image cannot be loaded")
			sys.exit(1)
	return im
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("image",nargs='*',help="The image to render")
	parser.add_argument("--no-resize",help="keep the size of the image",action="store_false")
	args = parser.parse_args()
        
        imagelen = len(args.image)

        if(imagelen > 1):
            space_between = 4
        else:
            space_between = 0

        for i in range(imagelen):
	    printImage(args.image[i],args.no_resize)
            if(i < imagelen-1):
                print("\n"*space_between)


        #TODO create the thumbnails

