import boto3
import configparser
import json
import os

from datetime import datetime, timedelta
from dateutil.parser import parse
from pymysql import connect, cursors


client = boto3.client('ec2')


def spot_parser(spot):
    spot['Timestamp'] = spot['Timestamp'].isoformat(
    ) if 'Timestamp' in spot else None

    return spot


def aurora_connector():
    config = configparser.ConfigParser()
    config.read('config.ini')
    env = 'aws' if 'AWS_EXECUTION_ENV' in os.environ else 'local'

    return connect(
        host=config[env]['host'],
        user=config[env]['user'],
        password=config[env].get('pass', None),
        db=config[env]['db'],
        charset=config[env]['charset'],
        cursorclass=cursors.DictCursor
    )


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
        ProductDescriptions=['Linux/UNIX', 'Windows'],
    )

    return [spot_parser(spot) for spot in res.get('SpotPriceHistory')]


def data_writer(spot_prices):
    required_data = ['Timestamp', 'SpotPrice',
                     'AvailabilityZone', 'InstanceType', 'ProductDescription']

    connection = aurora_connector()
    with connection.cursor() as cursor:
        for price_data in spot_prices:
            if all([key in price_data for key in required_data]):
                insert_statement = 'INSERT INTO `data` VALUES (NULL, %(time)s, %(price)s, %(zone)s, %(type)s, %(product)s)'

                cursor.execute(insert_statement, {
                    'time': price_data['Timestamp'],
                    'price': price_data['SpotPrice'],
                    'zone': price_data['AvailabilityZone'],
                    'type': price_data['InstanceType'],
                    'product': price_data['ProductDescription'],
                })

    connection.commit()
    connection.close()


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

    data_writer(spot_prices)

    return {
        'statusCode': 200,
        'body': {
            'processed_entries': len(spot_prices)
        }
    }


##### debug
# fake_event = {
#     'availability_zone': 'eu-west-1a',
#     'instance_types': ['t1.micro', 't2.micro', 't3.micro'],
#     'end_time': datetime(2018, 12, 20).isoformat(),
#     # 'start_time': datetime(2018, 10, 1).isoformat(),
# }
# res = lambda_handler(fake_event, None)
# print(res)
