#!/usr/bin/env python3
"""
Example 2: Difference between bytes and str
Demonstrates conversion between text and binary data.
"""

def demonstrate_conversion():
    # String (text for humans)
    text = "Hello, Networks!"
    print(f"String: {text}")
    print(f"Type: {type(text)}")
    
    # Conversion to bytes (for sending over network)
    octets = text.encode('utf-8')
    print(f"\nBytes: {octets}")
    print(f"Type: {type(octets)}")
    print(f"Length in bytes: {len(octets)}")
    
    # Conversion back to string
    decoded_text = octets.decode('utf-8')
    print(f"\nDecoded: {decoded_text}")
    
    # Bytes literal (commonly used in networking)
    http_request = b"GET /index.html HTTP/1.1\r\nHost: localhost\r\n\r\n"
    print(f"\nHTTP Request (bytes):\n{http_request}")
    
    # Hexadecimal representation
    ip_bytes = b'\xC0\xA8\x01\x01'  # 192.168.1.1
    print(f"\nIP as bytes: {ip_bytes}")
    print(f"Hex: {ip_bytes.hex()}")

if __name__ == "__main__":
    demonstrate_conversion()
