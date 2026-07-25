 """
MCP Server — Streamable HTTP transport (manual JSON-RPC 2.0 implementation).
The grader connects as a standard MCP client:
  1. POST initialize  → server capabilities
  2. POST notifications/initialized  → 202 (no response body)
  3. POST tools/list  → list of tools
  4. POST tools/call  → call solve_challenge, reading X-Exam-Challenge from HTTP headers
We implement the protocol by hand with Flask so we have direct access to
both the JSON-RPC body AND the HTTP request headers — the standard MCP SDK
does not expose HTTP headers to tool handlers.
"""
import os
import hashlib
import json
import uuid
from flask import Flask, request, jsonify, Response
app = Flask(__name__)
# Your registered exam email, trimmed and lowercased
EMAIL = "25ds1000076@ds.study.iitm.ac.in"
# A stable session ID for this server instance
SESSION_ID = uuid.uuid4().hex
def make_response_json(req_id, result):
    """Build a JSON-RPC 2.0 success response."""
    resp = jsonify({"jsonrpc": "2.0", "id": req_id, "result": result})
    resp.headers["Content-Type"] = "application/json"
    return resp
def make_error_json(req_id, code, message):
    """Build a JSON-RPC 2.0 error response."""
    resp = jsonify({
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": code, "message": message}
    })
    resp.headers["Content-Type"] = "application/json"

    app.run(host="0.0.0.0", port=port)
