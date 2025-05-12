#!/bin/bash
# Builds and optionally pushes a new version of a docker image
set -e

# ref: https://stackoverflow.com/a/4774063/3211029
HERE="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
APP_ROOT="$(dirname "$HERE")"

PUSH_IMAGE=false

function usage {
  echo "Usage: $0 [-h] [-p] image tag dockerfile"
  echo "  -h              Show this help message"
  echo "  -p              Push the image after building"
  echo "  image           Name of the image to build"
  echo "  tag             Tag of the image to build"
  echo "  dockerfile      Path to the Dockerfile to build"
}

# Parse arguments and options regardless its position
# Ref: https://stackoverflow.com/a/63421397/3211029
args=()
while [ $OPTIND -le "$#" ]
do
  if getopts "hp" flag
  then
    case $flag in
      h)
        usage
        exit 0
        ;;
      p)
        PUSH_IMAGE=true
        ;;
    esac
  else
    args+=("${!OPTIND}")
    ((OPTIND++))
  fi
done

# Read positional arguments
IMAGE_NAME="${args[0]}"
IMAGE_TAG="${args[1]}"
DOCKERFILE="${args[2]}"

# Validate image name is provided
if [ -z "$IMAGE_NAME" ]; then
  echo "Error: image name is required" >&2
  exit 1
fi

# Validate image tag is provided
if [ -z "$IMAGE_TAG" ]; then
  echo "Error: image tag is required" >&2
  exit 1
fi

# Validate dockerfile is provided
if [ -z "$DOCKERFILE" ]; then
  echo "Error: dockerfile is required" >&2
  exit 1
fi

# Validate dockerfile existense
if [ ! -f "$DOCKERFILE" ]; then
  echo "Error: dockerfile does not exist" >&2
  exit 1
fi


echo "Building image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo "    Dockerfile: ${DOCKERFILE}"
echo "    Push image: ${PUSH_IMAGE}"
echo

if [ "$PUSH_IMAGE" = true ]; then

  # Multi arch build and push
  docker buildx build                   \
    --platform linux/amd64,linux/arm64  \
    -t "${IMAGE_NAME}":"${IMAGE_TAG}"   \
    -f "${DOCKERFILE}"                  \
    --push                              \
    "${APP_ROOT}"

  echo
  echo "Image build and released to docker registry: ${IMAGE_NAME}:${IMAGE_TAG}"
else

  # Local build (No push to container registry and no multi-arch support)
  docker build                         \
    -t "${IMAGE_NAME}":"${IMAGE_TAG}"  \
    -f "${DOCKERFILE}"                 \
    "${APP_ROOT}"

  echo
  echo "Image build and ready for local usage: ${IMAGE_NAME}:${IMAGE_TAG}"
fi
