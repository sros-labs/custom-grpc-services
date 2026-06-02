#!/usr/bin/env bash

python \
    -m grpc_tools.protoc \
    --python_out=python/ \
    --pyi_out=python/ \
    --grpc_python_out=python/ \
    -oproto/my_custom_proto.protoc \
    -Iproto/ \
    proto/my_custom_proto.proto
