import os

from configparser import ConfigParser
from writer import SpotWriter
from fetcher import get_spot_prices


current_env = os.environ.get('ENV', 'live')
config_parser = ConfigParser()
config_parser.read('config.ini')
config = config_parser[current_env]


spot_prices = get_spot_prices()
SpotWriter(
    dbname=config.get('db_name', None),
    user=config.get('db_user', None),
    password=config.get('db_password', None),
    host=config.get('db_host', None),
    port=config.get('db_port', None),
).write_spot_prices(spot_prices)
