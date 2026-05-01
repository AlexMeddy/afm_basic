from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/request_tree_ep", methods=["POST"])
def request_tree1():
    client_ip = request.remote_addr

    print(f"request_tree1: Client IP received: {client_ip}")

    return jsonify({
        "status": "ok",
        "client_ip": client_ip
    })
@app.route("/request_tree", methods=["PUT"])
def request_tree2():
    client_ip = request.remote_addr
    data = request.json or {}

    print("\n[CLIENT -> SERVER]")
    print(f"IP: {client_ip}")
    print(f"RAW BODY: {request.data}")
    print(f"PARSED JSON: {data}")

    msg = data.get("msg")

    if msg:
        print(f"ACTUAL MESSAGE: {msg}")

    response_data = {
        "status": "ok",
        "client_ip": client_ip
    }

    print("\n[SERVER -> CLIENT]")
    print(f"RESPONSE: {response_data}\n")

    return jsonify(response_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)