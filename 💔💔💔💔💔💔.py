from flask import Flask, request, jsonify
import requests
import jwt  # pip install pyjwt

app = Flask(__name__)

@app.route('/api/get_token', methods=['GET'])
def get_token():
    uid = request.args.get('uid')
    password = request.args.get('password')

    if not uid or not password:
        return jsonify({"error": "uid and password required"}), 400

    oauth_url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    payload = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    headers = {
        'User-Agent': "GarenaMSDK/4.0.19P9(Android 13;en;US;)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip"
    }

    try:
        response = requests.post(oauth_url, data=payload, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        access_token = data.get('access_token')
        open_id = data.get('open_id')

        if not access_token or not open_id:
            return jsonify({"error": "access_token or open_id missing"}), 500

        # Decode JWT
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})

        return jsonify({
            "access_token": access_token,
            "open_id": open_id,
            "decoded": decoded_token
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# تشغيل السيرفر
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1080)