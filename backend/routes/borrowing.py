from flask import Blueprint, request, jsonify

from models.user import (
    get_user_by_email
)

from models.device import (
    get_device_by_id
)

from models.borrowing import (
    borrow_device,
    get_user_borrowings
)


# =====================================================
# BORROWING BLUEPRINT
# =====================================================

borrowing_bp = Blueprint(
    "borrowing",
    __name__,
    url_prefix="/api/borrowing"
)


# =====================================================
# BORROW DEVICE
# =====================================================

@borrowing_bp.route(
    "/borrow",
    methods=["POST"]
)
def borrow():

    data = request.get_json(
        silent=True
    ) or {}


    email = str(
        data.get(
            "email",
            ""
        )
    ).strip().lower()


    device_id = data.get(
        "device_id"
    )


    quantity = data.get(
        "quantity"
    )


    # =================================================
    # VALIDATE EMAIL
    # =================================================

    if not email:

        return jsonify({

            "success": False,

            "message":
                "Email is required."

        }), 400


    # =================================================
    # VALIDATE DEVICE AND QUANTITY
    # =================================================

    try:

        device_id = int(
            device_id
        )

        quantity = int(
            quantity
        )

    except (
        ValueError,
        TypeError
    ):

        return jsonify({

            "success": False,

            "message":
                "Invalid device ID or quantity."

        }), 400


    if quantity <= 0:

        return jsonify({

            "success": False,

            "message":
                "Quantity must be greater than zero."

        }), 400


    try:

        # =============================================
        # FIND USER
        # =============================================

        user = get_user_by_email(
            email
        )


        if not user:

            return jsonify({

                "success": False,

                "message":
                    "User not found. "
                    "Please register first."

            }), 404


        # =============================================
        # CHECK DEVICE
        # =============================================

        device = get_device_by_id(
            device_id
        )


        if not device:

            return jsonify({

                "success": False,

                "message":
                    "Device not found."

            }), 404


        # =============================================
        # BORROW DEVICE
        # =============================================

        result = borrow_device(

            user["user_id"],

            device_id,

            quantity

        )


        if not result["success"]:

            return jsonify(
                result
            ), 400


        return jsonify(
            result
        ), 200


    except Exception as error:

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500


# =====================================================
# GET USER BORROWING REPORT
# =====================================================

@borrowing_bp.route(
    "/user",
    methods=["GET"]
)
def user_borrowing_report():

    email = str(
        request.args.get(
            "email",
            ""
        )
    ).strip().lower()


    # =================================================
    # VALIDATE EMAIL
    # =================================================

    if not email:

        return jsonify({

            "success": False,

            "message":
                "Email is required."

        }), 400


    try:

        # =============================================
        # FIND USER
        # =============================================

        user = get_user_by_email(
            email
        )


        if not user:

            return jsonify({

                "success": False,

                "message":
                    "User not found."

            }), 404


        # =============================================
        # GET BORROWING RECORDS
        # =============================================

        borrowings = get_user_borrowings(
            user["user_id"]
        )


        return jsonify({

            "success": True,

            "borrowings":
                borrowings

        }), 200


    except Exception as error:

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500