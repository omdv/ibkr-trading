# === SETUP ===
PROJECT := ibkr-trading
REPOSITORY := omdv/ibkr-trading
GATEWAY_VERSION := 978
APP_VERSION := v001

GATEWAY_IMAGE := docker.io/omdv/ib-gateway:$(GATEWAY_VERSION)
APP_IMAGE := gcr.io/ibkr-trading/ib-app:$(APP_VERSION)

# === DEVELOPMENT ===
.PHONY: test
test:
	docker-compose -f docker-compose.dev.yml up -d --build

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