from flask import Blueprint, request, jsonify

from models.user import (
    get_user_by_email
)

from models.feedback import (
    create_feedback,
    get_all_feedback
)


feedback_bp = Blueprint(
    "feedback",
    __name__,
    url_prefix="/api/feedback"
)


# ==========================================
# SUBMIT FEEDBACK
# ==========================================

@feedback_bp.route(
    "",
    methods=["POST"]
)
def submit_feedback():

    data = request.get_json() or {}


    full_name = data.get(
        "full_name",
        ""
    ).strip()


    email = data.get(
        "email",
        ""
    ).strip().lower()


    description = data.get(
        "description",
        ""
    ).strip()


    # --------------------------------------
    # VALIDATION
    # --------------------------------------

    if not full_name:

        return jsonify({

            "success": False,

            "message":
                "Full name is required."

        }), 400


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


    # --------------------------------------
    # FIND USER
    # --------------------------------------

    user = get_user_by_email(
        email
    )


    user_id = None

    if user:

        user_id = user["user_id"]


    # --------------------------------------
    # SAVE FEEDBACK
    # --------------------------------------

    try:

        feedback_id = create_feedback(

            user_id,

            full_name,

            email,

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


# ==========================================
# GET ALL FEEDBACK
# ==========================================

@feedback_bp.route(
    "",
    methods=["GET"]
)
def all_feedback():

    try:

        feedback = get_all_feedback()


        return jsonify({

            "success": True,

            "feedback": feedback

        })


    except Exception as error:

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500