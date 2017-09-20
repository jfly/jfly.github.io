#!/usr/bin/env python3

import os
import re
import yaml
import argparse
import subprocess
from os.path import join, exists

EXTENSIONS = "(jpg|png)"
IMAGE_RE = re.compile(r".*\.{}".format(EXTENSIONS), re.IGNORECASE)
THUMBNAIL_RE = re.compile(r".*-thumb\.{}".format(EXTENSIONS), re.IGNORECASE)

def is_image(name):
    return IMAGE_RE.match(name)

def is_master_image(name):
    return is_image(name) and not is_thumbnail_image(name)

def is_thumbnail_image(name):
    return is_image(name) and THUMBNAIL_RE.match(name)

def get_thumbnail_name(name):
    return name[::-1].replace(".", ".bmuht-", 1)[::-1]

def get_image_size(path):
    return subprocess.check_output(["identify", "-format", "%G", path]).decode("utf-8")

def resize(args):
    image_data = {}
    for root, dirs, names in os.walk('.'):
        for name in names:
            path = join(root, name)
            if path.startswith("./_site"):
                continue
            if is_master_image(name):
                thumbnail_name = get_thumbnail_name(name)
                thumbnail_path = join(root, thumbnail_name)
                thumbnail_exists = exists(thumbnail_path)

                should_generate_thumbnail = None
                if not thumbnail_exists or args.force:
                    should_generate_thumbnail = True
                    if args.dry_run:
                        if thumbnail_exists:
                            print("Thumbnail already exists, but regenerating {}".format(thumbnail_path))
                        else:
                            print("Generating nonexistent thumbnail {}".format(thumbnail_path))
                else:
                    should_generate_thumbnail = False

                url = path[1::]
                image_data[url] = {
                    "size": get_image_size(path),
                }

                if should_generate_thumbnail and not args.dry_run:
                    print("Generating {} from {}".format(thumbnail_path, path))
                    subprocess.check_call(["convert", path, "-resize", "400x400>", thumbnail_path])

    with open('_data/images.yml', 'w') as out:
        yaml.dump(image_data, out, default_flow_style=False)

def main():
    parser = argparse.ArgumentParser(description='Resize images')
    parser.add_argument('--dry-run', '-n', action='store_true',
			help='perform a trial run with no changes made')
    parser.add_argument('--force', '-f', action='store_true',
			help='force regenerating thumbnail images even if they alread exist')
    args = parser.parse_args()

    resize(args)

if __name__ == "__main__":
    main()
