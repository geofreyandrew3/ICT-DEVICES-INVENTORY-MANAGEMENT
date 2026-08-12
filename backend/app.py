from flask import Flask, jsonify

from database import initialize_database


# ==========================================
# IMPORT ROUTES
# ==========================================

from routes.auth import auth_bp

from routes.devices import devices_bp

from routes.borrowing import borrowing_bp

from routes.reports import reports_bp

from routes.feedback import feedback_bp


# ==========================================
# CREATE FLASK APP
# ==========================================

app = Flask(__name__)


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


# ==========================================
# HOME / API STATUS
# ==========================================

@app.route("/")
def home():

    return jsonify({

        "system":
            "ICT DEVICES MANAGEMENT",

        "status":
            "Backend is running",

        "database":
            "MySQL / XAMPP"

    })


# ==========================================
# INITIALIZE DATABASE
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