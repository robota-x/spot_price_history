import json

from msg_pb2 import Result


message = Result()

with open('sample_msg.bin', 'rb') as f:
    message = Result()
    message.ParseFromString(f.read())

    print(message)
