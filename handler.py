import boto3
import json
from datetime import datetime, timedelta


client = boto3.client('ec2')


def spot_parser(spot):
    spot['Timestamp'] = spot['Timestamp'].isoformat(
    ) if 'Timestamp' in spot else None

    return spot


def price_grabber(availability_zone, instance_types, end_time=None, start_time=None):
    computed_end_time = end_time or datetime.now()
    computed_start_time = start_time or (
        computed_end_time - timedelta(seconds=3610))

    # not using filters as they seem to be quite flaky results
    res = client.describe_spot_price_history(
        AvailabilityZone=availability_zone,
        InstanceTypes=instance_types,
        EndTime=computed_end_time,
        StartTime=computed_start_time,
        ProductDescriptions=['Linux/UNIX'],
    )

    return [spot_parser(spot) for spot in res.get('SpotPriceHistory')]


def lambda_handler(event, context):
    availability_zone = 'eu-west-1a'
    instance_types = ['t2.micro', 't3.micro']
    prices = price_grabber(availability_zone, instance_types)

    return {
        'statusCode': 200,
        'body': {
            'price_list': json.dumps(prices),
            'len': len(prices)
        }
    }


## debug
res = lambda_handler(None, None)
print(res)
