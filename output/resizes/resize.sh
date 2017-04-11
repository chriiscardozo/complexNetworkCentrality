#!/bin/bash

for image_file in *.png
do
	convert $image_file[200x200] -set filename:mysize '%wx%h' $image_file'%[filename:mysize].png'
done
