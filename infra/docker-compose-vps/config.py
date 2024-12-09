"""
Read config
"""

import os


def read_config():
  """
  Read config from config.json
  """
  config = {}
  config["vps_ip_address"] = os.environ.get("VPS_IP_ADDRESS")
  config["vps_ssh_port"] = int(os.environ.get("VPS_SSH_PORT"))
  config["vps_ssh_private_key"] = os.environ.get("VPS_SSH_PRIVATE_KEY")
  config["vps_ssh_user"] = os.environ.get("VPS_SSH_USER")

  config["gh_user"] = os.environ.get("GH_USER")
  config["gh_token"] = os.environ.get("GH_TOKEN")
  config["ibkr_user"] = os.environ.get("IBKR_USER")
  config["ibkr_password"] = os.environ.get("IBKR_PASSWORD")

  return config
