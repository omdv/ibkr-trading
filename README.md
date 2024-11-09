![ib-app-ver](https://img.shields.io/docker/v/omdv/ib-app?label=ib-app&logo=docker)
![ib-app-size](https://img.shields.io/docker/image-size/omdv/ib-app?label=ib-app&logo=docker)


# Interactive Brokers Application

Boilerplate to create your own trading application (bot) using Interactive Brokers gateway. Trading application involves two services:

1. Image for IBKR gateway with IBC. I stopped maintaining my own version and instead recommend using the `stable` version from [extrange](https://github.com/extrange/ibkr-docker)

2. Image for the python application using `ib_async` library, which supports scheduling.


This repo provides several ways to deploy the application:
- docker-compose, which is recommended for local development
- terraform for deploying on GCP IaaS using VMs
- helm chart for deploying on Kubernetes cluster (local or PaaS)
- (WIP) terraform for deploying on OCI using k8s

# Usage

## Local development

Add your variables to `.envrc` and then `direnv allow`. Running `task evd-up` will start TWS gateway locally in paper mode.

Running `python app/main.py` will start the trading application.


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
