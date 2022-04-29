# Author: Alex Xu
# Description: This file is the main entry of cloud platform.

from flask import Flask
import secrets
from datetime import timedelta
from admin.admin import admin
from device.device import device

app = Flask(__name__)
app.register_blueprint(admin)
app.register_blueprint(device)

app.config["SECRET_KEY"] = secrets.token_urlsafe(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
