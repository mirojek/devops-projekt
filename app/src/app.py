from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.get("/hello")
def hello():
    return jsonify(message="hello devops")

@app.get("/items")
def items():
    return jsonify(items=[1, 2, 3])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)