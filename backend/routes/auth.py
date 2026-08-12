from flask import Blueprint, request, jsonify

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models.user import (
    create_user,
    get_user_by_email
)


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


# ==========================================
# REGISTER
# ==========================================

@auth_bp.route(
    "/register",
    methods=["POST"]
)
def register():

    data = request.get_json() or {}


    full_name = data.get(
        "full_name",
        ""
    ).strip()


    phone = data.get(
        "phone",
        ""
    ).strip()


    email = data.get(
        "email",
        ""
    ).strip().lower()


    password = data.get(
        "password",
        ""
    )


    # --------------------------------------
    # VALIDATION
    # --------------------------------------

    if not full_name:

        return jsonify({
            "success": False,
            "message": "Full name is required."
        }), 400


    if not phone:

        return jsonify({
            "success": False,
            "message": "Phone number is required."
        }), 400


    if not email:

        return jsonify({
            "success": False,
            "message": "Email is required."
        }), 400


    if not password:

        return jsonify({
            "success": False,
            "message": "Password is required."
        }), 400


    if len(password) < 6:

        return jsonify({
            "success": False,
            "message":
                "Password must be at least 6 characters."
        }), 400


    # --------------------------------------
    # CHECK EXISTING USER
    # --------------------------------------

    existing_user = get_user_by_email(email)


    if existing_user:

        return jsonify({
            "success": False,
            "message":
                "Email is already registered."
        }), 409


    # --------------------------------------
    # HASH PASSWORD
    # --------------------------------------

    hashed_password = generate_password_hash(
        password
    )


    # --------------------------------------
    # CREATE USER
    # --------------------------------------

    try:

        user_id = create_user(
            full_name,
            phone,
            email,
            hashed_password
        )


        return jsonify({

            "success": True,

            "message":
                "Registration successful.",

            "user_id":
                user_id

        }), 201


    except Exception as error:

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500


# ==========================================
# LOGIN
# ==========================================

@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    data = request.get_json() or {}


    email = data.get(
        "email",
        ""
    ).strip().lower()


    password = data.get(
        "password",
        ""
    )


    if not email or not password:

        return jsonify({

            "success": False,

            "message":
                "Email and password are required."

        }), 400


    user = get_user_by_email(email)


    if not user:

        return jsonify({

            "success": False,

            "message":
                "Invalid email or password."

        }), 401


    if not check_password_hash(
        user["password"],
        password
    ):

        return jsonify({

            "success": False,

            "message":
                "Invalid email or password."

        }), 401


    return jsonify({

        "success": True,

        "message":
            "Login successful.",

        "user": {

            "user_id":
                user["user_id"],

            "full_name":
                user["full_name"],

            "phone":
                user["phone"],

            "email":
                user["email"]

        }

    })