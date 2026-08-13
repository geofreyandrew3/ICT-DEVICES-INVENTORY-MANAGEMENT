from flask import Blueprint, request, jsonify

from models.user import (
    get_user_by_email
)

from models.feedback import (
    create_feedback,
    get_all_feedback,
    get_user_feedback
)


feedback_bp = Blueprint(
    "feedback",
    __name__,
    url_prefix="/api/feedback"
)


# =====================================================
# SUBMIT FEEDBACK
# =====================================================

@feedback_bp.route(
    "",
    methods=["POST"]
)
def submit_feedback():

    data = request.get_json(
        silent=True
    ) or {}


    email = str(
        data.get(
            "email",
            ""
        )
    ).strip().lower()


    description = str(
        data.get(
            "description",
            ""
        )
    ).strip()


    # =================================================
    # VALIDATION
    # =================================================

    if not email:

        return jsonify({

            "success": False,

            "message":
                "Email is required."

        }), 400


    if not description:

        return jsonify({

            "success": False,

            "message":
                "Feedback description is required."

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
                    "User account not found."

            }), 404


        # =============================================
        # GET USER INFORMATION FROM DATABASE
        # =============================================

        user_id = user["user_id"]

        full_name = user["full_name"]

        user_email = user["email"]


        # =============================================
        # SAVE FEEDBACK
        # =============================================

        feedback_id = create_feedback(

            user_id,

            full_name,

            user_email,

            description

        )


        return jsonify({

            "success": True,

            "message":
                "Feedback submitted successfully.",

            "feedback_id":
                feedback_id

        }), 201


    except Exception as error:

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500


# =====================================================
# GET ALL FEEDBACK - ADMIN
# =====================================================

@feedback_bp.route(
    "",
    methods=["GET"]
)
def all_feedback():

    try:

        feedback = get_all_feedback()


        return jsonify({

            "success": True,

            "feedback":
                feedback

        }), 200


    except Exception as error:

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500


# =====================================================
# GET USER FEEDBACK
# =====================================================

@feedback_bp.route(
    "/user",
    methods=["GET"]
)
def user_feedback():

    email = str(
        request.args.get(
            "email",
            ""
        )
    ).strip().lower()


    if not email:

        return jsonify({

            "success": False,

            "message":
                "Email is required."

        }), 400


    try:

        user = get_user_by_email(
            email
        )


        if not user:

            return jsonify({

                "success": False,

                "message":
                    "User not found."

            }), 404


        feedback = get_user_feedback(
            user["user_id"]
        )


        return jsonify({

            "success": True,

            "feedback":
                feedback

        }), 200


    except Exception as error:

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500