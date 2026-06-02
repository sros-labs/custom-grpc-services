#!/usr/bin/env python3


import my_custom_proto_pb2
import my_custom_proto_pb2_grpc
import grpc
import os
import random


def main():
    host = os.environ.get("PYSROS_IP", "172.20.20.10")
    port = os.environ.get("PYSROS_GRPC_PORT", "57400")
    username = os.environ.get("PYSROS_NAME", "admin")
    password = os.environ.get("PYSROS_PASS", "NokiaSros1!")
    auth_metadata = [
        ("username", username),
        ("password", password),
    ]
    number_one = random.getrandbits(16)
    number_two = random.getrandbits(16)
    print(
        f"Sending number {number_one} and {number_two} to {host} over gRPC to add them together"
    )
    with grpc.insecure_channel(f"{host}:{port}") as channel:
        stub = my_custom_proto_pb2_grpc.myserviceStub(channel)
        response = stub.Add(
            my_custom_proto_pb2.AddRequest(
                number_one=number_one, number_two=number_two
            ),
            metadata=auth_metadata,
        )
        print(response.result)


if __name__ == "__main__":
    main()
