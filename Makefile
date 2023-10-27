# === SETUP ===
PROJECT := ibkr-trading
REPOSITORY := omdv/ibkr-trading

APP_FOLDER := ./app
APP_IMAGE := docker.io/omdv/ib-app:${IB_APP_VERSION}

# === DEVELOPMENT ===
.PHONY: test
test:
	docker-compose up -d --build

.PHONY: dev
dev: build-app
	docker-compose up -d

# === DOCKER ===
.PHONY: build-app
build-app:
	docker build -t $(APP_IMAGE) $(APP_FOLDER)

.PHONY: publish-app
publish-app: build-app
	docker push $(APP_IMAGE)

.PHONY: publish
publish: publish-app
