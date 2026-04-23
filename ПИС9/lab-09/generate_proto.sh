#!/bin/bash
# Генерация Python-кода из .proto файла
# Запускать из корня проекта: bash generate_proto.sh

python3 -m grpc_tools.protoc \
    -I. \
    --python_out=grpc \
    --grpc_python_out=grpc \
    travel_service.proto

echo "Generated: grpc/travel_pb2.py and grpc/travel_pb2_grpc.py"
