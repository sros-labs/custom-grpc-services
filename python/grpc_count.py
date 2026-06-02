#!/usr/bin/env python3

import my_custom_proto_pb2
import my_custom_proto_pb2_grpc
import grpc
import os

def main():
  host = os.environ.get("PYSROS_IP", "172.20.20.10")
  port = os.environ.get("PYSROS_GRPC_PORT", "57400")
  username = os.environ.get("PYSROS_NAME", "admin")
  password = os.environ.get("PYSROS_PASS", "NokiaSros1!")
  auth_metadata = [
      ("username", username),
      ("password", password),
  ]
  with grpc.insecure_channel(f"{host}:{port}") as channel:
    stub = my_custom_proto_pb2_grpc.myserviceStub(channel)
    for response in stub.Count(my_custom_proto_pb2.CountRequest(), metadata=auth_metadata):
      print(response.response)

if __name__ == "__main__":
  main()


