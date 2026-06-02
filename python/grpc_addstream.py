#!/usr/bin/env python3
import my_custom_proto_pb2
import my_custom_proto_pb2_grpc
import grpc
import os
import random

def _generate_messages(number_of_messages):
    print(f"Sending the following numbers: ", end="")
    for i in range(0, number_of_messages):
        number = random.getrandbits(16)
        print(f"{number} ", end="")
        yield my_custom_proto_pb2.AddStreamRequest(number=number)
    print("\n")


def main():
    host = os.environ.get("PYSROS_IP", "172.20.20.10")
    port = os.environ.get("PYSROS_GRPC_PORT", "57400")
    username = os.environ.get("PYSROS_NAME", "admin")
    password = os.environ.get("PYSROS_PASS", "NokiaSros1!")
    auth_metadata = [
        ("username", username),
        ("password", password),
    ]
    number_of_messages = random.getrandbits(8)
    print(
        f"Sending number 8 gRPC messages to {host} over gRPC (each with one number) to add them together"
    )
    with grpc.insecure_channel(f"{host}:{port}") as channel:
        stub = my_custom_proto_pb2_grpc.myserviceStub(channel)
        response = stub.StreamingAdd(
            _generate_messages(number_of_messages), metadata=auth_metadata
        )
    print(
        f"{host} performed the addition of the above numbers.  The result is {response.result}"
    )


if __name__ == "__main__":
    main()
