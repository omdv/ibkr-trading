from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  """
  Read server settings
  """

  ib_gateway_host: str
  ib_gateway_port: str
  timezone: str = "US/Eastern"
  timeformat: str = "%Y-%m-%dT%H%M"
  storage: str = "file"
  storage_path: str
  close_spread_on_expiry: bool = False
  ntfy_topic: str
  ntfy_enabled: bool
