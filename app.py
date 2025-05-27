
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'OpenEMIS Middleware API is running.'

@app.route('/get-students', methods=['POST'])
def get_students():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    session = requests.Session()

    login_url = "https://emis.moe.gov.jo/openemis-core/index.php/user/login"
    payload = {
        "username": username,
        "password": password
    }

    try:
        login_response = session.post(login_url, data=payload, timeout=10)

        if "logout" not in login_response.text.lower():
            return jsonify({"error": "Login failed"}), 401

        students_url = "https://emis.moe.gov.jo/openemis-core/ajax.php?mod=student&act=search"
        response = session.get(students_url, timeout=10)

        return jsonify({"data": response.text})

    except Exception as e:
        return jsonify({"error": "Connection error", "details": str(e)}), 500

import os
port = int(os.environ.get("PORT", 10000))
app.run(host='0.0.0.0', port=port)
