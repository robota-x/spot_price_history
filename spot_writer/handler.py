import configparser
import os
import traceback

from msg_pb2 import Result
from pymysql import connect, cursors


def deserialise_prices(payload):
    msg = Result()

    try:
        msg.ParseFromString(payload)

        return msg.spotprices
    except:
        print(f'failed parsing payload: {payload}')
        return []


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


def data_writer(spot_prices):
    required_fields = ['time', 'price',
                       'zone', 'type', 'product']

    connection = aurora_connector()
    with connection.cursor() as cursor:
        success_count = 0

        for datapoint in spot_prices:
            if all([getattr(datapoint, field) for field in required_fields]):
                insert_statement = 'INSERT INTO `data` VALUES (NULL, %(time)s, %(price)s, %(zone)s, %(type)s, %(product)s)'

                cursor.execute(insert_statement, {
                    'time': datapoint.time,
                    'price': datapoint.price,
                    'zone': datapoint.zone,
                    'type': datapoint.type,
                    'product': datapoint.product,
                })
            success_count += 1

    connection.commit()
    connection.close()
    return success_count


def lambda_handler(event, context):
    spot_prices = deserialise_prices(event)
    success_count = data_writer(spot_prices)

    print(f'writer processed {len(spot_prices)} entries. {success_count} success, {len(spot_prices) - success_count} failures')
    return {
        'statusCode': 200,
        'body': {
            'processed_entries': len(spot_prices)
        }
    }
