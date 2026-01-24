#!/usr/bin/env python3
"""
Week 10 - Exercise 2: Richardson Maturity Model — From RPC to HATEOAS
================================================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This exercise implements a Flask server that demonstrates all four levels
of the Richardson Maturity Model for REST APIs:

- Level 0: Single URI, RPC-style (HTTP as transport)
- Level 1: Multiple URIs for resources
- Level 2: HTTP verbs used semantically
- Level 3: Hypermedia controls (HATEOAS)

Objectives:
- Compare API designs across maturity levels
- Understand the progression from RPC to REST
- Implement proper HTTP verb semantics

Prerequisites:
- Python 3.11+
- Flask library (pip install flask)

Pair Programming Notes:
- Driver: Start server and make Level 0-1 requests
- Navigator: Document differences in request format
- Swap after: Completing Level 1 requests

Common Errors
-------------
1. "Address already in use" → Kill process on port 5000: lsof -ti:5000 | xargs kill
2. "Flask not found" → pip install flask --break-system-packages
3. "405 Method Not Allowed" → Wrong HTTP verb for the endpoint level
4. "404 Not Found" → Check URL path matches the level (level0, level1, level2, level3)
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import sys
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

try:
    from flask import Flask, jsonify, request, url_for
except ImportError:
    print("[ERROR] Flask is required: pip install flask")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_MODEL
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class User:
    """User entity for demonstration."""
    id: int
    name: str
    email: str


class UserStore:
    """Thread-safe in-memory user storage."""
    
    def __init__(self) -> None:
        self._users: Dict[int, User] = {}
        self._next_id = 1
        self._lock = threading.Lock()
        self._seed_data()

    def _seed_data(self) -> None:
        """Add initial demo data."""
        self.create("Alice Smith", "alice@example.com")
        self.create("Bob Jones", "bob@example.com")

    def list_all(self) -> List[Dict[str, Any]]:
        """Return all users."""
        with self._lock:
            return [self._to_dict(u) for u in self._users.values()]

    def get(self, uid: int) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        with self._lock:
            user = self._users.get(uid)
            return None if user is None else self._to_dict(user)

    def create(self, name: str, email: str) -> Dict[str, Any]:
        """Create a new user."""
        with self._lock:
            uid = self._next_id
            self._next_id += 1
            user = User(id=uid, name=name, email=email)
            self._users[uid] = user
            return self._to_dict(user)

    def update(self, uid: int, name: Optional[str], email: Optional[str]) -> Optional[Dict[str, Any]]:
        """Update an existing user."""
        with self._lock:
            user = self._users.get(uid)
            if user is None:
                return None
            if name is not None:
                user.name = name
            if email is not None:
                user.email = email
            return self._to_dict(user)

    def delete(self, uid: int) -> bool:
        """Delete a user."""
        with self._lock:
            return self._users.pop(uid, None) is not None

    @staticmethod
    def _to_dict(user: User) -> Dict[str, Any]:
        """Convert User to dictionary."""
        return {"id": user.id, "name": user.name, "email": user.email}


# ═══════════════════════════════════════════════════════════════════════════════
# FLASK_APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════
app = Flask(__name__)
store = UserStore()


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL_0_ENDPOINTS (RPC-style, single endpoint)
# ═══════════════════════════════════════════════════════════════════════════════
@app.route("/level0/service", methods=["POST"])
def level0_service() -> tuple:
    """
    Level 0: The Swamp of POX (Plain Old XML/JSON)
    
    💭 PREDICTION: How will the request differ from a typical REST API?
    
    All operations go through a single endpoint with an "action" field.
    This is RPC-style - HTTP is just a transport tunnel.
    """
    data = request.get_json() or {}
    action = data.get("action", "")

    if action == "list_users":
        return jsonify({"status": "ok", "users": store.list_all()}), 200

    if action == "get_user":
        uid = data.get("id")
        if uid is None:
            return jsonify({"status": "error", "message": "Missing id"}), 200
        user = store.get(int(uid))
        if user is None:
            return jsonify({"status": "error", "message": "User not found"}), 200
        return jsonify({"status": "ok", "user": user}), 200

    if action == "create_user":
        name = data.get("name", "")
        email = data.get("email", "")
        if not name or not email:
            return jsonify({"status": "error", "message": "Missing name or email"}), 200
        user = store.create(name, email)
        return jsonify({"status": "ok", "user": user}), 200

    if action == "update_user":
        uid = data.get("id")
        if uid is None:
            return jsonify({"status": "error", "message": "Missing id"}), 200
        user = store.update(int(uid), data.get("name"), data.get("email"))
        if user is None:
            return jsonify({"status": "error", "message": "User not found"}), 200
        return jsonify({"status": "ok", "user": user}), 200

    if action == "delete_user":
        uid = data.get("id")
        if uid is None:
            return jsonify({"status": "error", "message": "Missing id"}), 200
        if not store.delete(int(uid)):
            return jsonify({"status": "error", "message": "User not found"}), 200
        return jsonify({"status": "ok", "message": "Deleted"}), 200

    return jsonify({"status": "error", "message": f"Unknown action: {action}"}), 200


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL_1_ENDPOINTS (Resources with URIs)
# ═══════════════════════════════════════════════════════════════════════════════
@app.route("/level1/users/list", methods=["POST"])
def level1_list() -> tuple:
    """
    Level 1: Resources
    
    💭 PREDICTION: What's different from Level 0? What's still missing?
    
    Multiple URIs for different resources, but still using POST for everything.
    """
    return jsonify({"users": store.list_all()}), 200


@app.route("/level1/users/<int:uid>/get", methods=["POST"])
def level1_get(uid: int) -> tuple:
    """Level 1: Get a specific user (still POST)."""
    user = store.get(uid)
    if user is None:
        return jsonify({"error": "User not found"}), 200
    return jsonify({"user": user}), 200


@app.route("/level1/users/create", methods=["POST"])
def level1_create() -> tuple:
    """Level 1: Create user (action in URL)."""
    data = request.get_json() or {}
    name = data.get("name", "")
    email = data.get("email", "")
    if not name or not email:
        return jsonify({"error": "Missing name or email"}), 200
    user = store.create(name, email)
    return jsonify({"user": user}), 200


@app.route("/level1/users/<int:uid>/update", methods=["POST"])
def level1_update(uid: int) -> tuple:
    """Level 1: Update user (action in URL)."""
    data = request.get_json() or {}
    user = store.update(uid, data.get("name"), data.get("email"))
    if user is None:
        return jsonify({"error": "User not found"}), 200
    return jsonify({"user": user}), 200


@app.route("/level1/users/<int:uid>/delete", methods=["POST"])
def level1_delete(uid: int) -> tuple:
    """Level 1: Delete user (action in URL)."""
    if not store.delete(uid):
        return jsonify({"error": "User not found"}), 200
    return jsonify({"message": "Deleted"}), 200


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL_2_ENDPOINTS (HTTP Verbs)
# ═══════════════════════════════════════════════════════════════════════════════
@app.route("/level2/users", methods=["GET"])
def level2_list() -> tuple:
    """
    Level 2: HTTP Verbs
    
    💭 PREDICTION: What HTTP status codes should each operation return?
    - GET (list): ?
    - POST (create): ?
    - PUT (update): ?
    - DELETE: ?
    
    Proper use of HTTP methods and status codes.
    """
    return jsonify({"users": store.list_all()}), 200


@app.route("/level2/users/<int:uid>", methods=["GET"])
def level2_get(uid: int) -> tuple:
    """Level 2: GET for retrieval."""
    user = store.get(uid)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


@app.route("/level2/users", methods=["POST"])
def level2_create() -> tuple:
    """Level 2: POST for creation → 201 Created."""
    data = request.get_json() or {}
    name = data.get("name", "")
    email = data.get("email", "")
    if not name or not email:
        return jsonify({"error": "Missing name or email"}), 400
    user = store.create(name, email)
    return jsonify(user), 201


@app.route("/level2/users/<int:uid>", methods=["PUT"])
def level2_update(uid: int) -> tuple:
    """Level 2: PUT for update."""
    data = request.get_json() or {}
    user = store.update(uid, data.get("name"), data.get("email"))
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


@app.route("/level2/users/<int:uid>", methods=["DELETE"])
def level2_delete(uid: int) -> tuple:
    """Level 2: DELETE for removal → 204 No Content."""
    if not store.delete(uid):
        return jsonify({"error": "User not found"}), 404
    return "", 204


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL_3_ENDPOINTS (HATEOAS)
# ═══════════════════════════════════════════════════════════════════════════════
def add_user_links(user: Dict[str, Any]) -> Dict[str, Any]:
    """Add hypermedia links to a user resource."""
    uid = user["id"]
    user["_links"] = {
        "self": {"href": f"/level3/users/{uid}", "method": "GET"},
        "update": {"href": f"/level3/users/{uid}", "method": "PUT"},
        "delete": {"href": f"/level3/users/{uid}", "method": "DELETE"},
        "collection": {"href": "/level3/users", "method": "GET"},
    }
    return user


@app.route("/level3/users", methods=["GET"])
def level3_list() -> tuple:
    """
    Level 3: Hypermedia Controls (HATEOAS)
    
    💭 PREDICTION: What extra information will the response contain?
    
    Responses include links for navigation and available actions.
    """
    users = [add_user_links(u) for u in store.list_all()]
    return jsonify({
        "users": users,
        "_links": {
            "self": {"href": "/level3/users", "method": "GET"},
            "create": {"href": "/level3/users", "method": "POST"},
        }
    }), 200


@app.route("/level3/users/<int:uid>", methods=["GET"])
def level3_get(uid: int) -> tuple:
    """Level 3: GET with hypermedia links."""
    user = store.get(uid)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(add_user_links(user)), 200


@app.route("/level3/users", methods=["POST"])
def level3_create() -> tuple:
    """Level 3: POST with hypermedia in response."""
    data = request.get_json() or {}
    name = data.get("name", "")
    email = data.get("email", "")
    if not name or not email:
        return jsonify({"error": "Missing name or email"}), 400
    user = store.create(name, email)
    return jsonify(add_user_links(user)), 201


@app.route("/level3/users/<int:uid>", methods=["PUT"])
def level3_update(uid: int) -> tuple:
    """Level 3: PUT with hypermedia in response."""
    data = request.get_json() or {}
    user = store.update(uid, data.get("name"), data.get("email"))
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(add_user_links(user)), 200


@app.route("/level3/users/<int:uid>", methods=["DELETE"])
def level3_delete(uid: int) -> tuple:
    """Level 3: DELETE."""
    if not store.delete(uid):
        return jsonify({"error": "User not found"}), 404
    return "", 204


# ═══════════════════════════════════════════════════════════════════════════════
# INDEX_PAGE
# ═══════════════════════════════════════════════════════════════════════════════
@app.route("/")
def index() -> str:
    """Home page with API documentation."""
    return """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Week 10 - REST Maturity Levels</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 800px; margin: 2em auto; padding: 0 1em; }
        code { background: #f4f4f4; padding: 0.2em 0.4em; border-radius: 3px; }
        pre { background: #f4f4f4; padding: 1em; overflow-x: auto; }
        h2 { border-bottom: 2px solid #333; padding-bottom: 0.3em; margin-top: 2em; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 0.5em; text-align: left; }
        th { background: #f4f4f4; }
    </style>
</head>
<body>
    <h1>Week 10 - Richardson Maturity Model</h1>
    
    <h2>Level 0: The Swamp of POX</h2>
    <p>Single endpoint, action in body:</p>
    <pre>POST /level0/service
{"action": "list_users"}
{"action": "get_user", "id": 1}
{"action": "create_user", "name": "...", "email": "..."}
{"action": "update_user", "id": 1, "name": "..."}
{"action": "delete_user", "id": 1}</pre>

    <h2>Level 1: Resources</h2>
    <p>Multiple URIs, but still POST for everything:</p>
    <pre>POST /level1/users/list
POST /level1/users/1/get
POST /level1/users/create {"name": "...", "email": "..."}
POST /level1/users/1/update {"name": "..."}
POST /level1/users/1/delete</pre>

    <h2>Level 2: HTTP Verbs</h2>
    <p>Proper HTTP methods and status codes:</p>
    <pre>GET    /level2/users         → 200 OK
GET    /level2/users/1       → 200 OK / 404 Not Found
POST   /level2/users         → 201 Created
PUT    /level2/users/1       → 200 OK / 404 Not Found
DELETE /level2/users/1       → 204 No Content / 404 Not Found</pre>

    <h2>Level 3: Hypermedia (HATEOAS)</h2>
    <p>Same as Level 2, but responses include navigation links:</p>
    <pre>GET /level3/users/1
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com",
  "_links": {
    "self": {"href": "/level3/users/1", "method": "GET"},
    "update": {"href": "/level3/users/1", "method": "PUT"},
    "delete": {"href": "/level3/users/1", "method": "DELETE"},
    "collection": {"href": "/level3/users", "method": "GET"}
  }
}</pre>

    <h2>Comparison Table</h2>
    <table>
        <tr><th>Operation</th><th>Level 0</th><th>Level 1</th><th>Level 2</th><th>Level 3</th></tr>
        <tr><td>List</td><td>POST /service action=list</td><td>POST /users/list</td><td>GET /users</td><td>GET /users + links</td></tr>
        <tr><td>Get</td><td>POST /service action=get</td><td>POST /users/1/get</td><td>GET /users/1</td><td>GET /users/1 + links</td></tr>
        <tr><td>Create</td><td>POST /service action=create</td><td>POST /users/create</td><td>POST /users</td><td>POST /users + links</td></tr>
        <tr><td>Update</td><td>POST /service action=update</td><td>POST /users/1/update</td><td>PUT /users/1</td><td>PUT /users/1 + links</td></tr>
        <tr><td>Delete</td><td>POST /service action=delete</td><td>POST /users/1/delete</td><td>DELETE /users/1</td><td>DELETE /users/1</td></tr>
    </table>
</body>
</html>"""


# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT_PARSING
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="REST Maturity Levels Demo")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_serve = sub.add_parser("serve", help="Start the Flask server")
    p_serve.add_argument("--host", default=DEFAULT_HOST)
    p_serve.add_argument("--port", type=int, default=DEFAULT_PORT)
    p_serve.add_argument("--debug", action="store_true")

    return parser.parse_args(argv)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main(argv: list[str]) -> int:
    """Main entry point."""
    args = parse_args(argv)

    if args.cmd == "serve":
        print(f"[INFO] Starting REST levels server on http://{args.host}:{args.port}/")
        print("[INFO] Press Ctrl+C to stop")
        app.run(host=args.host, port=args.port, debug=args.debug)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
