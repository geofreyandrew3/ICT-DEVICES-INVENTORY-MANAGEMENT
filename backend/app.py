from flask import Flask, jsonify

from flask_cors import CORS

from database import initialize_database


# ==========================================
# IMPORT ROUTES
# ==========================================

from routes.auth import auth_bp

from routes.devices import devices_bp

from routes.borrowing import borrowing_bp

from routes.reports import reports_bp

from routes.feedback import feedback_bp

from routes.admin import admin_bp


# ==========================================
# CREATE FLASK APP
# ==========================================

app = Flask(__name__)


# ==========================================
# ENABLE CORS
# ==========================================

CORS(app)


# ==========================================
# REGISTER BLUEPRINTS
# ==========================================

app.register_blueprint(
    auth_bp
)

app.register_blueprint(
    devices_bp
)

app.register_blueprint(
    borrowing_bp
)

app.register_blueprint(
    reports_bp
)

app.register_blueprint(
    feedback_bp
)

app.register_blueprint(
    admin_bp
)


# ==========================================
# HOME / API STATUS
# ==========================================

@app.route("/")
def home():

    return jsonify({

        "success": True,

        "system":
            "ICT DEVICES MANAGEMENT",

        "status":
            "Backend is running",

        "database":
            "MySQL / XAMPP"

    })


# ==========================================
# DATABASE INITIALIZATION
# ==========================================

initialize_database()


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="127.0.0.1",

        port=5000

    )