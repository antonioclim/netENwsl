#!/usr/bin/env python3
"""
Homework Assignment 1: Enhanced Echo Protocol
NETWORKING class - ASE, Informatics | by Revolvix

Week 14 - Computer Networks Laboratory

OBJECTIVE:
Extend the TCP echo server to support multiple commands beyond simple echo.

REQUIREMENTS:
1. Implement a command parser that recognises different message types
2. Support at least 4 commands: ECHO, TIME, CALC, QUIT
3. Handle malformed commands gracefully
4. Maintain backwards compatibility with simple echo

COMMANDS TO IMPLEMENT:
- ECHO <message>   : Returns the message (existing behaviour)
- TIME             : Returns current server timestamp
- CALC <expr>      : Evaluates simple arithmetic (e.g., "CALC 2+3*4")
- QUIT             : Closes the connection gracefully
- HELP             : Lists available commands

EXAMPLE SESSION:
    Client: ECHO Hello World
    Server: ECHO: Hello World
    
    Client: TIME
    Server: TIME: 2026-01-07T12:30:45Z
    
    Client: CALC 10+5*2
    Server: CALC: 20
    
    Client: HELP
    Server: HELP: Available commands: ECHO, TIME, CALC, QUIT, HELP
    
    Client: QUIT
    Server: QUIT: Goodbye!
    [connection closed]

DELIVERABLES:
1. hw_14_01_server.py - Enhanced echo server implementation
2. hw_14_01_client.py - Interactive client for testing
3. hw_14_01_test.py - Test suite for all commands
4. hw_14_01_report.md - Brief report on design decisions

EVALUATION CRITERIA:
- Correctness of command parsing (30%)
- Error handling and edge cases (25%)
- Code quality and documentation (20%)
- Test coverage (15%)
- Backwards compatibility (10%)

HINTS:
- Use a dictionary to map commands to handler functions
- Consider using ast.literal_eval() for safe arithmetic evaluation
- Handle partial messages (commands may arrive in chunks)
- Remember TCP is a stream protocol, not message-based
"""

import socket
import threading
from datetime import datetime, timezone
from typing import Callable, Dict, Tuple, Optional
import ast
import operator

# Configuration
HOST = '0.0.0.0'
PORT = 9001  # Use different port from lab echo server

class EnhancedEchoServer:
    """
    Enhanced TCP Echo Server with multiple commands.
    
    TODO: Implement the command handlers and server logic.
    """
    
    def __init__(self, host: str = HOST, port: int = PORT):
        """Initialise the server."""
        self.host = host
        self.port = port
        self.running = False
        self.socket: Optional[socket.socket] = None
        
        # Command registry - maps command names to handler methods
        self.commands: Dict[str, Callable] = {
            'ECHO': self.cmd_echo,
            'TIME': self.cmd_time,
            'CALC': self.cmd_calc,
            'QUIT': self.cmd_quit,
            'HELP': self.cmd_help,
        }
    
    def cmd_echo(self, args: str) -> Tuple[str, bool]:
        """
        Handle ECHO command.
        
        Args:
            args: The message to echo
            
        Returns:
            Tuple of (response, should_continue)
        """
        # TODO: Implement ECHO command
        # Return the message prefixed with "ECHO: "
        pass
    
    def cmd_time(self, args: str) -> Tuple[str, bool]:
        """
        Handle TIME command.
        
        Args:
            args: Ignored for TIME command
            
        Returns:
            Tuple of (response, should_continue)
        """
        # TODO: Implement TIME command
        # Return current UTC timestamp in ISO format
        pass
    
    def cmd_calc(self, args: str) -> Tuple[str, bool]:
        """
        Handle CALC command for simple arithmetic.
        
        Args:
            args: Mathematical expression to evaluate
            
        Returns:
            Tuple of (response, should_continue)
            
        SECURITY NOTE:
        DO NOT use eval() directly - it's a security risk!
        Use ast.literal_eval() or implement a safe expression parser.
        
        Supported operators: +, -, *, /, //, %, **
        """
        # TODO: Implement CALC command
        # Safely evaluate arithmetic expression
        # Handle errors gracefully
        pass
    
    def cmd_quit(self, args: str) -> Tuple[str, bool]:
        """
        Handle QUIT command.
        
        Args:
            args: Ignored for QUIT command
            
        Returns:
            Tuple of (response, should_continue) where should_continue is False
        """
        # TODO: Implement QUIT command
        # Return goodbye message and signal to close connection
        pass
    
    def cmd_help(self, args: str) -> Tuple[str, bool]:
        """
        Handle HELP command.
        
        Args:
            args: Optional specific command to get help for
            
        Returns:
            Tuple of (response, should_continue)
        """
        # TODO: Implement HELP command
        # List all available commands
        pass
    
    def parse_command(self, message: str) -> Tuple[str, str]:
        """
        Parse incoming message into command and arguments.
        
        Args:
            message: Raw message from client
            
        Returns:
            Tuple of (command, arguments)
            
        Examples:
            "ECHO Hello" -> ("ECHO", "Hello")
            "TIME" -> ("TIME", "")
            "CALC 2+3*4" -> ("CALC", "2+3*4")
        """
        # TODO: Implement command parsing
        # Handle messages with and without arguments
        # Convert command to uppercase for case-insensitivity
        pass
    
    def handle_client(self, client_socket: socket.socket, address: Tuple[str, int]) -> None:
        """
        Handle a single client connection.
        
        Args:
            client_socket: Connected client socket
            address: Client address tuple (ip, port)
        """
        print(f"[INFO] Client connected: {address}")
        
        try:
            while True:
                # TODO: Implement client handling loop
                # 1. Receive data from client
                # 2. Parse command
                # 3. Execute appropriate handler
                # 4. Send response
                # 5. Check if connection should continue
                pass
                
        except Exception as e:
            print(f"[ERROR] Client {address}: {e}")
        finally:
            client_socket.close()
            print(f"[INFO] Client disconnected: {address}")
    
    def start(self) -> None:
        """Start the server and listen for connections."""
        # TODO: Implement server startup
        # 1. Create socket
        # 2. Bind to host:port
        # 3. Listen for connections
        # 4. Accept and handle clients in threads
        pass
    
    def stop(self) -> None:
        """Stop the server gracefully."""
        # TODO: Implement graceful shutdown
        pass


# Safe arithmetic evaluator (provided as helper)
class SafeCalculator:
    """
    Safe arithmetic expression evaluator.
    
    Uses AST parsing to safely evaluate mathematical expressions
    without the security risks of eval().
    """
    
    # Allowed operators
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }
    
    @classmethod
    def evaluate(cls, expression: str) -> float:
        """
        Safely evaluate a mathematical expression.
        
        Args:
            expression: String containing arithmetic expression
            
        Returns:
            Result of evaluation
            
        Raises:
            ValueError: If expression is invalid or uses unsupported operations
            
        Examples:
            >>> SafeCalculator.evaluate("2+3*4")
            14
            >>> SafeCalculator.evaluate("10/3")
            3.333...
        """
        try:
            tree = ast.parse(expression, mode='eval')
            return cls._eval_node(tree.body)
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")
    
    @classmethod
    def _eval_node(cls, node) -> float:
        """Recursively evaluate AST node."""
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value)}")
        
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in cls.OPERATORS:
                raise ValueError(f"Unsupported operator: {op_type.__name__}")
            left = cls._eval_node(node.left)
            right = cls._eval_node(node.right)
            return cls.OPERATORS[op_type](left, right)
        
        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in cls.OPERATORS:
                raise ValueError(f"Unsupported operator: {op_type.__name__}")
            operand = cls._eval_node(node.operand)
            return cls.OPERATORS[op_type](operand)
        
        else:
            raise ValueError(f"Unsupported node type: {type(node).__name__}")


def main():
    """Main entry point."""
    print("=" * 50)
    print("Enhanced Echo Server - Homework Assignment 1")
    print("NETWORKING class - ASE, Informatics")
    print("=" * 50)
    print()
    print(f"Starting server on {HOST}:{PORT}")
    print("Press Ctrl+C to stop")
    print()
    
    server = EnhancedEchoServer()
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down...")
        server.stop()


if __name__ == "__main__":
    main()
