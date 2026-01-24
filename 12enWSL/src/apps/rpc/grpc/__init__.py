"""
gRPC Implementation — Week 12
=============================
Computer Networks - ASE, CSIE | by ing. dr. Antonio Clim

gRPC server and client with Protocol Buffers.

Documentation: https://grpc.io/docs/languages/python/

Note: calculator_pb2.py and calculator_pb2_grpc.py are generated from
calculator.proto using grpc_tools.protoc.

Usage:
    from src.apps.rpc.grpc import grpc_server, grpc_client
"""

__all__ = [
    "grpc_server",
    "grpc_client",
    "calculator_pb2",
    "calculator_pb2_grpc",
]
