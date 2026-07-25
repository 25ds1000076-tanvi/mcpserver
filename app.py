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
    data = request.get_json(force=True, silent=True)
    if data is None:
        data = {}
    method = data.get("method", "")
    req_id = data.get("id")
    params = data.get("params", {})

    if req_id is None:
        return Response("", status=202)

    if method == "initialize":
        result = {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "exam-mcp-server", "version": "1.0.0"}
        }
        resp = jsonify({"jsonrpc": "2.0", "id": req_id, "result": result})
        resp.headers["Mcp-Session-Id"] = SESSION_ID
        return resp

    if method == "tools/list":
        tool = {
            "name": "solve_challenge",
            "description": "Solves the exam challenge",
            "inputSchema": {"type": "object", "properties": {}, "required": []}
        }
        result = {"tools": [tool]}
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": result})

    if method == "tools/call":
        tool_name = params.get("name", "")
        if tool_name != "solve_challenge":
            err = {"code": -32602, "message": "Unknown tool"}
            return jsonify({"jsonrpc": "2.0", "id": req_id, "error": err})
        to_hash = challenge + ":" + EMAIL
        answer = hashlib.sha256(to_hash.encode()).hexdigest()[:16]
        content = [{"type": "text", "text": answer}]
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": {"content": content}})

    err = {"code": -32601, "message": "Method not found"}
    return jsonify({"jsonrpc": "2.0", "id": req_id, "error": err})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
