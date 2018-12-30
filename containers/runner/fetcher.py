import boto3
import json
import os

from configparser import ConfigParser
from datetime import datetime, timedelta

config = None


def setup():
    global config
    if config is None:
        current_env = os.environ.get('ENV', 'live')
        config_parser = ConfigParser()
        config_parser.read('config.ini')
        config = config_parser[current_env]

    # live permission are expected through an attached role rather than auth
    if 'aws_profile' in config:  
        boto3.setup_default_session(profile_name=config['aws_profile'])

def get_availability_zones(client):
    res = client.describe_availability_zones()

    return [zone.get('ZoneName') for zone in res.get('AvailabilityZones', [])]


def load_required_metrics():
    obj_body = boto3 \
        .client('s3') \
        .get_object(
            Bucket=config['requirements_s3_bucket'],
            Key=config['requirements_s3_key'],
        )['Body']

    requirements = json.loads(obj_body.read().decode('utf-8'))

    return {
        'regions': requirements.get('regions'),
        'instance_types': requirements.get('instance_types'),
    }


def fetch_zone_spot_prices(client, availability_zone, instance_types, end_time, start_time, product_description):
    res = client.describe_spot_price_history(
        AvailabilityZone=availability_zone,
        InstanceTypes=instance_types,
        EndTime=end_time,
        StartTime=start_time,
        ProductDescriptions=product_description,
    )

    return res.get('SpotPriceHistory', [])


def collate_data(required_metrics, end_time=None, start_time=None):
    computed_end_time = end_time or datetime.now()
    computed_start_time = start_time or (computed_end_time - timedelta(seconds=3610))
    product_description = ['Linux/UNIX', 'Windows']

    spot_prices = []

    for region in required_metrics['regions']:
        client = boto3.client('ec2', region_name=region)

        availability_zones = get_availability_zones(client)

        for zone in availability_zones:
            zone_prices = fetch_zone_spot_prices(
                client=client,
                availability_zone=zone,
                instance_types=required_metrics['instance_types'],
                end_time=computed_end_time,
                start_time=computed_start_time,
                product_description=product_description
            )

            print(f'fetched {len(zone_prices)} prices for zone: {zone}')
            spot_prices += zone_prices

    print(f'fetched {len(spot_prices)} prices for {len(required_metrics["regions"])} regions')
    return spot_prices


def get_spot_prices():
    setup()

    required_metrics = load_required_metrics()
    return collate_data(required_metrics)