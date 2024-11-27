![ib-trading-app-ver](https://img.shields.io/docker/v/omdv/ib-trading-app?label=ib-trading-app&logo=docker)
![ib-trading-app-size](https://img.shields.io/docker/image-size/omdv/ib-trading-app?label=ib-trading-app&logo=docker)


# Description

This is the boilerplate or framework to create your own trading application with Interactive Brokers. It is **not** a finished product - the provided example will work end-to-end, but you are expected to add your own trading logic and workflow. This said, I do use it for my own trading and will continue adding some key elements, without exposing my own algorithm.

The **systematic** approach to trading requires your trading application to have several services. I designed this framework to be modular, loosely coupled and containerized:

1. You will need the IBKR gateway to provide the API. [IBC](https://github.com/IbcAlpha/IBC) emerged as the default way to manage the IBKR gateway. Still, this setup is finicky, especially when containerized. After many months I stopped maintaining my own docker image and recommend using the image from [extrange](https://github.com/extrange/ibkr-docker), which is quite stable, as long as you include health checks to ensure it restarts on failure and use right settings to restart if you miss the MFA window.

2. The main "know-how" - the image of the trading application itself. I use `ib_async` library with scheduler. You can see the example of the end-to-end implementation in `app` folder. You will need to modify it and add github workflow to build your custom image.

3. Storage and messaging backends. I recommend using `ntfy.sh` service, which is free and nothing short of amazing. Just make sure you select an obfuscated name for your topic.

4. Backtesting backend. You need to track the performance of your strategy and compare it with the *theoretical* performance. I developed my own backend for backtesting options strategy, using duckdb, sql and arrows, instead of pandas for significant performance boost. I will try to open portions of my backtest repo in the future.


# Tech stack
- `devenv` and `poetry` for reproducible dev environment
- `duckdb` for storage and analytics
- `docker-compose` or `helm chart` for deployment
- `pulumi` or `terraform` for infrastructure-as-a-code

# Usage

Utility will be limited, unless you build your own trading application. This said below are some general notes on deployment and usage.

### Local development

Local deployment is using docker-compose. Add your variables to `.envrc`, `direnv allow`. Running `task evd-up` will start TWS gateway locally. `python app/main.py` will start the trading application. There is a mock class available to mock the `IB` API.


### AWS deployment

My preferred way to run it is with docker-compose on a single EC2 instance. I use `pulumi` for IaaC. Instructions to be added...


### Helm chart deployment

There is a helm chart, if you prefer k8s.

```bash
helm repo add ibkr-trading https://omdv.github.io/ibkr-trading/
helm search repo ibkr-trading
```
OCI has a very generous free tier and I was successful deploying this chart within it, however it proved to be too much hassle. Chart will be supported, but not updated frequently.


### GCP deployment with Terraform

My first deployment outside of local was on GCP with Terraform. It was based on two separate VMs hosting gateway and application containers, connected via VPC.

I will **not support** this moving forward.

Expected env variables:
```bash
export TF_VAR_TWS_USER_ID = <your-TWS-login>
export TF_VAR_TWS_PASSWORD = <your-TWS-pass>
export TF_VAR_TRADING_MODE = <"paper" or "live">
export TF_VAR_project_id = <your-GCP-project-id>
```

Review and deploy:

```bash
cd ./deployments/google
terraform init
terraform plan
terraform apply
```


## Troubleshooting / Usefull snippets

- Update container image by `gcloud compute instances update-container ib-app --container-image $TF_VAR_app_image`
- Or connect to application instance and check docker logs.
- If you already had GCP project import it: `terraform import google_project.project $TF_VAR_project_id`


# References

Inspired by the following projects:

- [IBC and TWS on ubuntu](https://dimon.ca/how-to-setup-ibc-and-tws-on-headless-ubuntu-in-10-minutes)
- [IBGateway docker image for GCP](https://github.com/dvasdekis/ib-gateway-docker-gcp)
- [Systematic trading](https://www.amazon.com/Systematic-Trading-designing-trading-investing/dp/0857194453)
