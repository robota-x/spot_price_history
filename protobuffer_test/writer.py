import base64
import json

from msg_pb2 import Result


message = Result()

repetitions = 100

for _ in range(repetitions):
    price = message.spotprices.add()

    price.time = '2018-12-28T11:04:00'
    price.price = 0.532300
    price.zone = 'eu-west-1a'
    price.type = 'c4.8xlarge'
    price.product = 'Linux/UNIX'

binary_message = message.SerializeToString()

with open('sample_msg.bin', 'wb') as f:
    f.write(binary_message)

with open('sample_msg.b64.json', 'w') as f:
    encoded_string = base64.b64encode(binary_message).decode('ascii')
    f.write(json.dumps(encoded_string))  # this feels so stupid.

with open('sample_msg.json', 'w') as f:
    f.write(json.dumps([{
        'AvailabilityZone': 'eu-west-1a',
        'InstanceType': 'c4.8xlarge',
        'ProductDescription': 'Linux/UNIX',
        'SpotPrice': '0.532300',
        'Timestamp': '2018-12-28T11:04:00'
    }] * repetitions))
