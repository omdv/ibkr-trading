# Interactive Brokers trading application

## Usage

Create the following environment variables:

- `$TWS_VNC_PASSWORD` with the password for VNC login. Leave blank for no password.
- `$TWS_TRADING_MODE` for trading mode. Allowed values are `paper` or `live`.
- `$TWS_USER_ID` and `$TWS_PASSWORD`.

### Local test

Run `make test` to create a local docker compose deployment. Observe logs - the application should be able to connect to API and print out your account information.

Access VNC via `http://[your-docker-host-ip]:8888` and API via `[your-docker-host-ip]:4000`.

### Building docker images for production

Run `make publish-all` to create production docker images. Define image tags in Makefile.

### Tailscale

*Will likely abandon in favor of SSH port forwarding.*

`dc -f docker-compose.tailscale.yml up -d --build`
Enable magic DNS in tailscale console and setup one DNS server, e.g. 8.8.8.8. VNC via `tailscale-IP:80`, API via `tailscale-IP:4000`

### Cloud deployments

WIP on Terraform recipes for:

- GCP (90% done)
- AWS (not started)
- Digital Ocean (not started)

## References

- [Tailscale and docker](https://rnorth.org/tailscale-docker/)
- [IBC and TWS on ubuntu](https://dimon.ca/how-to-setup-ibc-and-tws-on-headless-ubuntu-in-10-minutes)
