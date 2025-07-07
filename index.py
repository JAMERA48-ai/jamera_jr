from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "🚀 API JAMERA-ADD تعمل بنجاح!",
        "status": "OK"
    })

@app.route("/ping")
def ping():
    return "pong 🏓"
