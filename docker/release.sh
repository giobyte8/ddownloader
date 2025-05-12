#!/bin/bash
# Builds and optionally pushes a new version of docker image
set -e

# Scripts path
# ref: https://stackoverflow.com/a/4774063/3211029
HERE="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
BUILD_SCRIPT="build_image.sh"
DOCKERFILE="ddownloader.dockerfile"

IMAGE_NAME=giobyte8/ddownloader
IMAGE_TAG=dev
PUSH_IMAGE=false

function usage {
  echo "Usage: $0 [-t tag] [-p]"
  echo "  -h        Display this help message"
  echo "  -t tag    Tag of the image to build"
  echo "            Default tag: dev"
  echo "  -p        Push the image after building"
}

# Simple and easy args parsing
# Ref: https://stackoverflow.com/a/21535142/3211029
while [ "`echo $1 | cut -c1`" = "-" ]
do
    case "$1" in
        -h)
          usage
          exit 0
          ;;
        -p)
          PUSH_IMAGE=true
          shift 1
          ;;
        -t)
          IMAGE_TAG=$2
          shift 2
          ;;
        *)
          usage
          exit 1
          ;;
esac
done

# Use absolute paths in case that script is executed from other path
if [ ! -f "$BUILD_SCRIPT" ]; then
    BUILD_SCRIPT="${HERE}/${BUILD_SCRIPT}"
    DOCKERFILE="${HERE}/${DOCKERFILE}"

    echo "Build script: $BUILD_SCRIPT"
    echo "Dockerfile: $DOCKERFILE"
    echo
fi

# Build image by invoking .build_image.sh script
if [ "$PUSH_IMAGE" = true ]; then
  . "$BUILD_SCRIPT" -p "$IMAGE_NAME" "$IMAGE_TAG" "$DOCKERFILE"
else
  . "$BUILD_SCRIPT" "$IMAGE_NAME" "$IMAGE_TAG" "$DOCKERFILE"
fi
