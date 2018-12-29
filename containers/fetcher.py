import boto3
import json
import os

from configparser import ConfigParser

CONFIG = None

def get_config():
    global CONFIG
    if CONFIG is None:
        current_env = os.environ.get('ENV', 'live')
        config_parser = ConfigParser()
        config_parser.read('config.ini')
        CONFIG = config_parser[current_env]

    return CONFIG


def load_required_metrics():
    config = get_config()

    obj_body = boto3 \
        .session.Session(profile_name=config['aws_profile']) \
        .client('s3') \
        .get_object(
            Bucket=config['requirements_s3_bucket'],
            Key=config['requirements_s3_key'],
        )['Body']
    requirements = json.loads(obj_body.read().decode('utf-8'))

    return {
        'regions': requirements.get('regions'),
        'instance_types': requirements.get('instance_types'),
    }


# debug
res = load_required_metrics()
print(res)