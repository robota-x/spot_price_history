import boto3
import json
import os

from configparser import ConfigParser

config = None


def setup():
    global config
    if config is None:
        current_env = os.environ.get('ENV', 'live')
        config_parser = ConfigParser()
        config_parser.read('config.ini')
        config = config_parser[current_env]

    if 'aws_profile' in config:
        boto3.setup_default_session(profile_name=config['aws_profile'])


def get_availability_zones(region_name):
    res = boto3.client('ec2', region_name=region_name).describe_availability_zones()

    return [zone.get('ZoneName') for zone in res.get('AvailabilityZones', [])]


def load_required_metrics():
    obj_body = boto3 \
        .client('s3') \
        .get_object(
            Bucket=config['requirements_s3_bucket'],
            Key=config['requirements_s3_key'],
        )['Body']

    requirements = json.loads(obj_body.read().decode('utf-8'))
    availability_zones = [zone for region in requirements.get('regions') for zone in get_availability_zones(region)]

    return {
        'regions': requirements.get('regions'),
        'instance_types': requirements.get('instance_types'),
        'availability_zones': availability_zones
    }


# still debug
def main():
    setup()
    required_metrics = load_required_metrics()

 
    print(required_metrics)


main()
