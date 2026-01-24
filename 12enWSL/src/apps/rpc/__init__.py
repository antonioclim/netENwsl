"""
RPC Protocol Implementations — Week 12
======================================
Computer Networks - ASE, CSIE | by ing. dr. Antonio Clim

Remote Procedure Call implementations:
- jsonrpc/ — JSON-RPC 2.0 server and client
- xmlrpc/ — XML-RPC server and client
- grpc/ — gRPC with Protocol Buffers

Usage:
    from src.apps.rpc import jsonrpc, xmlrpc, grpc
"""

__all__ = ["jsonrpc", "xmlrpc", "grpc", "benchmark_rpc"]
