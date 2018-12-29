import base64
import boto3
import configparser
import json
import traceback

from datetime import datetime, timedelta
from dateutil.parser import parse
from msg_pb2 import Result


config = configparser.ConfigParser()
config.read('config.ini')


def serialise_prices(spot_prices):
    msg = Result()

    for datapoint in spot_prices:
        price = msg.spotprices.add()

        price.time = datapoint['Timestamp'].isoformat() if 'Timestamp' in datapoint else None
        price.price = float(datapoint['SpotPrice']) if 'SpotPrice' in datapoint else None
        price.zone = datapoint.get('AvailabilityZone')
        price.type = datapoint.get('InstanceType')
        price.product = datapoint.get('ProductDescription')

    return msg.SerializeToString()


def get_availability_zones(client, region_name):
    res = client.describe_availability_zones()

    return [zone.get('ZoneName') for zone in res.get('AvailabilityZones', [])]


def get_region_spot_prices(region, instance_types, end_time=None, start_time=None):
    client = boto3.client('ec2', region_name=region)
    availability_zones = get_availability_zones(client, region)

    computed_end_time = end_time or datetime.now()
    computed_start_time = start_time or (computed_end_time - timedelta(seconds=3610))

    spot_prices = []
    # not using filters as they seem to be quite flaky results
    for zone in availability_zones:
        res = client.describe_spot_price_history(
            AvailabilityZone=zone,
            InstanceTypes=instance_types,
            EndTime=computed_end_time,
            StartTime=computed_start_time,
            ProductDescriptions=['Linux/UNIX', 'Windows'],
        )
        zone_prices = res.get('SpotPriceHistory', [])

        print(f'fetched {len(zone_prices)} prices for zone: {zone}')
        spot_prices += zone_prices

    return spot_prices


def lambda_handler(event, context):
    region = event.get('region', 'eu-west-1')
    instance_types = event.get('instance_types', ['t1.micro'])

    end_time = parse(event['end_time']) if 'end_time' in event else None
    start_time = parse(event['start_time']) if 'start_time' in event else None

    spot_prices = get_region_spot_prices(region, instance_types, end_time=end_time, start_time=start_time)

    if(len(spot_prices)):
        boto3.client('lambda').invoke(
            FunctionName=config['aws']['writer_function'],
            InvocationType='Event',
            Payload=json.dumps(base64.b64encode(serialise_prices(spot_prices)).decode('ascii'))  # ....yeah.
        )

    print(f'parser processed {len(spot_prices)} entries for region: {region}')

