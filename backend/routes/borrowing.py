from flask import Blueprint, request, jsonify

from models.user import (
    get_user_by_email,
    get_user_by_id
)

from models.device import (
    get_device_by_id
)

from models.borrowing import (
    borrow_device,
    get_user_borrowings,
    get_all_borrowings
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

    # -------------------------------------------------
    # GET USER INFORMATION
    # -------------------------------------------------

    user_id = data.get("user_id")

    email = str(
        data.get(
            "email",
            ""
        )
    ).strip().lower()

    # -------------------------------------------------
    # GET DEVICE INFORMATION
    # -------------------------------------------------

    device_id = data.get(
        "device_id"
    )

    quantity = data.get(
        "quantity"
    )

    # =================================================
    # VALIDATE USER
    # =================================================

    if not user_id and not email:

        return jsonify({

            "success": False,

            "message":
                "User ID or email is required."

        }), 400

    # =================================================
    # VALIDATE DEVICE ID
    # =================================================

    try:

        device_id = int(
            device_id
        )

    except (
        ValueError,
        TypeError
    ):

        return jsonify({

            "success": False,

            "message":
                "Invalid device ID."

        }), 400

    # =================================================
    # VALIDATE QUANTITY
    # =================================================

    try:

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
                "Invalid quantity."

        }), 400

    # =================================================
    # CHECK QUANTITY
    # =================================================

    if quantity <= 0:

        return jsonify({

            "success": False,

            "message":
                "Quantity must be greater than zero."

        }), 400

    # =================================================
    # PROCESS BORROWING
    # =================================================

    try:

        # -------------------------------------------------
        # FIND USER
        # -------------------------------------------------

        user = None

        if user_id:

            try:

                user = get_user_by_id(
                    int(user_id)
                )

            except (
                ValueError,
                TypeError
            ):

                user = None

        # -------------------------------------------------
        # IF USER ID FAILED, TRY EMAIL
        # -------------------------------------------------

        if not user and email:

            user = get_user_by_email(
                email
            )

        # -------------------------------------------------
        # USER NOT FOUND
        # -------------------------------------------------

        if not user:

            return jsonify({

                "success": False,

                "message":
                    "User not found. "
                    "Please login again."

            }), 404

        # -------------------------------------------------
        # GET REAL USER ID
        # -------------------------------------------------

        real_user_id = user.get(
            "user_id"
        )

        if not real_user_id:

            return jsonify({

                "success": False,

                "message":
                    "Unable to identify user."

            }), 400

        # =================================================
        # CHECK DEVICE
        # =================================================

        device = get_device_by_id(
            device_id
        )

        if not device:

            return jsonify({

                "success": False,

                "message":
                    "Device not found."

            }), 404

        # =================================================
        # CHECK AVAILABLE QUANTITY
        # =================================================

        available_quantity = int(
            device.get(
                "available_quantity",
                0
            )
        )

        if available_quantity <= 0:

            return jsonify({

                "success": False,

                "message":
                    "This device is currently "
                    "not available."

            }), 400

        if quantity > available_quantity:

            return jsonify({

                "success": False,

                "message":
                    f"Only {available_quantity} "
                    f"device(s) are available."

            }), 400

        # =================================================
        # BORROW DEVICE
        # =================================================

        result = borrow_device(

            real_user_id,

            device_id,

            quantity

        )

        # -------------------------------------------------
        # CHECK RESULT
        # -------------------------------------------------

        if not result:

            return jsonify({

                "success": False,

                "message":
                    "Unable to process borrowing request."

            }), 500

        if isinstance(result, dict):

            if not result.get(
                "success",
                True
            ):

                return jsonify(
                    result
                ), 400

            return jsonify(
                result
            ), 200

        # -------------------------------------------------
        # FALLBACK SUCCESS RESPONSE
        # -------------------------------------------------

        return jsonify({

            "success": True,

            "message":
                "Device borrowed successfully.",

            "result":
                result

        }), 200

    # =================================================
    # ERROR
    # =================================================

    except Exception as error:

        print(
            "Borrowing error:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                str(error)

        }), 500


# =====================================================
# GET USER BORROWING REPORT BY EMAIL
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

        # =================================================
        # FIND USER
        # =================================================

        user = get_user_by_email(
            email
        )

        if not user:

            return jsonify({

                "success": False,

                "message":
                    "User not found."

            }), 404

        # =================================================
        # GET USER BORROWINGS
        # =================================================

        borrowings = get_user_borrowings(
            user["user_id"]
        )

        # =================================================
        # RETURN REPORT
        # =================================================

        return jsonify({

            "success": True,

            "borrowings":
                borrowings or []

        }), 200

    except Exception as error:

        print(
            "User borrowing report error:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                str(error)

        }), 500


# =====================================================
# GET USER BORROWING REPORT BY USER ID
# =====================================================

@borrowing_bp.route(
    "/user/<int:user_id>",
    methods=["GET"]
)
def user_borrowing_report_by_id(
    user_id
):

    try:

        # =================================================
        # FIND USER
        # =================================================

        user = get_user_by_id(
            user_id
        )

        if not user:

            return jsonify({

                "success": False,

                "message":
                    "User not found."

            }), 404

        # =================================================
        # GET BORROWINGS
        # =================================================

        borrowings = get_user_borrowings(
            user_id
        )

        # =================================================
        # RETURN DATA
        # =================================================

        return jsonify({

            "success": True,

            "borrowings":
                borrowings or []

        }), 200

    except Exception as error:

        print(
            "User borrowing report by ID error:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                str(error)

        }), 500


# =====================================================
# GET ALL BORROWING RECORDS
# =====================================================

@borrowing_bp.route(
    "/all",
    methods=["GET"]
)
def all_borrowings():

    try:

        borrowings = get_all_borrowings()

        return jsonify({

            "success": True,

            "borrowings":
                borrowings or []

        }), 200

    except Exception as error:

        print(
            "Get all borrowings error:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                str(error)

        }), 500