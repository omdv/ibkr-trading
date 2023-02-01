![ib-gateway-ver](https://img.shields.io/docker/v/omdv/ib-gateway?label=ib-gateway&logo=docker)
![ib-gateway-size](https://img.shields.io/docker/image-size/omdv/ib-gateway?label=ib-gateway&logo=docker)
![ib-app-ver](https://img.shields.io/docker/v/omdv/ib-app?label=ib-app&logo=docker)
![ib-app-size](https://img.shields.io/docker/image-size/omdv/ib-app?label=ib-app&logo=docker)


# Interactive Brokers Application

Boilerplate or framework to create your own trading application or bot using Interactive Brokers gateway. At the basic level this repo hosts images for two docker containers:

1. Docker image for IBKR gateway with IBC. While there are several images none met my requirements for reliability and self-recovery.

2. Docker image for the python application using `ib_insync` library, which supports scheduling and can be used for trading bot.

You can use these images as-is. In addition I provide several ways to deploy the application:
- docker-compose, which can be good for local development and hosting
- terraform for deploying on GCP IaaS (VMs)
- helm chart for deploying on Kubernetes cluster (local or PaaS)

# Usage

## Standalone Docker

The `docker.io/omdv/ib-gateway` container expects three variables:
- `$TRADING_MODE`: `paper` or `live`.
- `$TWSUSERID`
- `$TWSPASSWORD`

Available tags:
| Tag | Gateway version |
| --- | ----: |
| 1019 | 10.19 |
| 1012 | 10.12 |
| 981.3c | 981 |

## Docker-compose deployment

Add your variables to `.env`. Then run `make dev`, which will start `docker-compose`.

## Helm chart deployment

Add repo and find the latest version.

```bash
helm repo add ibkr-trading https://omdv.github.io/ibkr-trading/
helm search repo ibkr-trading
```

## GCP deployment

This repository has Terraform recipes for GCP. It is based on two separate VMs hosting gateway and application containers, connected via VPC. Such separation allows to remove concerns around security by making gateway accessible only by trading application via internal network. Trading application is expected (at least at the moment) to be stateless with the hope to make it serverless in the future.

To deploy you will need to expose the following env variables or enter them in console during terraform application:

```bash
export TF_VAR_TWS_USER_ID = <your-TWS-login>
export TF_VAR_TWS_PASSWORD = <your-TWS-pass>
export TF_VAR_TRADING_MODE = <"paper" or "live">
export TF_VAR_project_id = <your-GCP-project-id>
```

Review and deploy Terraform plan:

```bash
cd ./deployments/google
terraform init
terraform plan
terraform apply
```

# Development

## Dependencies

Some recommended dependencies for pre-commit hooks.
- `pre-commit`
- `ripsecrets`

## Troubleshooting / Usefull snippets

- Update container image by `gcloud compute instances update-container ib-app --container-image $TF_VAR_app_image`
- Or connect to application instance and check docker logs.
- If you already had GCP project import it: `terraform import google_project.project $TF_VAR_project_id`


# References

Inspired by the following projects:

- [IBC and TWS on ubuntu](https://dimon.ca/how-to-setup-ibc-and-tws-on-headless-ubuntu-in-10-minutes)
- [IBGateway docker image for GCP](https://github.com/dvasdekis/ib-gateway-docker-gcp)
