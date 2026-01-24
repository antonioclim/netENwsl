#!/usr/bin/env python3
"""
Week 10 - Homework Assignment 2: REST API Client
=================================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This template provides the structure for your REST API client.
Complete the TODO sections to implement all four Richardson Maturity levels.

Usage:
    python3 hw_10_02_rest_client.py level0 list
    python3 hw_10_02_rest_client.py level2 list
    python3 hw_10_02_rest_client.py level2 create --name "Alice" --email "alice@example.com"
    python3 hw_10_02_rest_client.py compare

TODO (Student):
1. Implement the Level 0 operation function
2. Implement all Level 2 CRUD functions
3. Add proper error handling
4. Complete the comparison table generator
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import json
import sys
from typing import Any, Dict, List, Optional

try:
    import requests
except ImportError:
    print("[ERROR] requests library required: pip install requests")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
BASE_URL = "http://127.0.0.1:5000"

# Endpoints for each level
ENDPOINTS = {
    "level0": f"{BASE_URL}/level0/service",
    "level1": f"{BASE_URL}/level1/users",
    "level2": f"{BASE_URL}/level2/users",
    "level3": f"{BASE_URL}/level3/users",
}


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL_0_RPC_STYLE
# ═══════════════════════════════════════════════════════════════════════════════
def level0_operation(action: str, **kwargs) -> Dict[str, Any]:
    """
    Call the Level 0 (RPC-style) endpoint.
    
    Level 0 uses a single endpoint with the action specified in the request body.
    All operations use POST.
    
    💭 PREDICTION: What HTTP method does Level 0 use for listing users?
    
    Args:
        action: The action to perform (list_users, get_user, create_user, etc.)
        **kwargs: Additional parameters for the action
        
    Returns:
        The JSON response from the server
        
    TODO (Student): Implement this function
    """
    url = ENDPOINTS["level0"]
    payload = {"action": action, **kwargs}
    
    # TODO: Make the POST request and return the JSON response
    # Hint: Use requests.post(url, json=payload)
    
    raise NotImplementedError("TODO: Implement level0_operation")


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL_2_REST_VERBS
# ═══════════════════════════════════════════════════════════════════════════════
def level2_list() -> List[Dict[str, Any]]:
    """
    List all users using Level 2 API.
    
    💭 PREDICTION: What HTTP method should be used to list resources?
    
    Returns:
        List of user dictionaries
        
    TODO (Student): Implement this function
    """
    url = ENDPOINTS["level2"]
    
    # TODO: Make the GET request and return the JSON response
    # Hint: Level 2 uses proper HTTP verbs - GET for reading
    
    raise NotImplementedError("TODO: Implement level2_list")


def level2_get(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Get a single user by ID using Level 2 API.
    
    Args:
        user_id: The user ID to retrieve
        
    Returns:
        User dictionary or None if not found
        
    TODO (Student): Implement this function
    """
    url = f"{ENDPOINTS['level2']}/{user_id}"
    
    # TODO: Make the GET request
    # Handle 404 Not Found by returning None
    
    raise NotImplementedError("TODO: Implement level2_get")


def level2_create(name: str, email: str) -> Dict[str, Any]:
    """
    Create a new user using Level 2 API.
    
    💭 PREDICTION: What HTTP status code should a successful create return?
    
    Args:
        name: User's name
        email: User's email
        
    Returns:
        The created user dictionary
        
    TODO (Student): Implement this function
    """
    url = ENDPOINTS["level2"]
    payload = {"name": name, "email": email}
    
    # TODO: Make the POST request to create a user
    # Hint: Check that status code is 201 Created
    
    raise NotImplementedError("TODO: Implement level2_create")


def level2_update(user_id: int, name: str, email: str) -> Optional[Dict[str, Any]]:
    """
    Update an existing user using Level 2 API.
    
    💭 PREDICTION: Should we use POST or PUT for updating?
    
    Args:
        user_id: The user ID to update
        name: New name
        email: New email
        
    Returns:
        Updated user dictionary or None if not found
        
    TODO (Student): Implement this function
    """
    url = f"{ENDPOINTS['level2']}/{user_id}"
    payload = {"name": name, "email": email}
    
    # TODO: Make the PUT request to update the user
    # Handle 404 Not Found by returning None
    
    raise NotImplementedError("TODO: Implement level2_update")


def level2_delete(user_id: int) -> bool:
    """
    Delete a user using Level 2 API.
    
    💭 PREDICTION: What HTTP status code indicates successful deletion?
    
    Args:
        user_id: The user ID to delete
        
    Returns:
        True if deleted, False if not found
        
    TODO (Student): Implement this function
    """
    url = f"{ENDPOINTS['level2']}/{user_id}"
    
    # TODO: Make the DELETE request
    # Return True if 204 No Content, False if 404 Not Found
    
    raise NotImplementedError("TODO: Implement level2_delete")


# ═══════════════════════════════════════════════════════════════════════════════
# COMPARISON_TABLE
# ═══════════════════════════════════════════════════════════════════════════════
def generate_comparison_table() -> str:
    """
    Generate a markdown comparison table of all levels.
    
    This function should:
    1. Perform the same operation at each level
    2. Document the request format used
    3. Document the response format received
    4. Note the HTTP status codes
    
    Returns:
        Markdown formatted comparison table
        
    TODO (Student): Implement this function to generate comparison_table.md
    """
    table = """# REST API Levels Comparison

## Student: [YOUR NAME HERE]
## Date: [DATE]

---

## Operation: List Users

| Aspect | Level 0 | Level 1 | Level 2 | Level 3 |
|--------|---------|---------|---------|---------|
| HTTP Method | POST | ? | ? | ? |
| URL | /level0/service | ? | ? | ? |
| Request Body | {"action": "list_users"} | ? | ? | ? |
| Response Format | ? | ? | ? | ? |

---

## Operation: Create User

| Aspect | Level 0 | Level 1 | Level 2 | Level 3 |
|--------|---------|---------|---------|---------|
| HTTP Method | ? | ? | ? | ? |
| URL | ? | ? | ? | ? |
| Request Body | ? | ? | ? | ? |
| Status Code | ? | ? | ? | ? |

---

## TODO: Add more operations (get, update, delete)

---

## Observations

### Level 0 → Level 1 Difference
[Your observation here]

### Level 1 → Level 2 Difference
[Your observation here]

### Level 2 → Level 3 Difference
[Your observation here]

"""
    return table


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND_LINE_INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    parser = argparse.ArgumentParser(description="REST API Client for Week 10 Homework")
    subparsers = parser.add_subparsers(dest="level", required=True)
    
    # Level 0 commands
    p_l0 = subparsers.add_parser("level0", help="Level 0 (RPC-style) operations")
    p_l0.add_argument("action", choices=["list", "get", "create", "update", "delete"])
    p_l0.add_argument("--id", type=int, help="User ID for get/update/delete")
    p_l0.add_argument("--name", help="User name for create/update")
    p_l0.add_argument("--email", help="User email for create/update")
    
    # Level 2 commands
    p_l2 = subparsers.add_parser("level2", help="Level 2 (REST verbs) operations")
    p_l2.add_argument("action", choices=["list", "get", "create", "update", "delete"])
    p_l2.add_argument("--id", type=int, help="User ID for get/update/delete")
    p_l2.add_argument("--name", help="User name for create/update")
    p_l2.add_argument("--email", help="User email for create/update")
    
    # Comparison command
    subparsers.add_parser("compare", help="Generate comparison table")
    
    args = parser.parse_args()
    
    try:
        if args.level == "compare":
            table = generate_comparison_table()
            print(table)
            with open("comparison_table.md", "w") as f:
                f.write(table)
            print("\n[INFO] Saved to comparison_table.md")
            return 0
        
        if args.level == "level0":
            if args.action == "list":
                result = level0_operation("list_users")
            elif args.action == "get":
                result = level0_operation("get_user", user_id=args.id)
            elif args.action == "create":
                result = level0_operation("create_user", name=args.name, email=args.email)
            elif args.action == "update":
                result = level0_operation("update_user", user_id=args.id, name=args.name, email=args.email)
            elif args.action == "delete":
                result = level0_operation("delete_user", user_id=args.id)
            print(json.dumps(result, indent=2))
            
        elif args.level == "level2":
            if args.action == "list":
                result = level2_list()
            elif args.action == "get":
                result = level2_get(args.id)
            elif args.action == "create":
                result = level2_create(args.name, args.email)
            elif args.action == "update":
                result = level2_update(args.id, args.name, args.email)
            elif args.action == "delete":
                result = level2_delete(args.id)
            print(json.dumps(result, indent=2) if result else "Not found / Deleted")
            
        return 0
        
    except NotImplementedError as e:
        print(f"[ERROR] {e}")
        print("[INFO] Complete the TODO sections in this file first!")
        return 1
    except requests.RequestException as e:
        print(f"[ERROR] Request failed: {e}")
        print("[INFO] Make sure the REST levels server is running:")
        print("       python3 src/exercises/ex_10_02_richardson_maturity.py serve")
        return 1


if __name__ == "__main__":
    sys.exit(main())
