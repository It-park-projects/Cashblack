from datetime import datetime
import base64


def encode_str(item):
    print(item)
    return base64.b64encode(bytes(item, 'utf-8'))

def dencode_str(item):
    return base64.b64decode(item) 