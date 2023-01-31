# === SETUP ===
include .env
PROJECT := ibkr-trading
REPOSITORY := omdv/ibkr-trading

GATEWAY_FOLDER := ./gateway
GATEWAY_IMAGE := docker.io/omdv/ib-gateway:${IB_GATEWAY_VERSION}

APP_FOLDER := ./app
APP_IMAGE := docker.io/omdv/ib-app:${IB_APP_VERSION}

# === DEVELOPMENT ===
.PHONY: test
test:
	docker-compose up -d --build

.PHONY: dev
dev: build-gateway build-app
	docker-compose up -d

# === DOCKER ===
.PHONY: build-gateway
build-gateway:
	docker build -t $(GATEWAY_IMAGE) $(GATEWAY_FOLDER) --build-arg IBC_VERSION=${IBC_VERSION} --build-arg IB_GATEWAY_VERSION=${IB_GATEWAY_VERSION}

.PHONY: build-app
build-app:
	docker build -t $(APP_IMAGE) $(APP_FOLDER)

.PHONY: publish-gateway
publish-gateway: build-gateway
	docker push $(GATEWAY_IMAGE)

.PHONY: publish-app
publish-app: build-app
	docker push $(APP_IMAGE)

.PHONY: publish
publish: publish-gateway publish-app
