from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

# RECAPTCHA_SECRET = 'YOUR_SECRET_KEY'  # Replace with your reCAPTCHA v3 secret key
RECAPTCHA_SECRET = os.getenv('YOUR_SECRET_KEY')  # Read secret key from env var. 

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    token = request.form.get('recaptcha_token')

    verify_url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {
        'secret': RECAPTCHA_SECRET,
        'response': token
    }
    r = requests.post(verify_url, data=payload)
    result = r.json()

    score = result.get('score', 0)
    action = result.get('action')

    if result.get('success') and action == 'login' and score >= 0.5:
        return f"✅ Login allowed (score: {score:.2f})"
    else:
        return f"🚫 Suspicious activity detected (score: {score:.2f})", 403

if __name__ == '__main__':
    app.run(debug=True)
