import configparser
import json
import os
import traceback

from pymysql import connect, cursors


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
    try:
        spot_prices = event.get('spot_prices', [])

        data_writer(spot_prices)

        print(f'writer processed {len(spot_prices)} entries')
        return {
            'statusCode': 200,
            'body': {
                'processed_entries': len(spot_prices)
            }
        }
    except:
        # dump trace and event
        traceback.print_exc()
        print(json.dumps(event))
