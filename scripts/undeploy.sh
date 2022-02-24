#!/usr/bin/env bash
printf "\n\n######## ai-sensor deploy ########\n"
set -x

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

PROJECT=${PROJECT:-ai-sensor}
oc project ${PROJECT} 2> /dev/null || oc new-project ${PROJECT}
oc project
echo "Deploying ${IMAGE_REPOSITORY}"
PARAMS="-p AWS_ACCESS_KEY_ID=dontcare -p AWS_SECRET_ACCESS_KEY=dontcare"

oc process -f "${DIR}/deployment.yml" ${PARAMS} | oc delete -f -

