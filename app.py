import os
import hashlib
import uuid
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

EMAIL = "25ds1000076@ds.study.iitm.ac.in"
SESSION_ID = uuid.uuid4().hex


@app.route("/", methods=["GET"])
def health():
    return "MCP Server is alive and ready!"


@app.route("/", methods=["POST"])
@app.route("/mcp", methods=["POST"])
def mcp_endpoint():
    challenge = request.headers.get("X-Exam-Challenge", "")
    data = request.get_json(force=True, silent=True) or {}
    method = data.get("method", "")
    req_id = data.get("id")
    params = data.get("params", {})

    if req_id is None:
        return Response("", status=202)

    if method == "initialize":
        resp = jsonify({"jsonrpc": "2.0", "id": req_id, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "exam-mcp-server", "version": "1.0.0"}
        }})
        resp.headers["Mcp-Session-Id"] = SESSION_ID
        return resp

    if method == "tools/list":
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": {
            "tools": [{
                "name": "solve_challenge",
                "description": "Solves the exam challenge",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            }]
        }})

    if method == "tools/call":
        tool_name = params.get("name", "")
        if tool_name != "solve_challenge":
            return jsonify({"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": "Unknown tool"}})
        answer = hashlib.sha256(f"{challenge}:{EMAIL}".encode()).hexdigest()[:16]
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": {
            "content": [{"type": "text", "text": answer}]
        }})

    return jsonify({"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)ort)
