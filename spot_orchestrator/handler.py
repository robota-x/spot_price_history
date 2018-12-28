import boto3
import configparser
import json
import traceback


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

    return requirements['regions'], requirements['instance_types']


def lambda_handler(event, context):
    try:
        regions, instance_types = load_required_metrics()

        for region in regions:
            result = lambda_client.invoke(
                FunctionName=config['aws']['parser_function'],
                InvocationType='Event',
                Payload=json.dumps({
                    'region': region,
                    'instance_types': instance_types
                })
            )

        print(f'orchestrator processed {len(regions)} regions')
        return {
            'statusCode': 200,
            'body': {
                'processed_regions': len(regions)
            }
        }
    except:
        # dump trace and event
        traceback.print_exc()
        print(json.dumps(event))
