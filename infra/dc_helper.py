"""
Configure docker-compose
"""

import io
from ruamel.yaml import YAML


def get_docker_compose(config):
  """
  Read and parameterize docker compose file
  """

  yaml = YAML()
  with open("docker-compose-prod.yaml", "r", encoding="utf-8") as file:
    data = yaml.load(file)

  # Replace the value
  data["services"]["ib-gateway"]["image"] = config["gateway_image"]
  data["services"]["ib-app"]["image"] = config["app_image"]

  # Write the updated data back to the file
  with open("docker-compose-prod.yaml", "w", encoding="utf-8") as file:
    yaml.dump(data, file)

  string_stream = io.StringIO()
  yaml.dump(data, string_stream)
  return string_stream.getvalue()
