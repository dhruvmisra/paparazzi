SHELL := /bin/bash

-include ./.env.development

start:
	@docker-compose up --force-recreate --remove-orphans

rebuild:
	@docker-compose build

local.install:
	@chmod +x ./scripts/init.sh
	@./scripts/init.sh

local.server:
	@source venv/bin/activate;
	@python src/run_uvicorn.py

format:
	@black ./src

build.server:
	@docker build -f docker/server/Dockerfile -t paparazzi-server:latest .

build.worker:
	@docker build -f docker/worker/Dockerfile -t paparazzi-worker:latest .

build.beat:
	@docker build -f docker/beat/Dockerfile -t paparazzi-beat:latest .

push.server:
	@docker tag paparazzi-server:latest $(DOCKER_REGISTRY)/paparazzi-server:latest
	@docker push $(DOCKER_REGISTRY)/paparazzi-server:latest

push.worker:
	@docker tag paparazzi-worker:latest $(DOCKER_REGISTRY)/paparazzi-worker:latest
	@docker push $(DOCKER_REGISTRY)/paparazzi-worker:latest

push.beat:
	@docker tag paparazzi-beat:latest $(DOCKER_REGISTRY)/paparazzi-beat:latest
	@docker push $(DOCKER_REGISTRY)/paparazzi-beat:latest

