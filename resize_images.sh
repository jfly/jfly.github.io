#!/usr/bin/bash

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")

IMGS_RE=".*\.\(jpg\|gif\|png\|jpeg\)"

if [ -d "public/img/original" ]; then
    for originalFile in `find public/img/original -iregex "$IMGS_RE"`; do
        # resize original images to a maximum size of 1024x1024 (full)
        fullFile=$(echo $originalFile | sed 's|public/img/original|public/img/full|g')

        # do not create a full file if one already exists
        if [ ! -f "$fullFile" ]; then
            mkdir -p `dirname $fullFile`
            echo Converting $originalFile to $fullFile
            convert $originalFile -resize 1024x1024 $fullFile
        fi
    done
fi

for fullFile in `find public/img/full -iregex "$IMGS_RE"`; do
    # resize full images to a maximum size of 400x400 (thumbs)
    thumbsFile=$(echo $fullFile | sed 's|public/img/full|public/img/thumbs|g')

    # do not create a thumbnail if one already exists
    if [ ! -f "$thumbsFile" ]; then
        mkdir -p `dirname $thumbsFile`
        echo Converting $fullFile to $thumbsFile
        convert $fullFile -resize 400x400 $thumbsFile
    fi
done

IFS=$SAVEIFS
