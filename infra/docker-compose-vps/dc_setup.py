import pulumi
import pulumi_command as command
from loguru import logger


def setup_docker_compose(config, setup_vps):
  # Create remote connection to execute commands
  logger.info(f"Connecting to {config['vps_ip_address']}")
  connection = command.remote.ConnectionArgs(
    host=config["vps_ip_address"],
    port=config["vps_ssh_port"],
    private_key=config["vps_ssh_private_key"],
    user=config["vps_ssh_user"],
  )

  # Create ibkr directory
  logger.info("Creating ibkr directory")
  create_ibkr_dir = command.remote.Command(
    "create-ibkr-dir",
    connection=connection,
    create=f"mkdir -p {config['remote_path']}",
    opts=pulumi.ResourceOptions(depends_on=[setup_vps]),
  )

  # Create .env file
  logger.info("Creating .env file")
  docker_env_vars = {
    "GH_USER": config["gh_user"],
    "GH_TOKEN": config["gh_token"],
    "IBKR_USER": config["ibkr_user"],
    "IBKR_PASSWORD": config["ibkr_password"],
    "IB_TRADING_MODE": config["ib_trading_mode"],
    "NTFY_TOPIC": config["ntfy_topic"],
    "NTFY_ENABLED": config["ntfy_enabled"],
    "STORAGE_PATH": config["storage_path"],
  }
  env_file_content = "\n".join(
    [f"{k}={v}" for k, v in docker_env_vars.items() if v is not None]
  )
  copy_env_file = command.remote.Command(
    "copy-env-file",
    connection=connection,
    create=f'echo "{env_file_content}" > {config["remote_path"]}/.env',
    opts=pulumi.ResourceOptions(depends_on=[create_ibkr_dir]),
  )

  # Send docker compose file
  logger.info("Sending docker compose file")
  copy_docker_compose = command.remote.CopyToRemote(
    "copy-docker-compose",
    connection=connection,
    source=pulumi.FileAsset(f"{config['docker_compose_file']}"),
    remote_path=f"{config['remote_path']}/{config['docker_compose_file']}",
    opts=pulumi.ResourceOptions(depends_on=[copy_env_file]),
  )

  # Login to GitHub Container Registry
  logger.info("Logging into GitHub Container Registry")
  ghcr_login = command.remote.Command(
    "ghcr-login",
    connection=connection,
    create=f'echo "{config["gh_token"]}" | docker login ghcr.io -u {config["gh_user"]} --password-stdin',
    opts=pulumi.ResourceOptions(depends_on=[setup_vps]),
  )

  # Start Docker Compose
  logger.info("Starting Docker Compose")
  start_docker_compose = command.remote.Command(
    "start-docker-compose",
    connection=connection,
    create=f"cd {config['remote_path']} && docker compose up -d",
    opts=pulumi.ResourceOptions(
      depends_on=[setup_vps, copy_docker_compose, copy_env_file, ghcr_login]
    ),
  )

  return start_docker_compose
