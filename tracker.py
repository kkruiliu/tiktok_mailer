from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from datetime import datetime
from io import BytesIO
import os

from database import mark_email_opened, unsubscribe_user
from send_email import send_email

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains


@app.route('/open/<message_id>')
def track_open(message_id):
    print(f"Tracking open for message_id: {message_id}")
    mark_email_opened(message_id)

    # Return a 1x1 transparent GIF
    pixel = BytesIO(
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF'
        b'\x21\xF9\x04\x01\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4C\x01\x00\x3B'
    )
    return send_file(pixel, mimetype='image/gif')

# --- 2. Unsubscribe ---
@app.route('/unsubscribe')
def unsubscribe():
    email = request.args.get('email')
    if email:
        unsubscribe_user(email)
        return f"<h3>{email} has been unsubscribed.</h3>"
    else:
        return "<h3>Error: missing email parameter.</h3>", 400

# --- 3. Send email from HTML content ---
@app.route('/send-html', methods=['POST'])
def send_html():
    data = request.json
    html = data.get('html')
    to_email = data.get('to')
    subject = data.get('subject', 'Untitled Campaign')

    if not html or not to_email:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        send_email(
            recipient=to_email,
            subject=subject,
            html_body=html,
            mailbox_name='campaignA'  # use dynamic if needed
        )
        return jsonify({"status": "sent"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 4. Serve React frontend ---
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# --- 5. Optional: Shut down Flask after idle timeout (5 mins) ---
import threading
import time

def idle_killer(timeout=300):
    last_request_time = time.time()

    def update_timer():
        nonlocal last_request_time
        last_request_time = time.time()

    def monitor():
        while True:
            if time.time() - last_request_time > timeout:
                print("💀 Server idle. Shutting down...")
                os._exit(0)
            time.sleep(10)

    app.before_request(update_timer)
    threading.Thread(target=monitor, daemon=True).start()

idle_killer(timeout=300)

# --- 6. Start server ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
