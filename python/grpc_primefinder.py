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
    number = random.getrandbits(32)
    print(
        f"Sending random nummber {number} to {host} over gRPC to find all factors to see if they are primes"
    )
    with grpc.insecure_channel(f"{host}:{port}") as channel:
        stub = my_custom_proto_pb2_grpc.myserviceStub(channel)
        for response in stub.PrimeFinder(
            my_custom_proto_pb2.PrimeRequest(starting_number=number), metadata=auth_metadata
        ):
            print(f"{response.factor} is a factor of {number} but is it a prime factor? {response.prime}")

if __name__ == "__main__":
    main()
