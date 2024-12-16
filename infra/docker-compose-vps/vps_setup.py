"""
Helper for VPS setup
"""

from loguru import logger
import pulumi
import pulumi_command as command


def setup_vps(config):
  """
  Setup VPS by installing Docker Compose and other dependencies
  """
  # Create remote connection to execute commands
  logger.info(f"Connecting to {config['vps_ip_address']}")
  connection = command.remote.ConnectionArgs(
    host=config["vps_ip_address"],
    port=config["vps_ssh_port"],
    private_key=config["vps_ssh_private_key"],
    user=config["vps_ssh_user"],
  )

  logger.info("Updating apt")
  update_apt = command.remote.Command(
    "update-apt", connection=connection, create="sudo apt-get update -y"
  )

  logger.info("Installing Docker Compose")
  install_docker_compose = command.remote.Command(
    "install-docker-compose",
    connection=connection,
    create="\n".join(
      [
        # Add Docker's official GPG key
        "sudo apt-get update",
        "sudo apt-get install -y ca-certificates curl",
        "sudo install -m 0755 -d /etc/apt/keyrings",
        "sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc",
        "sudo chmod a+r /etc/apt/keyrings/docker.asc",
        # Add the repository to Apt sources
        'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null',
        "sudo apt-get update",
        # Install Docker and Docker Compose
        "sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin",
        # Add user to Docker group
        "sudo usermod -aG docker om",
      ]
    ),
    opts=pulumi.ResourceOptions(depends_on=[update_apt]),
  )

  logger.info("Restarting Docker")
  restart_docker = command.remote.Command(
    "restart-docker",
    connection=connection,
    create="sudo systemctl restart docker",
    opts=pulumi.ResourceOptions(
      depends_on=[
        install_docker_compose,
      ],
    ),
  )

  return restart_docker
