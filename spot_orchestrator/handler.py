import boto3
import json


client = boto3.client('lambda')


INSTANCE_TYPES = [
    't1.micro',
    't2.nano',  # seems to be mostly unavailable
    't2.micro',
    't2.small',
    't2.medium',
    't2.large',
    't2.xlarge',
    't2.2xlarge',
    't3.nano',
    't3.micro',
    't3.small',
    't3.medium',
    't3.large',
    't3.xlarge',
    't3.2xlarge',
]

AVAILABILITY_ZONES = [
    'eu-west-1a',
    'eu-west-1b',
    'eu-west-1c',
]

PARSE_FUNCTION_NAME = 'spot_parser'  # TODO: move to arn


def lambda_handler(event, context):
    for zone in AVAILABILITY_ZONES:
        deb = client.invoke(
            FunctionName=PARSE_FUNCTION_NAME,
            InvocationType='Event',
            Payload=json.dumps({
                'availability_zone': zone,
                'instance_types': INSTANCE_TYPES
            })
        )

        print(deb)
