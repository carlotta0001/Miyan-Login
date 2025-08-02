from flask import Blueprint, request, jsonify
from app.core import database

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def index():
    return "Login API is active."

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.form
    user_key = data.get('auth')
    device_id = data.get('device')

    if not user_key or not device_id:
        return jsonify({"result": "error", "message": "Missing required parameters."}), 400

    response = database.verify_and_update_device(user_key, device_id)

    if response["status"] == "success":
        expiry_date = response.get("expiry")
        expiry_str = expiry_date if expiry_date else "never"

        return jsonify({
            "result": "success",
            "message": response["message"],
            "auth": user_key,
            "expiry": expiry_str
        })
    else:
        return jsonify({"result": "error", "message": response["message"]}), 403