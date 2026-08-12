from flask import Blueprint, request, jsonify

from models.user import (
    get_user_by_email
)

from models.borrowing import (
    borrow_device
)


borrowing_bp = Blueprint(
    "borrowing",
    __name__,
    url_prefix="/api/borrowing"
)


# ==========================================
# BORROW DEVICE
# ==========================================

@borrowing_bp.route(
    "/borrow",
    methods=["POST"]
)
def borrow():

    data = request.get_json() or {}


    email = data.get(
        "email",
        ""
    ).strip().lower()


    device_id = data.get(
        "device_id"
    )


    quantity = data.get(
        "quantity"
    )


    # --------------------------------------
    # VALIDATION
    # --------------------------------------

    if not email:

        return jsonify({

            "success": False,

            "message":
                "Email is required."

        }), 400


    try:

        device_id = int(device_id)

        quantity = int(quantity)

    except:

        return jsonify({

            "success": False,

            "message":
                "Invalid device ID or quantity."

        }), 400


    # --------------------------------------
    # FIND USER
    # --------------------------------------

    user = get_user_by_email(email)


    if not user:

        return jsonify({

            "success": False,

            "message":
                "User not found. Please register first."

        }), 404


    # --------------------------------------
    # BORROW
    # --------------------------------------

    result = borrow_device(
        user["user_id"],
        device_id,
        quantity
    )


    if not result["success"]:

        return jsonify(result), 400


    return jsonify(result), 200