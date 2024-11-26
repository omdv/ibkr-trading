"""
Read config
"""

import os


def read_config():
  """
  Read config from config.json
  """
  config = {}
  config["aws_region"] = os.environ.get("AWS_REGION")
  config["aws_availability_zone"] = os.environ.get("AWS_AVAILABILITY_ZONE")
  config["public_key"] = os.environ.get("MY_PUBLIC_KEY")
  config["gateway_image"] = os.environ.get("GATEWAY_IMAGE")
  config["app_image"] = os.environ.get("APP_IMAGE")

  return config
