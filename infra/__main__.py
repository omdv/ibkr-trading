"""
Main pulumi module
"""

import pulumi
import pulumi_aws as aws

import ec2_helper as ec2h
import config as cfg
import dc_helper as dch

config = cfg.read_config()

aws.config.region = config['aws_region']

dc = dch.get_docker_compose(config)
instance = ec2h.create_ec2(config, dc)

pulumi.export("config", config)
pulumi.export("instance_id", instance.id)
pulumi.export("instance_ip", instance.public_ip)
pulumi.export("instance_public_dns", instance.public_dns)
