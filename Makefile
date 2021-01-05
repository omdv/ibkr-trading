# === SETUP ===
PROJECT := ibkr-trading
REPOSITORY := omdv/ibkr-trading

GATEWAY_IMAGE := docker.io/omdv/ib-gateway:latest
APP_IMAGE := docker.io/omdv/ib-app:test

# === DEVELOPMENT ===
.PHONY: test
test:
	docker-compose up -d --build

.PHONY: dev
dev:
	docker-compose up -d --build

# === DOCKER ===
.PHONY: build-gateway
build-gateway:
	docker build -t $(GATEWAY_IMAGE) ./gateway/

.PHONY: publish-gateway
publish-gateway:
	docker push $(GATEWAY_IMAGE)

.PHONY: build-app
build-app:
	docker build -t $(APP_IMAGE) ./application

.PHONY: publish-app
publish-app:
	docker push $(APP_IMAGE)
	
.PHONY: publish-all
publish-all: build-gateway publish-gateway build-app publish-app

# === DEPLOYMENTS ===