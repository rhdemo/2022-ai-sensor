#!/usr/bin/env bash
printf "\n\n######## ai-sensor deploy ########\n"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

PROJECT=${PROJECT:-ai-sensor}

oc project ${PROJECT} 2> /dev/null || oc new-project ${PROJECT}
oc project
echo "Deploying ${IMAGE_REPOSITORY}"

oc process -f "${DIR}/deployment.yml" | oc create -f -
