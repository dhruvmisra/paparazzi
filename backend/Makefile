SHELL := /bin/bash

-include ./.env.development

services:
	@docker-compose up worker scheduler localstack --force-recreate --remove-orphans

start:
	@docker-compose up --force-recreate --remove-orphans

watch:
	@docker-compose watch --no-up & docker-compose up worker scheduler localstack --force-recreate --remove-orphans

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

aws.login:
	@aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 402963518398.dkr.ecr.us-east-1.amazonaws.com

push.server:
	@docker tag paparazzi-server:latest 402963518398.dkr.ecr.us-east-1.amazonaws.com/paparazzi-backend:latest
	@docker push 402963518398.dkr.ecr.us-east-1.amazonaws.com/paparazzi-backend:latest

push.worker:
	@docker tag paparazzi-worker:latest 402963518398.dkr.ecr.us-east-1.amazonaws.com/paparazzi-worker:latest
	@docker push 402963518398.dkr.ecr.us-east-1.amazonaws.com/paparazzi-worker:latest

push.beat:
	@docker tag paparazzi-beat:latest 402963518398.dkr.ecr.us-east-1.amazonaws.com/paparazzi-scheduler:latest
	@docker push 402963518398.dkr.ecr.us-east-1.amazonaws.com/paparazzi-scheduler:latest

build-and-push-all:
	@make build.server
	@make build.worker
	@make build.beat
	@make push.server
	@make push.worker
	@make push.beat
