#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""
Network Testing Utilities
=========================
Computer Networks - ASE Bucharest | by ing. dr. Antonio Clim

Provides helper functions for network testing and protocol validation.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import socket
import json
import time
from typing import Any, Optional
from dataclasses import dataclass

from .logger import setup_logger


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_CLASSES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class SMTPResponse:
    """Represents an SMTP server response."""
    code: int
    message: str
    raw: str


@dataclass
class RPCResponse:
    """Represents an RPC response."""
    success: bool
    result: Any
    error: Optional[dict]
    raw: str


# ═══════════════════════════════════════════════════════════════════════════════
# SMTP_TESTER_CLASS
# ═══════════════════════════════════════════════════════════════════════════════
class SMTPTester:
    """Test SMTP server connectivity and dialogue."""
    
    # ───────────────────────────────────────────────────────────────────────────
    # INITIALISATION
    # ───────────────────────────────────────────────────────────────────────────
    def __init__(self, host: str = "127.0.0.1", port: int = 1025) -> None:
        self.host = host
        self.port = port
        self.logger = setup_logger("smtp_tester")
        self.socket: Optional[socket.socket] = None
    
    # ───────────────────────────────────────────────────────────────────────────
    # CONNECTION_METHODS
    # ───────────────────────────────────────────────────────────────────────────
    def connect(self) -> SMTPResponse:
        """Connect to SMTP server and receive greeting."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(10)
        self.socket.connect((self.host, self.port))
        
        greeting = self._receive()
        return self._parse_response(greeting)
    
    def close(self) -> None:
        """Close the connection."""
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass
            self.socket = None
    
    # ───────────────────────────────────────────────────────────────────────────
    # SMTP_COMMAND_METHODS
    # ───────────────────────────────────────────────────────────────────────────
    def send_command(self, command: str) -> SMTPResponse:
        """Send an SMTP command and receive response."""
        if not self.socket:
            raise RuntimeError("Not connected")
        
        self.socket.send(f"{command}\r\n".encode("utf-8"))
        response = self._receive()
        return self._parse_response(response)
    
    def send_data(self, data: str) -> SMTPResponse:
        """Send DATA content (terminates with single dot)."""
        if not self.socket:
            raise RuntimeError("Not connected")
        
        # Ensure proper line endings and dot-stuffing
        lines = data.split("\n")
        for line in lines:
            line = line.rstrip("\r")
            # Dot-stuffing: escape leading dots
            if line.startswith("."):
                line = "." + line
            self.socket.send(f"{line}\r\n".encode("utf-8"))
        
        # Send terminating dot
        self.socket.send(b".\r\n")
        
        response = self._receive()
        return self._parse_response(response)
    
    # ───────────────────────────────────────────────────────────────────────────
    # PRIVATE_HELPER_METHODS
    # ───────────────────────────────────────────────────────────────────────────
    def _receive(self) -> str:
        """Receive data from server."""
        data = b""
        while True:
            chunk = self.socket.recv(4096)
            data += chunk
            if b"\r\n" in chunk or not chunk:
                break
        return data.decode("utf-8", errors="replace")
    
    def _parse_response(self, raw: str) -> SMTPResponse:
        """Parse SMTP response code and message."""
        lines = raw.strip().split("\r\n")
        if lines:
            first_line = lines[-1]  # Use last line for final response code
            if len(first_line) >= 3 and first_line[:3].isdigit():
                code = int(first_line[:3])
                message = first_line[4:] if len(first_line) > 4 else ""
                return SMTPResponse(code=code, message=message, raw=raw)
        
        return SMTPResponse(code=0, message="", raw=raw)
    
    # ───────────────────────────────────────────────────────────────────────────
    # TEST_METHODS
    # ───────────────────────────────────────────────────────────────────────────
    def quick_test(self) -> bool:
        """Perform a quick connectivity test."""
        try:
            greeting = self.connect()
            self.logger.info(f"Connected: {greeting.code} {greeting.message}")
            
            ehlo = self.send_command("EHLO test.client")
            self.logger.info(f"EHLO: {ehlo.code}")
            
            quit_resp = self.send_command("QUIT")
            self.logger.info(f"QUIT: {quit_resp.code}")
            
            self.close()
            return greeting.code == 220 and quit_resp.code == 221
        except Exception as e:
            self.logger.error(f"SMTP test failed: {e}")
            return False


# ═══════════════════════════════════════════════════════════════════════════════
# JSONRPC_TESTER_CLASS
# ═══════════════════════════════════════════════════════════════════════════════
class JSONRPCTester:
    """Test JSON-RPC server functionality."""
    
    # ───────────────────────────────────────────────────────────────────────────
    # INITIALISATION
    # ───────────────────────────────────────────────────────────────────────────
    def __init__(self, url: str = "http://127.0.0.1:6200") -> None:
        self.url = url
        self.logger = setup_logger("jsonrpc_tester")
        self._request_id = 0
    
    def _next_id(self) -> int:
        """Generate next request ID."""
        self._request_id += 1
        return self._request_id
    
    # ───────────────────────────────────────────────────────────────────────────
    # RPC_CALL_METHODS
    # ───────────────────────────────────────────────────────────────────────────
    def call(self, method: str, params: Any = None) -> RPCResponse:
        """
        Make a JSON-RPC 2.0 call.
        
        Args:
            method: Method name to call
            params: Parameters (list or dict)
        
        Returns:
            RPCResponse with result or error
        """
        import urllib.request
        import urllib.error
        
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "id": self._next_id()
        }
        if params is not None:
            request["params"] = params
        
        body = json.dumps(request).encode("utf-8")
        
        try:
            req = urllib.request.Request(
                self.url,
                data=body,
                headers={"Content-Type": "application/json"}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                raw = response.read().decode("utf-8")
                data = json.loads(raw)
                
                if "error" in data:
                    return RPCResponse(
                        success=False,
                        result=None,
                        error=data["error"],
                        raw=raw
                    )
                
                return RPCResponse(
                    success=True,
                    result=data.get("result"),
                    error=None,
                    raw=raw
                )
        
        except urllib.error.URLError as e:
            return RPCResponse(
                success=False,
                result=None,
                error={"code": -1, "message": str(e)},
                raw=""
            )
        except Exception as e:
            return RPCResponse(
                success=False,
                result=None,
                error={"code": -1, "message": str(e)},
                raw=""
            )
    
    def batch_call(self, calls: list[tuple[str, Any]]) -> list[RPCResponse]:
        """
        Make a batch JSON-RPC call.
        
        Args:
            calls: List of (method, params) tuples
        
        Returns:
            List of RPCResponse objects
        """
        import urllib.request
        
        requests = []
        for method, params in calls:
            req = {
                "jsonrpc": "2.0",
                "method": method,
                "id": self._next_id()
            }
            if params is not None:
                req["params"] = params
            requests.append(req)
        
        body = json.dumps(requests).encode("utf-8")
        
        try:
            req = urllib.request.Request(
                self.url,
                data=body,
                headers={"Content-Type": "application/json"}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                raw = response.read().decode("utf-8")
                data = json.loads(raw)
                
                responses = []
                for item in data:
                    if "error" in item:
                        responses.append(RPCResponse(
                            success=False,
                            result=None,
                            error=item["error"],
                            raw=json.dumps(item)
                        ))
                    else:
                        responses.append(RPCResponse(
                            success=True,
                            result=item.get("result"),
                            error=None,
                            raw=json.dumps(item)
                        ))
                
                return responses
        
        except Exception as e:
            return [RPCResponse(
                success=False,
                result=None,
                error={"code": -1, "message": str(e)},
                raw=""
            )]
    
    # ───────────────────────────────────────────────────────────────────────────
    # TEST_METHODS
    # ───────────────────────────────────────────────────────────────────────────
    def quick_test(self) -> bool:
        """Perform a quick functionality test."""
        try:
            result = self.call("add", [10, 32])
            self.logger.info(f"add(10, 32) = {result.result}")
            
            if result.success and result.result == 42:
                self.logger.info("JSON-RPC test passed")
                return True
            else:
                self.logger.error(f"Unexpected result: {result}")
                return False
        except Exception as e:
            self.logger.error(f"JSON-RPC test failed: {e}")
            return False


# ═══════════════════════════════════════════════════════════════════════════════
# XMLRPC_TESTER_CLASS
# ═══════════════════════════════════════════════════════════════════════════════
class XMLRPCTester:
    """Test XML-RPC server functionality."""
    
    # ───────────────────────────────────────────────────────────────────────────
    # INITIALISATION
    # ───────────────────────────────────────────────────────────────────────────
    def __init__(self, url: str = "http://127.0.0.1:6201") -> None:
        self.url = url
        self.logger = setup_logger("xmlrpc_tester")
        self._proxy = None
    
    @property
    def proxy(self):
        """Get or create XML-RPC proxy."""
        if self._proxy is None:
            import xmlrpc.client
            self._proxy = xmlrpc.client.ServerProxy(self.url, allow_none=True)
        return self._proxy
    
    # ───────────────────────────────────────────────────────────────────────────
    # RPC_CALL_METHODS
    # ───────────────────────────────────────────────────────────────────────────
    def call(self, method: str, *args: Any) -> RPCResponse:
        """
        Make an XML-RPC call.
        
        Args:
            method: Method name to call
            *args: Positional arguments
        
        Returns:
            RPCResponse with result or error
        """
        try:
            func = getattr(self.proxy, method)
            result = func(*args)
            
            return RPCResponse(
                success=True,
                result=result,
                error=None,
                raw=str(result)
            )
        
        except Exception as e:
            return RPCResponse(
                success=False,
                result=None,
                error={"code": -1, "message": str(e)},
                raw=""
            )
    
    # ───────────────────────────────────────────────────────────────────────────
    # TEST_METHODS
    # ───────────────────────────────────────────────────────────────────────────
    def quick_test(self) -> bool:
        """Perform a quick functionality test."""
        try:
            result = self.call("add", 10, 32)
            self.logger.info(f"add(10, 32) = {result.result}")
            
            if result.success and result.result == 42:
                self.logger.info("XML-RPC test passed")
                return True
            else:
                self.logger.error(f"Unexpected result: {result}")
                return False
        except Exception as e:
            self.logger.error(f"XML-RPC test failed: {e}")
            return False


# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_LEVEL_UTILITY_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def check_port(host: str, port: int, timeout: float = 2.0) -> bool:
    """
    Check if a port is accepting connections.
    
    Args:
        host: Host to connect to
        port: Port number
        timeout: Connection timeout in seconds
    
    Returns:
        True if port is open
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            return result == 0
    except Exception:
        return False


def wait_for_port(host: str, port: int, timeout: float = 30.0, interval: float = 1.0) -> bool:
    """
    Wait for a port to become available.
    
    Args:
        host: Host to connect to
        port: Port number
        timeout: Maximum time to wait
        interval: Time between checks
    
    Returns:
        True if port became available within timeout
    """
    start = time.time()
    while time.time() - start < timeout:
        if check_port(host, port):
            return True
        time.sleep(interval)
    return False

if __name__ == "__main__":
    # Module loaded directly - display module info
    print(f"Module {__name__} loaded successfully.")
    print(f"This module provides utility functions for the networking laboratory.")
