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

    print(f"request_tree2: Client IP received: {client_ip}")

    return jsonify({
        "status": "ok",
        "client_ip": client_ip
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)