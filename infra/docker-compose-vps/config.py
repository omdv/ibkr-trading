"""
Read config
"""

import os


def read_config():
  """
  Read config from config.json
  """
  config = {}

  # vps connection config
  config["vps_ip_address"] = os.environ.get("VPS_IP_ADDRESS")
  config["vps_ssh_port"] = int(os.environ.get("VPS_SSH_PORT"))
  config["vps_ssh_private_key"] = os.environ.get("VPS_SSH_PRIVATE_KEY")
  config["vps_ssh_user"] = os.environ.get("VPS_SSH_USER")

  # docker compose config
  config["docker_compose_file"] = "docker-compose.yaml"
  config["remote_path"] = "/home/om/ibkr"

  # .env config
  config["ibkr_user"] = os.environ.get("LIVE_USER_ID")
  config["ibkr_password"] = os.environ.get("LIVE_PASSWORD")
  config["ib_trading_mode"] = os.environ.get("IB_TRADING_MODE")
  config["gh_user"] = os.environ.get("GH_USER")
  config["gh_token"] = os.environ.get("GH_TOKEN")
  config["ntfy_topic"] = os.environ.get("NTFY_TOPIC")
  config["ntfy_enabled"] = os.environ.get("NTFY_ENABLED")
  config["storage_path"] = "./data/ibkr_data.db"

  return config
