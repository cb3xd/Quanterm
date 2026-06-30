import msgspec
from typing import Callable, Union


class Test(msgspec.Struct):
    sample: str
    event_id: str | None = None


encoder = msgspec.json.Encoder()
decoder = msgspec.json.Decoder(Test)
test_dict = {"sample": "sample"}
byte_dict = encoder.encode(test_dict)
print(byte_dict)
decoded = decoder.decode(byte_dict)
decoded.event_id = "This"
print(decoded)
