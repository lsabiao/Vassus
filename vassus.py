#!/usr/bin/env python3
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
	try:
		im = prepareImage(imagePath).convert("RGB")
	except:
		return


	if(fit):
		im.thumbnail((terX,terY))
	for y in range(0,im.size[1],2):
		buffer = ""
		for x in range(im.size[0]):
			r,g,b = im.getpixel((x,y))
			try:
				rr,gg,bb = im.getpixel((x,y+1))
			except:
				rr,gg,bb = (0,0,0)
			
			buffer+= "\033[48;2;{rb};{gb};{bb}m\033[38;2;{rf};{gf};{bf}m{px}".format(rb=r,gb=g,bb=b,rf=rr,gf=gg,bf=bb,px=px)
		
		print(center_image(buffer,im.size[0],terX),end="")
		print("\033[0m ")


def prepareImage(path):
	prefix = ["http://","https://","ftp://"]
	local = True
	for p in prefix:
		if(path.startswith(p)):
			local = False
	if(local):
		if(os.path.isdir(os.path.realpath(path))):
			return False
		try:
			im = Image.open(os.path.realpath(path))
		except:
			return False
	else:
		try:
			downloaded = urlopen(path)
			pre = tempfile.SpooledTemporaryFile()
			pre.write(downloaded.read())
			im = Image.open(pre)
		except:
			return False
	print(f"\033[1m{path.center(terWidth)}\033[0m")
	return im


def center_image(to_center,img_width,terminal_width):
	if(img_width >= terminal_width):
		return to_center
	
	offset = (terminal_width - img_width)//2
	return f"{' '*offset}{to_center}\033[0m{' '*offset}"





if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("image",nargs='*',help="The image to render")
	parser.add_argument("--no-resize",help="keep the size of the image",action="store_false")
	args = parser.parse_args()

	terY,terX = os.popen('stty size','r').read().split()
	terWidth = int(terX)
		
	imagelen = len(args.image)
		
	if(imagelen > 1):
		space_between = 2
	else:
		space_between = 0
	
	index = 0
	for img in args.image:

		print("\n"*space_between)
		#print(f"\033[1m{img.center(terX)}\033[0m")
		printImage(args.image[index],args.no_resize)


		index+=1


	#TODO create the thumbnails

