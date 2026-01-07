#!/usr/bin/env python3
"""
Homework Assignment 2: Session State Machine
Week 9: Session Layer (L5) and Presentation Layer (L6)

NETWORKING class - ASE, Informatics | by Revolvix

Student: <Your Name>
ID: <Student ID>
Date: <Submission Date>

Assignment:
-----------
Implement a finite state machine for managing FTP-like sessions with
authentication, command processing and timeout handling.

State Diagram:
--------------

    ┌───────────────────────────────────────────────────────┐
    │                                                       │
    │                    disconnect                         │
    │                        │                              │
    ▼                        │                              │
┌────────────┐  connect  ┌───┴──────┐  user   ┌─────────────────┐
│DISCONNECTED├──────────►│CONNECTED ├────────►│ AUTHENTICATING  │
└────────────┘           └──────────┘         └────────┬────────┘
                              ▲                        │
                              │ reset            pass  │
                              │                  ┌─────┴─────┐
                         ┌────┴───┐              │           │
                         │ ERROR  │◄─────────────┤   valid?  │
                         └────────┘   invalid    │           │
                                                 └─────┬─────┘
                                                       │ valid
                                                       ▼
┌────────────┐  complete  ┌─────────────────┐  transfer  ┌───────────────┐
│TRANSFERRING│◄───────────┤  AUTHENTICATED  │◄───────────┤               │
│            ├───────────►│                 ├───────────►│               │
└────────────┘   abort    └─────────────────┘            └───────────────┘

Requirements:
- Enum-based state definitions
- Transition validation (reject invalid transitions)
- State history with timestamps
- Session timeout handling
- Available commands per state
"""

import time
from enum import Enum, auto
from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta


# =============================================================================
# State definitions
# =============================================================================

class SessionState(Enum):
    """Session states for the state machine."""
    DISCONNECTED = auto()
    CONNECTED = auto()
    AUTHENTICATING = auto()
    AUTHENTICATED = auto()
    TRANSFERRING = auto()
    ERROR = auto()


# =============================================================================
# State history entry
# =============================================================================

@dataclass
class StateTransition:
    """Record of a state transition."""
    timestamp: datetime
    from_state: SessionState
    to_state: SessionState
    event: str
    success: bool
    details: Optional[str] = None


# =============================================================================
# TODO: Implement the Session class
# =============================================================================

class Session:
    """
    FTP-like session state machine.
    
    Manages session state transitions, command availability,
    and timeout handling.
    
    Attributes:
        state: Current session state
        username: Authenticated username (if any)
        history: List of state transitions
        timeout_seconds: Session timeout in seconds
        last_activity: Timestamp of last activity
        
    Example:
        >>> session = Session(timeout_seconds=300)
        >>> session.transition('connect')
        True
        >>> session.state
        <SessionState.CONNECTED: 2>
        >>> session.get_available_commands()
        ['user', 'disconnect']
    """
    
    # Define valid transitions as: {(from_state, event): to_state}
    # TODO: Complete this transition table
    TRANSITIONS: Dict[tuple, SessionState] = {
        # (current_state, event): new_state
        (SessionState.DISCONNECTED, 'connect'): SessionState.CONNECTED,
        # Add more transitions...
    }
    
    # Define available commands per state
    # TODO: Complete this command table
    COMMANDS: Dict[SessionState, List[str]] = {
        SessionState.DISCONNECTED: ['connect'],
        SessionState.CONNECTED: ['user', 'disconnect'],
        # Add more states...
    }
    
    def __init__(self, timeout_seconds: int = 300):
        """
        Initialise a new session.
        
        Args:
            timeout_seconds: Inactivity timeout (default 5 minutes)
        """
        self.state = SessionState.DISCONNECTED
        self.username: Optional[str] = None
        self.history: List[StateTransition] = []
        self.timeout_seconds = timeout_seconds
        self.last_activity = datetime.now()
        
        # TODO: Add any additional initialisation
    
    def transition(self, event: str, **kwargs) -> bool:
        """
        Attempt a state transition.
        
        Args:
            event: The transition event (e.g., 'connect', 'user', 'pass')
            **kwargs: Additional parameters (e.g., username, password)
            
        Returns:
            True if transition succeeded, False otherwise
            
        Example:
            >>> session = Session()
            >>> session.transition('connect')
            True
            >>> session.transition('user', username='alice')
            True
            >>> session.transition('pass', password='secret')
            True
            >>> session.state
            <SessionState.AUTHENTICATED: 4>
        """
        # TODO: Implement this method
        # 1. Check for timeout
        # 2. Look up transition in TRANSITIONS table
        # 3. Handle special cases (authentication, etc.)
        # 4. Update state
        # 5. Record transition in history
        # 6. Update last_activity timestamp
        # 7. Return success/failure
        
        raise NotImplementedError("Implement transition()")
    
    def get_available_commands(self) -> List[str]:
        """
        Get commands available in the current state.
        
        Returns:
            List of valid command names
            
        Example:
            >>> session = Session()
            >>> session.get_available_commands()
            ['connect']
        """
        # TODO: Implement this method
        # Return commands from COMMANDS table for current state
        
        raise NotImplementedError("Implement get_available_commands()")
    
    def is_timed_out(self) -> bool:
        """
        Check if the session has timed out.
        
        Returns:
            True if session is timed out, False otherwise
        """
        # TODO: Implement this method
        # Compare current time with last_activity + timeout_seconds
        
        raise NotImplementedError("Implement is_timed_out()")
    
    def reset_timeout(self) -> None:
        """Reset the activity timer."""
        self.last_activity = datetime.now()
    
    def get_history(self) -> List[StateTransition]:
        """
        Get the complete state transition history.
        
        Returns:
            List of StateTransition records
        """
        return self.history.copy()
    
    def get_state_duration(self) -> timedelta:
        """
        Get time spent in current state.
        
        Returns:
            Duration since entering current state
        """
        if not self.history:
            return timedelta(0)
        return datetime.now() - self.history[-1].timestamp
    
    def __str__(self) -> str:
        """String representation of session."""
        user_info = f" (user: {self.username})" if self.username else ""
        return f"Session[{self.state.name}{user_info}]"
    
    def __repr__(self) -> str:
        """Detailed representation of session."""
        return (f"Session(state={self.state}, username={self.username!r}, "
                f"transitions={len(self.history)})")


# =============================================================================
# Optional: Thread-safe session (bonus)
# =============================================================================

class ThreadSafeSession(Session):
    """
    Thread-safe version of Session.
    
    Uses locking to ensure safe concurrent access to session state.
    
    Bonus points if implemented correctly!
    """
    
    def __init__(self, timeout_seconds: int = 300):
        """Initialise with threading lock."""
        super().__init__(timeout_seconds)
        # TODO: Add a threading.Lock() for synchronisation
        # self._lock = threading.Lock()
    
    def transition(self, event: str, **kwargs) -> bool:
        """Thread-safe transition."""
        # TODO: Wrap parent transition() with lock
        # with self._lock:
        #     return super().transition(event, **kwargs)
        raise NotImplementedError("Implement ThreadSafeSession.transition()")


# =============================================================================
# Test cases
# =============================================================================

def test_all():
    """Run all test cases."""
    print("Testing Session State Machine Implementation")
    print("=" * 50)
    
    tests = [
        test_initial_state,
        test_basic_transitions,
        test_authentication_flow,
        test_transfer_flow,
        test_invalid_transitions,
        test_disconnect_from_any_state,
        test_error_recovery,
        test_available_commands,
        test_history_tracking,
        test_timeout_detection,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            print(f"  [PASS] {test.__name__}")
            passed += 1
        except NotImplementedError as e:
            print(f"  [SKIP] {test.__name__}: {e}")
        except AssertionError as e:
            print(f"  [FAIL] {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  [ERROR] {test.__name__}: {type(e).__name__}: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    return failed == 0


def test_initial_state():
    """Test initial session state."""
    session = Session()
    assert session.state == SessionState.DISCONNECTED
    assert session.username is None
    assert len(session.history) == 0


def test_basic_transitions():
    """Test basic state transitions."""
    session = Session()
    
    assert session.transition('connect')
    assert session.state == SessionState.CONNECTED


def test_authentication_flow():
    """Test complete authentication flow."""
    session = Session()
    
    assert session.transition('connect')
    assert session.transition('user', username='alice')
    assert session.state == SessionState.AUTHENTICATING
    
    assert session.transition('pass', password='valid_password')
    assert session.state == SessionState.AUTHENTICATED
    assert session.username == 'alice'


def test_transfer_flow():
    """Test file transfer state transitions."""
    session = Session()
    
    # Get to authenticated state
    session.transition('connect')
    session.transition('user', username='alice')
    session.transition('pass', password='valid')
    
    # Start transfer
    assert session.transition('transfer')
    assert session.state == SessionState.TRANSFERRING
    
    # Complete transfer
    assert session.transition('complete')
    assert session.state == SessionState.AUTHENTICATED


def test_invalid_transitions():
    """Test rejection of invalid transitions."""
    session = Session()
    
    # Cannot authenticate without connecting
    assert not session.transition('user', username='alice')
    assert session.state == SessionState.DISCONNECTED
    
    # Cannot transfer without authentication
    session.transition('connect')
    assert not session.transition('transfer')
    assert session.state == SessionState.CONNECTED


def test_disconnect_from_any_state():
    """Test disconnection from any state."""
    for initial_event_sequence in [
        [],
        ['connect'],
        ['connect', 'user'],
    ]:
        session = Session()
        for event in initial_event_sequence:
            session.transition(event, username='test', password='test')
        
        assert session.transition('disconnect')
        assert session.state == SessionState.DISCONNECTED


def test_error_recovery():
    """Test error state and recovery."""
    session = Session()
    
    session.transition('connect')
    session.transition('user', username='alice')
    
    # Invalid password should go to ERROR
    session.transition('pass', password='wrong_password')
    # Note: This depends on your implementation
    # You may need to adjust based on your design
    
    # Reset should return to CONNECTED
    if session.state == SessionState.ERROR:
        assert session.transition('reset')
        assert session.state == SessionState.CONNECTED


def test_available_commands():
    """Test available commands per state."""
    session = Session()
    
    # Disconnected
    cmds = session.get_available_commands()
    assert 'connect' in cmds
    assert 'transfer' not in cmds
    
    # Connected
    session.transition('connect')
    cmds = session.get_available_commands()
    assert 'user' in cmds
    assert 'disconnect' in cmds


def test_history_tracking():
    """Test state transition history."""
    session = Session()
    
    session.transition('connect')
    session.transition('user', username='alice')
    session.transition('pass', password='secret')
    
    history = session.get_history()
    assert len(history) >= 3
    
    # Verify history entries have timestamps
    for entry in history:
        assert isinstance(entry.timestamp, datetime)
        assert isinstance(entry.from_state, SessionState)
        assert isinstance(entry.to_state, SessionState)


def test_timeout_detection():
    """Test session timeout detection."""
    session = Session(timeout_seconds=1)  # 1 second timeout
    
    session.transition('connect')
    assert not session.is_timed_out()
    
    # Wait for timeout
    time.sleep(1.5)
    assert session.is_timed_out()


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    # Run tests
    success = test_all()
    
    if success:
        print("\nAll tests passed! Your implementation is complete.")
    else:
        print("\nSome tests failed. Review your implementation.")
    
    # Interactive demo (uncomment to use)
    # print("\n--- Interactive Demo ---")
    # session = Session()
    # print(f"Initial: {session}")
    # 
    # while True:
    #     print(f"\nCurrent state: {session.state.name}")
    #     print(f"Available commands: {session.get_available_commands()}")
    #     cmd = input("Enter command (or 'quit'): ").strip()
    #     
    #     if cmd == 'quit':
    #         break
    #     
    #     parts = cmd.split(maxsplit=1)
    #     event = parts[0]
    #     kwargs = {}
    #     
    #     if event == 'user' and len(parts) > 1:
    #         kwargs['username'] = parts[1]
    #     elif event == 'pass' and len(parts) > 1:
    #         kwargs['password'] = parts[1]
    #     
    #     result = session.transition(event, **kwargs)
    #     print(f"Transition '{event}': {'SUCCESS' if result else 'FAILED'}")
    #     print(f"New state: {session}")
