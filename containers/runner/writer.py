from psycopg2 import connect
from psycopg2.extras import execute_values


class SpotWriter():
    def __init__(self, **kwargs):
        self.connection = connect(**kwargs)

    def prepare_spot_prices(self, spot_prices):
        ordered_key_list = ['Timestamp', 'AvailabilityZone', 'InstanceType', 'ProductDescription', 'SpotPrice']
        return [
            tuple(price[key] for key in ordered_key_list)
            for price
            in spot_prices
        ]

    def write_spot_prices(self, spot_prices):
        prepared_prices = self.prepare_spot_prices(spot_prices)
        statement = 'INSERT INTO data (Timestamp, AvailabilityZone, InstanceType, ProductDescription, SpotPrice) VALUES %s'
        with self.connection.cursor() as cur:
            execute_values(cur, statement, prepared_prices)

        self.connection.commit()
        print(f'{len(prepared_prices)} entries commited to database')


# CREATE TABLE data (id SERIAL PRIMARY KEY, Timestamp timestamp, AvailabilityZone char(20), InstanceType char(20), ProductDescription char(20), SpotPrice float)
