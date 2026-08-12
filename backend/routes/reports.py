from flask import Blueprint, request, jsonify

from models.user import (
    get_user_by_email
)

from models.borrowing import (
    get_user_borrowings
)


reports_bp = Blueprint(
    "reports",
    __name__,
    url_prefix="/api/reports"
)


# ==========================================
# MY REPORT
# ==========================================

@reports_bp.route(
    "",
    methods=["GET"]
)
def reports():

    email = request.args.get(
        "email",
        ""
    ).strip().lower()


    if not email:

        return jsonify({

            "success": False,

            "message":
                "Email is required."

        }), 400


    user = get_user_by_email(
        email
    )


    if not user:

        return jsonify({

            "success": False,

            "message":
                "User not found."

        }), 404


    borrowing_records = \
        get_user_borrowings(
            user["user_id"]
        )


    return jsonify({

        "success": True,

        "reports": borrowing_records

    })