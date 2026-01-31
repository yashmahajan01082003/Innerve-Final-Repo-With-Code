# backend/app/services/email_service.py
import smtplib
from email.mime.text import MIMEText
from flask import Blueprint, jsonify, request
from ..config import config

bp = Blueprint('email', __name__, url_prefix='/api/email')


@bp.route('/send', methods=['POST'])
def send_email():
    data = request.json
    sender = config.EMAIL
    password = config.EMAIL_PASSWORD

    try:
        msg = MIMEText(data['message'])
        msg['Subject'] = data['subject']
        msg['From'] = sender
        msg['To'] = data['recipient']

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.send_message(msg)

        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500