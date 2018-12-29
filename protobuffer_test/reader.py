import json

from msg_pb2 import Result


message = Result()

with open('sample_msg.bin', 'rb') as f:
    message = Result()
    message.ParseFromString(f.read())

    for price in message.spotprices:
        print('price!', price)
