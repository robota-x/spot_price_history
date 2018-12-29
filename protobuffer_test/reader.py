import base64
import json

from msg_pb2 import Result


message = Result()

# with open('sample_msg.bin', 'rb') as f:
#     message = Result()
#     message.ParseFromString(f.read())

#     for price in message.spotprices:
#         print('price!', price)

with open('sample_msg.b64.json', 'r') as f:
    message = Result()

    string_message = json.loads(f.read())
    byte_message = base64.b64decode(string_message.encode('ascii'))

    message.ParseFromString(byte_message)

    for price in message.spotprices:
        print('price!', price)
