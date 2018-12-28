import boto3
import configparser
import json

from datetime import datetime, timedelta
from dateutil.parser import parse


ec2_client = boto3.client('ec2')
lambda_client = boto3.client('lambda')

config = configparser.ConfigParser()
config.read('config.ini')


def spot_parser(spot):
    spot['Timestamp'] = spot['Timestamp'].isoformat(
    ) if 'Timestamp' in spot else None

    return spot


def price_grabber(availability_zone, instance_types, end_time=None, start_time=None):
    computed_end_time = end_time or datetime.now()
    computed_start_time = start_time or (
        computed_end_time - timedelta(seconds=3610))

    # not using filters as they seem to be quite flaky results
    res = ec2_client.describe_spot_price_history(
        AvailabilityZone=availability_zone,
        InstanceTypes=instance_types,
        EndTime=computed_end_time,
        StartTime=computed_start_time,
        ProductDescriptions=['Linux/UNIX', 'Windows'],
    )

    return [spot_parser(spot) for spot in res.get('SpotPriceHistory', [])]


def lambda_handler(event, context):
    availability_zone = event.get('availability_zone', 'eu-west-1a')
    instance_types = event.get('instance_types', ['t1.micro'])

    end_time = parse(event['end_time']) if 'end_time' in event else None
    start_time = parse(event['start_time']) if 'start_time' in event else None

    spot_prices = price_grabber(
        availability_zone,
        instance_types,
        end_time=end_time,
        start_time=start_time
    )

    if(len(spot_prices)):
        lambda_client.invoke(
            FunctionName=config['aws']['writer_function'],
            InvocationType='Event',
            Payload=json.dumps({'spot_prices': spot_prices})
        )

    print(f'parser processed {len(spot_prices)} entries for zone: {availability_zone}')
    return {
        'statusCode': 200,
        'body': {
            'processed_entries': len(spot_prices)
        }
    }
