DEFAULT_ENV_FILE := .env
ifneq ("$(wildcard $(DEFAULT_ENV_FILE))","")
include ${DEFAULT_ENV_FILE}
export $(shell sed 's/=.*//' ${DEFAULT_ENV_FILE})
endif

ENV_FILE := .env.local
ifneq ("$(wildcard $(ENV_FILE))","")
include ${ENV_FILE}
export $(shell sed 's/=.*//' ${ENV_FILE})
endif


##################################

# DEV - run app locally for development

.PHONY: dev
dev:
	./scripts/dev.sh

##################################

# BUILD - build images locally using s2i

.PHONY: build
build:
	./scripts/build.sh

##################################

# PUSH - push images to repository

.PHONY: push
push:
	./scripts/push.sh

##################################

# DEPLOY - deploy application to OpenShift

.PHONY: deploy
deploy:
	./scripts/deploy.sh

##################################

# DEPLOY - deploy application to OpenShift

.PHONY: undeploy
undeploy:
	./scripts/undeploy.sh

##################################
