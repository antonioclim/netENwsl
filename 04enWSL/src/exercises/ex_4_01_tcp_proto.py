#!/usr/bin/env python3
"""
Exercise 4.01: Custom TCP Protocol Implementation
=================================================
Computer Networks - Week 4 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

Objectives:
- Implement a TEXT protocol server supporting multiple commands
- Apply length-prefix framing for message boundaries
- Handle concurrent clients with threading

Protocol specification:
- Format: "<COMMAND> <LENGTH> <PAYLOAD>"
- COMMAND: ECHO, UPPER, LOWER, REVERSE, COUNT
- LENGTH: payload length in bytes
- PAYLOAD: the text data

Examples:
- "ECHO 5 hello"   → server responds "hello"
- "UPPER 5 hello"  → server responds "HELLO"
- "LOWER 5 HELLO"  → server responds "hello"
- "REVERSE 5 hello"→ server responds "olleh"
- "COUNT 5 hello"  → server responds "5" (character count)

TODO items to implement:
1. parse_command() - parse command from message
2. execute_command() - execute command and return result
3. handle_client() - manage communication with client
4. Main server with threading

Level: Intermediate
Estimated time: 45 minutes

Pair Programming Notes:
- Driver: Implement parse_command() and execute_command()
- Navigator: Verify edge cases (empty payload, invalid command)
- Swap after: parse_command() passes tests
"""

import socket
import threading
import sys
from typing import Tuple, Optional

# ═══════════════════════════════════════════════════════════════════════════════
# PROTOCOL_CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

VALID_COMMANDS = {'ECHO', 'UPPER', 'LOWER', 'REVERSE', 'COUNT'}
DEFAULT_PORT = 3334
BUFFER_SIZE = 4096


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_COMMAND
# ═══════════════════════════════════════════════════════════════════════════════

def parse_command(data: str) -> Tuple[Optional[str], Optional[int], Optional[str]]:
    """
    Parse received message and extract command, length and payload.
    
    Args:
        data: String in format "<COMMAND> <LENGTH> <PAYLOAD>"
    
    Returns:
        tuple: (command, length, payload) or (None, None, None) if invalid
    
    Examples:
        >>> parse_command("ECHO 5 hello")
        ('ECHO', 5, 'hello')
        >>> parse_command("UPPER 11 hello world")
        ('UPPER', 11, 'hello world')
        >>> parse_command("INVALID")
        (None, None, None)
    
    💭 PREDICTION: What will parse_command("ECHO 3 hello") return?
       The length says 3, but "hello" is 5 bytes. Think before checking!
    
    TODO: Implement this function
    Hints:
    - Use split(' ', 2) to separate into max 3 parts
    - Validate that first part is in VALID_COMMANDS
    - Convert second part to int
    - Verify that payload length matches declared value
    """
    # ═══════════════════════════════════════════════════════════════════════════
    # STEP 1: SPLIT_STRING
    # ═══════════════════════════════════════════════════════════════════════════
    # parts = data.split(' ', 2)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # STEP 2: VALIDATE_PARTS_COUNT
    # ═══════════════════════════════════════════════════════════════════════════
    # if len(parts) < 3:
    #     return (None, None, None)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # STEP 3: EXTRACT_AND_VALIDATE_COMMAND
    # ═══════════════════════════════════════════════════════════════════════════
    # command = parts[0].upper()
    # if command not in VALID_COMMANDS:
    #     return (None, None, None)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # STEP 4: EXTRACT_AND_VALIDATE_LENGTH
    # ═══════════════════════════════════════════════════════════════════════════
    # try:
    #     length = int(parts[1])
    # except ValueError:
    #     return (None, None, None)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # STEP 5: EXTRACT_PAYLOAD
    # ═══════════════════════════════════════════════════════════════════════════
    # payload = parts[2]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # STEP 6: VERIFY_LENGTH_CONSISTENCY
    # ═══════════════════════════════════════════════════════════════════════════
    # if len(payload.encode('utf-8')) != length:
    #     return (None, None, None)
    
    # return (command, length, payload)
    
    pass  # Replace with implementation


# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_COMMAND
# ═══════════════════════════════════════════════════════════════════════════════

def execute_command(command: str, payload: str) -> str:
    """
    Execute specified command on payload.
    
    Args:
        command: One of VALID_COMMANDS
        payload: Data to apply command to
    
    Returns:
        str: Result of command execution
    
    Examples:
        >>> execute_command('ECHO', 'hello')
        'hello'
        >>> execute_command('UPPER', 'hello')
        'HELLO'
        >>> execute_command('REVERSE', 'hello')
        'olleh'
    
    💭 PREDICTION: What does execute_command('COUNT', 'café') return?
       Hint: Think about UTF-8 encoding vs character count.
    
    TODO: Implement this function
    """
    # if command == 'ECHO':
    #     return payload
    # elif command == 'UPPER':
    #     return payload.upper()
    # elif command == 'LOWER':
    #     return payload.lower()
    # elif command == 'REVERSE':
    #     return payload[::-1]
    # elif command == 'COUNT':
    #     return str(len(payload))
    # else:
    #     return 'ERROR: Unknown command'
    
    pass  # Replace with implementation


# ═══════════════════════════════════════════════════════════════════════════════
# FORMAT_RESPONSE
# ═══════════════════════════════════════════════════════════════════════════════

def format_response(result: str) -> str:
    """
    Format response for client using length-prefix framing.
    
    Format: "<LENGTH> <RESULT>"
    
    Args:
        result: Result to send
    
    Returns:
        str: Formatted response
    
    💭 PREDICTION: What is format_response("OK")?
       Write your answer before uncommenting the code.
    
    TODO: Implement this function
    """
    # length = len(result.encode('utf-8'))
    # return f"{length} {result}"
    
    pass  # Replace with implementation


# ═══════════════════════════════════════════════════════════════════════════════
# HANDLE_CLIENT
# ═══════════════════════════════════════════════════════════════════════════════

def handle_client(client_socket: socket.socket, address: tuple) -> None:
    """
    Handle communication with a single client.
    
    Args:
        client_socket: Client's socket
        address: Tuple (ip, port) of client
    
    💭 PREDICTION: If client sends "ECHO 5 hello" then closes connection,
       how many times will the while loop execute?
    
    TODO: Implement this function
    Hints:
    - Use a while loop to process multiple messages
    - Call parse_command(), execute_command(), format_response()
    - Handle exceptions (ConnectionResetError, etc.)
    - Close socket at the end
    """
    print(f"[+] Client connected: {address}")
    
    # try:
    #     while True:
    #         # Receive data
    #         data = client_socket.recv(BUFFER_SIZE)
    #         if not data:
    #             break
    #         
    #         message = data.decode('utf-8').strip()
    #         print(f"[{address}] Received: {message}")
    #         
    #         # Parse command
    #         command, length, payload = parse_command(message)
    #         
    #         if command is None:
    #             response = format_response("ERROR: Invalid command format")
    #         else:
    #             result = execute_command(command, payload)
    #             response = format_response(result)
    #         
    #         # Send response
    #         client_socket.sendall(response.encode('utf-8'))
    #         print(f"[{address}] Sent: {response}")
    #         
    # except ConnectionResetError:
    #     print(f"[-] Connection reset: {address}")
    # except Exception as e:
    #     print(f"[!] Error: {e}")
    # finally:
    #     client_socket.close()
    #     print(f"[-] Client disconnected: {address}")
    
    pass  # Replace with implementation


# ═══════════════════════════════════════════════════════════════════════════════
# START_SERVER
# ═══════════════════════════════════════════════════════════════════════════════

def start_server(host: str = '0.0.0.0', port: int = DEFAULT_PORT) -> None:
    """
    Start multi-threaded TCP server.
    
    Args:
        host: Address to listen on
        port: Port to listen on
    
    💭 PREDICTION: What happens if you run two instances of this server
       on the same port? Will the second one start successfully?
    
    TODO: Implement this function
    """
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 
    # try:
    #     server_socket.bind((host, port))
    #     server_socket.listen(5)
    #     print(f"[*] Server started on {host}:{port}")
    #     print(f"[*] Accepted commands: {', '.join(VALID_COMMANDS)}")
    #     
    #     while True:
    #         client_socket, address = server_socket.accept()
    #         client_thread = threading.Thread(
    #             target=handle_client,
    #             args=(client_socket, address),
    #             daemon=True
    #         )
    #         client_thread.start()
    #         
    # except KeyboardInterrupt:
    #     print("\n[*] Server stopped")
    # finally:
    #     server_socket.close()
    
    pass  # Replace with implementation


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_CLIENT (do not modify)
# ═══════════════════════════════════════════════════════════════════════════════

def test_client(host: str = 'localhost', port: int = DEFAULT_PORT) -> bool:
    """
    Test client to verify implementation.
    """
    test_cases = [
        ("ECHO 5 hello", "5 hello"),
        ("UPPER 5 hello", "5 HELLO"),
        ("LOWER 5 HELLO", "5 hello"),
        ("REVERSE 5 hello", "5 olleh"),
        ("COUNT 5 hello", "1 5"),
        ("UPPER 11 hello world", "11 HELLO WORLD"),
    ]
    
    print(f"\n{'='*60}")
    print("TEST CLIENT - Verifying implementation")
    print(f"{'='*60}\n")
    
    passed = 0
    failed = 0
    
    for test_input, expected in test_cases:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((host, port))
            
            sock.sendall(test_input.encode('utf-8'))
            response = sock.recv(BUFFER_SIZE).decode('utf-8').strip()
            
            sock.close()
            
            if response == expected:
                print(f"✓ PASS: {test_input}")
                print(f"        Response: {response}")
                passed += 1
            else:
                print(f"✗ FAIL: {test_input}")
                print(f"        Expected: {expected}")
                print(f"        Got:      {response}")
                failed += 1
                
        except Exception as e:
            print(f"✗ ERROR: {test_input}")
            print(f"         {e}")
            failed += 1
        
        print()
    
    print(f"{'='*60}")
    print(f"Result: {passed}/{passed+failed} tests passed")
    print(f"{'='*60}")
    
    return failed == 0


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # Test client mode
        host = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
        port = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_PORT
        success = test_client(host, port)
        sys.exit(0 if success else 1)
    else:
        # Server mode
        port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
        start_server(port=port)
