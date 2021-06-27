# === SETUP ===
PROJECT := ibkr-trading
REPOSITORY := omdv/ibkr-trading

GATEWAY_FOLDER := ./gateway
GATEWAY_IMAGE := docker.io/omdv/ib-gateway:latest
APP_IMAGE := docker.io/omdv/ib-downloader:latest
APP_FOLDER := ./downloader

# === DEVELOPMENT ===
.PHONY: test
test:
	docker-compose up -d

.PHONY: dev
dev:
	docker-compose up -d --build

# === DOCKER ===
.PHONY: build-gateway
build-gateway:
	docker build -t $(GATEWAY_IMAGE) $(GATEWAY_FOLDER)

.PHONY: publish-gateway
publish-gateway:
	docker push $(GATEWAY_IMAGE)

.PHONY: build-app-test
build-app:
	docker build -t $(APP_IMAGE) $(APP_FOLDER)

.PHONY: publish-app-test
publish-app:
	docker push $(APP_IMAGE)
	
.PHONY: publish-all
publish-all: build-gateway publish-gateway build-app publish-app

# === DEPLOYMENTS ===