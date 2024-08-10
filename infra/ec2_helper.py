"""
Helper for EC2 instance creation
"""
import pulumi_aws as aws

def create_ec2(config, docker_compose_content):
  """
  Main function
  """


  # Create an EC2 Key Pair with the public key
  key_pair = aws.ec2.KeyPair(
    "my-key-pair",
    public_key=config['public_key'],
    key_name="my-key-pair"
  )

  # Create a VPC
  vpc = aws.ec2.Vpc(
    "my-vpc",
    cidr_block="10.0.0.0/16",
    tags={
        "Name": "my-vpc",
    }
  )

  # Create a subnet within the VPC
  subnet = aws.ec2.Subnet(
    "my-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone=config['aws_availability_zone'],
    tags={
        "Name": "my-subnet",
    }
  )

  # Create a security group allowing SSH access only
  security_group = aws.ec2.SecurityGroup(
    'security-group',
    vpc_id=vpc.id,
    description='Allow SSH traffic',
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol='tcp',
            from_port=22,
            to_port=22,
            cidr_blocks=['0.0.0.0/0'],
        ),
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol='-1',  # All traffic
            from_port=0,
            to_port=0,
            cidr_blocks=['0.0.0.0/0'],
        ),
    ]
  )

  # Fetch the most recent Amazon Linux 2 AMI.
  ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["amazon"],
    filters=[{
        "name": "name",
        "values": ["amzn2-ami-hvm-*-x86_64-gp2"],
    }]
  )

  # Create an EC2 instance using the created security group and SSH key pair
  ec2_instance = aws.ec2.Instance(
    "ec2-instance",
    ami=ami.id,
    instance_type="t2.micro",
    security_groups=[security_group.id],
    subnet_id=subnet.id,
    key_name=key_pair.key_name,
  )

  return ec2_instance
