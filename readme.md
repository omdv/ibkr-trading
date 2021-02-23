# Interactive Brokers trading application

## Usage

Create the following environment variables:

- `$TWS_VNC_PASSWORD` with the password for VNC login. Leave blank for no password.
- `$TWS_TRADING_MODE` for trading mode. Allowed values are `paper` or `live`.
- `$TWS_USER_ID` and `$TWS_PASSWORD`.

### Local development / Testing

Run `make test` to create a local docker compose deployment. Observe logs - the application should be able to connect to API and print out your account information.

Access VNC via `http://[your-docker-host-ip]:8888` and API via `[your-docker-host-ip]:4000`.

### Cloud development

You can use one of official Jupyter notebook images:

```bash
export TF_VAR_app_image=docker.io/jupyter/minimal-notebook:latest
```

Note that it won't have persistent storage, so commit your changes before destroying the instance.

### Building docker images for production

I will maintain two docker images:

- `docker.io/omdv/ib-gateway:latest` for gateway
- `docker.io/omdv/ib-app:test` for application

You will need to build and host your own image for trading logic instead of test application. Depending on your preferences you may want to host that image on private registry, e.g. gcr.io.

Run `make publish-all` to create production docker images. Define image tags in Makefile.

### Deployments

The stack can be deployed using docker compose. Either one of `make dev` or `docker-compose up -d --build` will work.

For production I recommend to use server environment or one of cloud platforms. This repository has Terraform recipes for some of cloud platforms.

All production deployments are based on two separate VMs hosting gateway and application containers, connected via VPC. Such separation allows to remove concerns around security by making gateway accessible only by trading application via internal network. Trading application is expected (at least at the moment) to be stateless with the hope to make it serverless in the future. If required, however, I may look at adding persistence in the future.

#### Google Cloud Platform

At a minimum expose the following variables:

```bash
export TF_VAR_TWS_USER_ID = <your-TWS-login>
export TF_VAR_TWS_PASSWORD = <your-TWS-pass>
export TF_VAR_TRADING_MODE = <"paper" or "live">
export TF_VAR_VNC_PASSWORD = <pass to access VNC, can leave blank, it is not exposed by default>
export TF_VAR_project_id = <your-GCP-project-id>
```

If you don't want to see default test application pick your desired image: `export TF_VAR_app_image=...`

Review and deploy Terraform plan:

```bash
cd ./deployments/google
terraform init
terraform plan
terraform apply
```

Once deployed in a few minutes you should start seeing entities in Firestore.

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
