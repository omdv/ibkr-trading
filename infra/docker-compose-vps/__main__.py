import config as cfg
import vps_setup
import dc_setup

config = cfg.read_config()
setup_vps = vps_setup.setup_vps(config)
setup_docker_compose = dc_setup.setup_docker_compose(config, setup_vps)
