#!/usr/bin/env bash
printf "\n\n######## ai-sensor local build ########\n"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

IMAGE_REPOSITORY=${IMAGE_REPOSITORY:-quay.io/redhatdemo/2022-ai-sensor:latest}
SOURCE_REPOSITORY_URL=${SOURCE_REPOSITORY_URL:-https://github.com/rhdemo/2022-ai-sensor.git}
SOURCE_REPOSITORY_REF=${SOURCE_REPOSITORY_REF:-master}
SOURCE_CONTEXT_DIR=${SOURCE_CONTEXT_DIR:-.}

echo "Building ${IMAGE_REPOSITORY} from ${SOURCE_REPOSITORY_URL} on ${SOURCE_REPOSITORY_REF}"

s2i build ${SOURCE_REPOSITORY_URL} --ref ${SOURCE_REPOSITORY_REF} --context-dir ${SOURCE_CONTEXT_DIR} registry.access.redhat.com/ubi8/python-39:latest ${IMAGE_REPOSITORY}
