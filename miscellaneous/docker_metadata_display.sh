#!/bin/sh
#
# Shell script which displays Dockerfile information as well as the contents
# of the Dockerfile itself.
#
# Files with the image name, version number, and the source Dockerfile itself
# must be ADDed into the container during the build step.
# This is meant to be run from within the Docker container; it is recommended
# add the execution of this script to the CMD or ENTRYPOINT instructions.

# Name of the project
PROJECT=""

# URL to the location where the built image is located
IMAGE_HOST_LOCATION=""

# Path to the Dockerfile, inside the Docker container
DOCKERFILE_FILEPATH=""

# Path of a file containing the namespace of the Docker image,
# inside the Docker container
NAMESPACE_FILEPATH=""

# Path of a file containing the name of the Docker image,
# inside the Docker container
IMAGE_NAME_FILEPATH=""

# Path of a file containing the current version of the Docker image,
# inside the Docker container
VERSION_FILEPATH=""

NAMESPACE=$(cat ${NAMESPACE_FILEPATH})
IMAGE_NAME=$(cat ${IMAGE_NAME_FILEPATH})
VERSION=$(cat ${VERSION_FILEPATH})

echo \
  "______________________________________________________________\n" \
  "\n" \
  "Docker image of" ${PROJECT}".\n" \
  "\n" \
  "This image is hosted at" ${IMAGE_HOST_LOCATION}".\n" \
  "  Namespace: "${NAMESPACE}"\n" \
  "  Image name: "${IMAGE_NAME}"\n" \
  "  Version: "${VERSION}"\n" \
  "\n" \
  "The source Dockerfile is embedded in the image, and can be found by running"\
  "the following command:\n" \
  "\n" \
  "  $ docker run <image_name> cat "${DOCKERFILE_FILEPATH}" \n" \
  "\n" \
  "The contents of the Dockerfile are:\n"

echo "===========================\n"
cat ${DOCKERFILE_FILEPATH}
echo "===========================\n"

echo "\n" \
  "______________________________________________________________\n"
