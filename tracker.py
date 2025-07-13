from flask import Flask, request, send_file, redirect
from database import mark_email_opened, unsubscribe_user
from io import BytesIO

app = Flask(__name__)


# 1. Track opens via tracking pixel
@app.route('/open/<message_id>')
def track_open(message_id):
    print(f"Tracking open for message_id: {message_id}")
    mark_email_opened(message_id)

    # Return a 1x1 transparent pixel
    pixel = BytesIO(
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF'
        b'\x21\xF9\x04\x01\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4C\x01\x00\x3B'
    )
    return send_file(pixel, mimetype='image/gif')


# 2. Unsubscribe via link
@app.route('/unsubscribe')
def unsubscribe():
    email = request.args.get('email')
    if email:
        unsubscribe_user(email)
        return f"<h3>{email} successfully unsubscribed from future emails.</h3>"
    else:
        return "<h3>Missing email parameter.</h3>", 400


if __name__ == '__main__':
    app.run(port=5000)
