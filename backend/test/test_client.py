import socket
import struct

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9999))

START_OF_MESSAGE = 0xBABA
MSG_TYPE_SUB = 0x20
MATCHING_UNIT_CLIENT = 0x00

stream1_param = struct.pack(">B32sBB", 0x01, b"btcusdt", 0x01, 0x01)

num_streams = 1
payload = struct.pack(">B", num_streams) + stream1_param

HEADER_SIZE = 6
total_length = HEADER_SIZE + len(payload)

message_header = struct.pack(
    ">HHBB", START_OF_MESSAGE, total_length, MSG_TYPE_SUB, MATCHING_UNIT_CLIENT
)

final_message = message_header + payload
client.send(final_message)

print(f"Sent Header (Hex): {message_header.hex(' ').upper()}")
print(f"Sent Total Pack (Hex): {final_message.hex(' ').upper()}")
print(f"Total Length Byte: {message_header[2:4].hex(' ').upper()}")

try:
    while True:
        data = client.recv(1024)
        if not data:
            print("Closed Conn.")
            break
        print(f"Recv: {data}")
except KeyboardInterrupt:
    print("\nStopping.")
finally:
    client.close()
