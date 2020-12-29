# Interactive Brokers trading application

## Usage

Update `.env` file if needed. Create the following environment variables:

- $TWS_VNC_PASSWORD
- $TWS_TRADING_MODE
- $TWS_USER_ID
- $TWS_PASSWORD

### Ports

`dc -f docker-compose.ports.yml up -d --build`
VNC via `docker-host:8888`, API via `docker-host:4000`

### Tailscale

`dc -f docker-compose.tailscale.yml up -d --build`
Enable magic DNS in tailscale console and setup one DNS server, e.g. 8.8.8.8. VNC via `tailscale-IP:80`, API via `tailscale-IP:4000`

## References

- [Tailscale and docker](https://rnorth.org/tailscale-docker/)
- [IBC and TWS on ubuntu](https://dimon.ca/how-to-setup-ibc-and-tws-on-headless-ubuntu-in-10-minutes)
