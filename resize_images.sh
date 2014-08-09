#!/usr/bin/bash

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")

for originalFile in `find public/img/original -name "*.jpg"`; do
    # resize original images to a maximum size of 1024x1024 (full)
    fullFile=$(echo $originalFile | sed 's|public/img/original|public/img/full|g')
    mkdir -p `dirname $fullFile`
    echo Converting $originalFile to $fullFile
    convert $originalFile -resize 1024x1024 $fullFile

    # resize full images to a maximum size of 400x400 (thumbs)
    thumbsFile=$(echo $originalFile | sed 's|public/img/original|public/img/thumbs|g')
    mkdir -p `dirname $thumbsFile`
    echo Converting $originalFile to $thumbsFile
    convert $originalFile -resize 400x400 $thumbsFile
done

IFS=$SAVEIFS
