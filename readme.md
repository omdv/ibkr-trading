# Interactive Brokers cloud deployment

This started as a development of IBKR trading application for cloud hosting. However during the development my objective changed towards being able to download real time option quotes for backtesting. So at the moment this repository includes the following:

1. Docker image for IBKR gateway with IBC. While there are several images none met my requirements for reliability and self-recovery. I included health tracking scripts and restart if gateway or IBC fails.

2. Docker image for the python application. Again, at the moment it is for downloading of the option quotes, but it has the right setup to create a trading application.

3. Terraform scripts to deploy two docker images to GCP on two standalone VMs with proper networking, firewalls, data persistence on GCS, etc.

## Usage

For local development create the following environment variables:

- `$TWS_TRADING_MODE` for trading mode. Allowed values are `paper` or `live`.
- `$TWS_USER_ID` and `$TWS_PASSWORD`.

### Local development / Testing

If you want to develop your own trading application or change the logic of my "quote downloader" you can use the gateway image, but will need to create your own application image.

My development flow involves deploying both images locally with docker-compose and use VSCode docker plugins to edit application script in the container.

Run `make test` to create a local docker compose deployment. Observe logs - the application should be able to connect to API and print out your account information.

### Building docker images for production

I will maintain two docker images:

- `docker.io/omdv/ib-gateway:latest` for gateway, you can use it as-is
- `docker.io/omdv/ib-downloader:latest`, downloading SPXW options every 30min

You will need to build and host your own image for trading logic instead of downloader. Depending on your preferences you may want to host that image on private registry, e.g. gcr.io.

Run `make publish-all` to create production docker images. You need to change image tags in Makefile first.

### Production deployment

The stack can be deployed using docker compose. Either one of `make dev` or `docker-compose up -d --build` will work.

For production I recommend to use server environment or one of cloud platforms. This repository has Terraform recipes for GCP.

It is based on two separate VMs hosting gateway and application containers, connected via VPC. Such separation allows to remove concerns around security by making gateway accessible only by trading application via internal network. Trading application is expected (at least at the moment) to be stateless with the hope to make it serverless in the future.

The downloaded option quotes are stored on GCS bucket.


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

Once deployed you should start seeing downloaded files in GCS bucket.

##### Troubleshooting / Usefull snippets

- Update container image by `gcloud compute instances update-container ib-app --container-image $TF_VAR_app_image`
<!-- - Forward VNC port: `gcloud compute ssh ib-gateway -- -v -L 8888:localhost:80`. -->
- Or connect to application instance and check docker logs.
- You cannot delete AppEngine once created, but you can import it into terraform plan: `terraform import google_app_engine_application.app $TF_VAR_project_id`
- If you already had GCP project import it: `terraform import google_project.project $TF_VAR_project_id`

## References

Inspired by the following projects:

- [IBC and TWS on ubuntu](https://dimon.ca/how-to-setup-ibc-and-tws-on-headless-ubuntu-in-10-minutes)
- [IBGateway docker image for GCP](https://github.com/dvasdekis/ib-gateway-docker-gcp)
