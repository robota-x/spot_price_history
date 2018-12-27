import boto3
import json
import configparser


session = boto3.Session(profile_name='spot', region_name='eu-west-1')  # TODO remove profile
lambda_client = session.client('lambda')
s3_client = session.client('s3')

config = configparser.ConfigParser()
config.read('config.ini')


def load_required_metrics():
    obj_body = s3_client.get_object(
        Bucket=config['aws']['s3_bucket'],
        Key=config['aws']['requirements_object'],
    )['Body']

    requirements = json.loads(obj_body.read().decode('utf-8'))

    return requirements['availability_zones'], requirements['instance_types']


def lambda_handler(event, context):
    availability_zones, instance_types = load_required_metrics()

    for zone in availability_zones:
        result = lambda_client.invoke(
            FunctionName=config['aws']['parser_function'],
            InvocationType='Event',
            Payload=json.dumps({
                'availability_zone': zone,
                'instance_types': instance_types
            })
        )

        print(result)



#### debug
lambda_handler(None, None)