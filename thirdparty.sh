#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

wget https://github.com/dimsemenov/PhotoSwipe/archive/master.zip -O /tmp/photoswipe.zip
unzip /tmp/photoswipe.zip 'PhotoSwipe-master/dist/*' -d /tmp/photoswipe
mv /tmp/photoswipe/PhotoSwipe-master/dist/ public/photoswipe
