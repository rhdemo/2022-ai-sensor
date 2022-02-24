#!/usr/bin/env bash
printf "\n\n######## ai-sensor deploy ########\n"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

PROJECT=${PROJECT:-ai-sensor}
oc project ${PROJECT} 2> /dev/null || oc new-project ${PROJECT}
oc project
echo "Deploying ${IMAGE_REPOSITORY}"

PARAMS="-p AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} -p AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}"
if [[ -n "${SECRET_NAME}" ]];then PARAMS="${PARAMS} -p SECRET_NAME=${SECRET_NAME}"; fi
if [[ -n "${AWS_S3_BUCKET}" ]];then PARAMS="${PARAMS} -p AWS_S3_BUCKET=${AWS_S3_BUCKET}"; fi
if [[ -n "${APPLICATION_NAME}" ]];then PARAMS="${PARAMS} -p APPLICATION_NAME=${APPLICATION_NAME}"; fi
if [[ -n "${REPLICAS}" ]];then PARAMS="${PARAMS} -p REPLICAS=${REPLICAS}"; fi
if [[ -n "${IMAGE_REPOSITORY}" ]];then PARAMS="${PARAMS} -p IMAGE_REPOSITORY=${IMAGE_REPOSITORY}"; fi
if [[ -n "${CONTAINER_REQUEST_CPU}" ]];then PARAMS="${PARAMS} -p CONTAINER_REQUEST_CPU=${CONTAINER_REQUEST_CPU}"; fi
if [[ -n "${CONTAINER_REQUEST_MEMORY}" ]];then PARAMS="${PARAMS} -p CONTAINER_REQUEST_MEMORY=${CONTAINER_REQUEST_MEMORY}"; fi
if [[ -n "${CONTAINER_LIMIT_CPU}" ]];then PARAMS="${PARAMS} -p CONTAINER_LIMIT_CPU=${CONTAINER_LIMIT_CPU}"; fi
if [[ -n "${CONTAINER_LIMIT_MEMORY}" ]];then PARAMS="${PARAMS} -p CONTAINER_LIMIT_MEMORY=${CONTAINER_LIMIT_MEMORY}"; fi

oc process -f "${DIR}/deployment.yml" ${PARAMS} | oc create -f -

