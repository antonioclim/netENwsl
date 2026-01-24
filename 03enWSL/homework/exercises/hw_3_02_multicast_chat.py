#!/usr/bin/env python3
"""
Homework 3.2: Multicast Chat Application
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Student: <Your Name>
Student ID: <Your ID>
Date: <Submission Date>

Description:
Implement a simple multicast-based chat application where multiple users
can join a group and exchange messages in real-time.

Requirements:
- Text-based command-line interface with username prompt
- Use multicast group 239.0.0.10, port 5010
- Concurrent sending and receiving of messages
- JSON message protocol with JOIN, MESSAGE, LEAVE types
- Display notifications for user join/leave events
- Ignore own messages (don't echo back)
- Graceful error handling

Usage:
    python hw_3_02.py [--group ADDRESS] [--port PORT]
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import socket
import struct
import sys
import json
import threading
import signal
import argparse
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, asdict
from enum import Enum

# Configuration
DEFAULT_MULTICAST_GROUP = '239.0.0.10'
DEFAULT_PORT = 5010
BUFFER_SIZE = 4096



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class MessageType(Enum):
    """Types of chat messages."""
    JOIN = "JOIN"
    MESSAGE = "MESSAGE"
    LEAVE = "LEAVE"


@dataclass


# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class ChatMessage:
    """Structure for chat messages."""
    type: str
    sender: str
    timestamp: str
    content: str = ""
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def to_json(self) -> str:
        """Serialize message to JSON string.
        
        TODO: Implement this method
        """
        # YOUR CODE HERE
        return "{}"
    
    @classmethod


# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def from_json(cls, json_str: str) -> Optional['ChatMessage']:
        """Deserialize message from JSON string.
        
        TODO: Implement this method
        - Parse JSON
        - Handle invalid JSON gracefully
        - Return ChatMessage instance or None on error
        """
        # YOUR CODE HERE
        return None
    
    @classmethod


# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCE_CREATION
# ═══════════════════════════════════════════════════════════════════════════════
    def create_join(cls, username: str) -> 'ChatMessage':
        """Create a JOIN message."""
        return cls(
            type=MessageType.JOIN.value,
            sender=username,
            timestamp=datetime.now().isoformat(),
            content=""
        )
    
    @classmethod


# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCE_CREATION
# ═══════════════════════════════════════════════════════════════════════════════
    def create_message(cls, username: str, content: str) -> 'ChatMessage':
        """Create a MESSAGE message."""
        return cls(
            type=MessageType.MESSAGE.value,
            sender=username,
            timestamp=datetime.now().isoformat(),
            content=content
        )
    
    @classmethod


# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCE_CREATION
# ═══════════════════════════════════════════════════════════════════════════════
    def create_leave(cls, username: str) -> 'ChatMessage':
        """Create a LEAVE message."""
        return cls(
            type=MessageType.LEAVE.value,
            sender=username,
            timestamp=datetime.now().isoformat(),
            content=""
        )



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class MulticastChat:
    """Multicast-based chat application."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
    def __init__(self, username: str, group: str = DEFAULT_MULTICAST_GROUP,
                 port: int = DEFAULT_PORT):
        self.username = username
        self.group = group
        self.port = port
        self.running = False
        
        self.send_socket: Optional[socket.socket] = None
        self.recv_socket: Optional[socket.socket] = None
        self.recv_thread: Optional[threading.Thread] = None
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)
    

# ═══════════════════════════════════════════════════════════════════════════════
# CLEANUP_RESOURCES
# ═══════════════════════════════════════════════════════════════════════════════
    def _handle_shutdown(self, signum, frame):
        """Handle graceful shutdown.
        
        TODO: Implement this method
        - Send LEAVE message
        - Set running to False
        - Clean up sockets
        """
        # YOUR CODE HERE
        print("\nLeaving chat...")
        self.running = False
    

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK_OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════
    def _create_send_socket(self) -> socket.socket:
        """Create socket for sending multicast messages.
        
        TODO: Implement this method
        - Create UDP socket
        - Set multicast TTL
        - Optionally disable multicast loopback
        """
        # YOUR CODE HERE
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return sock
    

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK_OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════
    def _create_recv_socket(self) -> socket.socket:
        """Create socket for receiving multicast messages.
        
        TODO: Implement this method
        - Create UDP socket
        - Set SO_REUSEADDR
        - Bind to port
        - Join multicast group using IP_ADD_MEMBERSHIP
        """
        # YOUR CODE HERE
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return sock
    

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK_OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════
    def _send_message(self, message: ChatMessage) -> None:
        """Send a message to the multicast group.
        
        TODO: Implement this method
        - Serialize message to JSON
        - Send to multicast group address and port
        """
        # YOUR CODE HERE
        pass
    

# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
    def _format_display_message(self, message: ChatMessage) -> str:
        """Format a message for display.
        
        TODO: Implement this method
        Returns formatted string based on message type:
        - JOIN: "[HH:MM:SS] <sender> joined the chat"
        - MESSAGE: "[HH:MM:SS] <sender>: <content>"
        - LEAVE: "[HH:MM:SS] <sender> left the chat"
        """
        # YOUR CODE HERE
        return ""
    

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK_OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════
    def _receive_loop(self) -> None:
        """Background thread for receiving messages.
        
        TODO: Implement this method
        - Loop while running
        - Receive messages with timeout
        - Parse JSON
        - Ignore own messages
        - Display formatted messages
        """
        # YOUR CODE HERE
        pass
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def _input_loop(self) -> None:
        """Main thread for handling user input.
        
        TODO: Implement this method
        - Loop while running
        - Read user input
        - Create and send MESSAGE
        - Handle empty input gracefully
        """
        # YOUR CODE HERE
        pass
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def start(self) -> None:
        """Start the chat application.
        
        TODO: Implement this method
        - Create sockets
        - Start receive thread
        - Send JOIN message
        - Run input loop
        """
        print(f"=== Multicast Chat ===")
        print(f"Group: {self.group}:{self.port}")
        print(f"Username: {self.username}")
        print(f"Type messages and press Enter to send")
        print(f"Press Ctrl+C to leave\n")
        
        # YOUR CODE HERE
        

# ═══════════════════════════════════════════════════════════════════════════════
# CLEANUP_RESOURCES
# ═══════════════════════════════════════════════════════════════════════════════
    def stop(self) -> None:
        """Stop the chat application and clean up.
        
        TODO: Implement this method
        - Send LEAVE message
        - Stop receive thread
        - Leave multicast group
        - Close sockets
        """
        # YOUR CODE HERE
        pass



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def get_username() -> str:
    """Prompt user for username."""
    while True:
        username = input("Enter your username: ").strip()
        if username:
            return username
        print("Username cannot be empty. Try again.")



# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════
def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Multicast Chat Application"
    )
    parser.add_argument(
        '--group', '-g',
        type=str,
        default=DEFAULT_MULTICAST_GROUP,
        help=f"Multicast group address (default: {DEFAULT_MULTICAST_GROUP})"
    )
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=DEFAULT_PORT,
        help=f"Port number (default: {DEFAULT_PORT})"
    )
    parser.add_argument(
        '--username', '-u',
        type=str,
        default=None,
        help="Username (will prompt if not provided)"
    )
    return parser.parse_args()



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Get username
    username = args.username or get_username()
    
    # Create and start chat
    chat = MulticastChat(
        username=username,
        group=args.group,
        port=args.port
    )
    
    try:
        chat.start()
    except Exception as e:
        print(f"Error: {e}")
        return 1
    finally:
        chat.stop()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
