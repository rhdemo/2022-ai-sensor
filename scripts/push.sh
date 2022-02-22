#!/usr/bin/env bash
printf "\n\n######## admin-ui push ########\n"

IMAGE_REPOSITORY=${IMAGE_REPOSITORY:-quay.io/redhatdemo/2022-ai-sensor:latest}

echo "Pushing ${IMAGE_REPOSITORY}"
docker push ${IMAGE_REPOSITORY}

