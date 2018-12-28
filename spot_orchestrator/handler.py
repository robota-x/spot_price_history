import boto3
import json
import configparser


lambda_client = boto3.client('lambda')
s3_client = boto3.client('s3')

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
    try:
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

        print(f'orchestrator processed {len(availability_zones)} zones')
        return {
            'statusCode': 200,
            'body': {
                'processed_zones': len(availability_zones)
            }
        }
    except:
        # dump trace and event
        traceback.print_exc()
        print(json.dumps(event))

