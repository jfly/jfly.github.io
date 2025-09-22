{
  lib,
  writers,
  python3Packages,
  imagemagick,
}:

writers.writePython3Bin "resize-images" {
  libraries = [ python3Packages.pyyaml ];
  # We already have project-wide lints for Python.
  doCheck = false;
  makeWrapperArgs = [
    "--prefix"
    "PATH"
    ":"
    "${lib.makeBinPath [ imagemagick ]}"
  ];
} (builtins.readFile ./resize_images.py)
