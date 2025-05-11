.ONESHELL:
SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -euc

DOCKER_IMAGE_TAG = 'ge-local'
PROJECT_DIR = 'ge'

##############################
# Docker
##############################
# build Docker image
.PHONY: docker/build
docker/build:
	@echo $@
	docker build -t $(DOCKER_IMAGE_TAG) .

# run Docker image mounting the current directory
.PHONY: docker/run
docker/run:
	@echo $@
	docker run -it --rm \
		--mount src="$$(pwd)",target=/workspaces,type=bind \
		--mount src="${HOME}/.config/gcloud",target=/root/.config/gcloud,type=bind \
		--workdir /workspaces/$(PROJECT_DIR) \
		--entrypoint /bin/bash \
		-p 8888:8888 \
		$(DOCKER_IMAGE_TAG)

.PHONY: docker/ge
docker/ge:
	@echo $@
	docker run -it --rm \
		--mount src="$$(pwd)",target=/workspaces,type=bind \
		--mount src="${HOME}/.config/gcloud",target=/root/.config/gcloud,type=bind \
		--workdir /workspaces/$(PROJECT_DIR) \
		-p 8888:8888 \
		$(DOCKER_IMAGE_TAG) \
		$(ARGS)

##############################
# Great Expectations
##############################
.PHONY: ge/version
ge/version:
	@echo $@
	$(MAKE) docker/ge ARGS='--version'

.PHONY: ge/test
ge/test:
	@echo $@
	$(MAKE) docker/ge ARGS='checkpoint run checkpoint_model'

.PHONY: ge/suite-edit
ge/suite-edit:
	@echo $@
	$(MAKE) docker/ge ARGS='suite edit dbt_example.my_first_dbt_model.warning -nj -m'

##############################
# Dev utilities
##############################
.PHONY: dev/lint
dev/lint:
	@echo $@
	docker run --rm -i ghcr.io/hadolint/hadolint < Dockerfile