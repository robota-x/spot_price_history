from msg_pb2 import Result
import json
import datetime

message = Result()

for _ in range(6000):
    price = message.spotprices.add()

    price.time = '2018-12-28T11:04:00'
    price.price = 0.532300
    price.zone = 'eu-west-1a'
    price.type = 'c4.8xlarge'
    price.product = 'Linux/UNIX'

with open('sample_msg.bin', 'wb') as f:
    f.write(message.SerializeToString())

with open('sample_msg.json', 'w') as f:
    f.write(json.dumps([{
        'AvailabilityZone': 'eu-west-1a',
        'InstanceType': 'c4.8xlarge',
        'ProductDescription': 'Linux/UNIX',
        'SpotPrice': '0.532300',
        'Timestamp': datetime.datetime(2018, 12, 28, 11, 4).isoformat()
    }] * 6000))
