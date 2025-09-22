#!/usr/bin/env python3

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from os.path import exists, join
from textwrap import dedent

import yaml

EXTENSIONS = "(jpg|png)"
IMAGE_RE = re.compile(r".*\.{}".format(EXTENSIONS), re.IGNORECASE)
THUMBNAIL_RE = re.compile(r".*-thumb\.{}".format(EXTENSIONS), re.IGNORECASE)


def is_image(name):
    return IMAGE_RE.match(name)


def is_og_image(name):
    return is_image(name) and not is_thumbnail_image(name)


def is_thumbnail_image(name):
    return is_image(name) and THUMBNAIL_RE.match(name)


def get_thumbnail_name(name):
    return name[::-1].replace(".", ".bmuht-", 1)[::-1]


@dataclass
class Dimension:
    width: int
    height: int

    @classmethod
    def parse(cls, s):
        width, height = s.split("x")
        return cls(
            width=int(width),
            height=int(height),
        )

    def __str__(self):
        return f"{self.width}x{self.height}"


@dataclass
class ImageMetadata:
    size: Dimension
    orientation: int


def get_image_metadata(path) -> ImageMetadata:
    raw_data = subprocess.check_output(
        ["identify", "-format", "%[EXIF:*]RESOLUTION=%G", path]
    ).decode("utf-8")
    grouped_data = {}
    for item in raw_data.split("\n"):
        key, value = item.split("=")
        grouped_data[key] = value

    return ImageMetadata(
        size=Dimension.parse(grouped_data["RESOLUTION"]),
        orientation=int(
            grouped_data.get("exif:Orientation", "1")
        ),  # Not all image filetypes have EXIF data
    )


def resize(args):
    image_data = {}
    for root, dirs, names in os.walk("."):
        for name in names:
            path = join(root, name)
            if path.startswith("./_site"):
                continue
            if is_og_image(name):
                image_metadata = get_image_metadata(path)
                thumbnail_name = get_thumbnail_name(name)
                thumbnail_path = join(root, thumbnail_name)
                thumbnail_exists = exists(thumbnail_path)

                # Check if the image is in need of auto rotation.
                # See https://jdhao.github.io/2019/07/31/image_rotation_exif_info/
                if image_metadata.orientation != 1:
                    print(
                        dedent(
                            f"""\
                            This image is in need of auto-orientation (exif:Orientation={image_metadata.orientation}): {path}

                            To fix this, try something like:

                                mogrify -auto-orient {path}
                                rm {thumbnail_path}  # In case a thumbnail already exists\
                            """
                        )
                    )
                    sys.exit(1)

                should_generate_thumbnail = None
                if not thumbnail_exists or args.force:
                    should_generate_thumbnail = True
                    if args.dry_run:
                        if thumbnail_exists:
                            print(
                                "Thumbnail already exists, but regenerating {}".format(
                                    thumbnail_path
                                )
                            )
                        else:
                            print(
                                "Generating nonexistent thumbnail {}".format(
                                    thumbnail_path
                                )
                            )
                else:
                    should_generate_thumbnail = False

                url = path[1::]
                image_data[url] = {
                    "size": str(image_metadata.size),
                }

                if should_generate_thumbnail and not args.dry_run:
                    print("Generating {} from {}".format(thumbnail_path, path))
                    subprocess.check_call(
                        ["convert", path, "-resize", "400x400>", thumbnail_path]
                    )

    with open("_data/images.yml", "w") as out:
        yaml.dump(image_data, out, default_flow_style=False)


def main():
    parser = argparse.ArgumentParser(description="Resize images")
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="perform a trial run with no changes made",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="force regenerating thumbnail images even if they alread exist",
    )
    args = parser.parse_args()

    resize(args)


if __name__ == "__main__":
    main()
