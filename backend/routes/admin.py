from flask import Blueprint, jsonify

from models.user import (
    get_all_users
)

from models.device import (
    get_all_devices
)

from models.feedback import (
    get_all_feedback
)

from models.borrowing import (
    get_all_borrowings
)


# =====================================================
# ADMIN BLUEPRINT
# =====================================================

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/admin"
)


# =====================================================
# GET ALL USERS
# =====================================================

@admin_bp.route(
    "/users",
    methods=["GET"]
)
def get_users():

    try:

        users = get_all_users()


        return jsonify({

            "success": True,

            "users":
                users

        }), 200


    except Exception as error:

        return jsonify({

            "success": False,

            "message":
                str(error)

        }), 500


# =====================================================
# GET ALL DEVICES
# =====================================================

@admin_bp.route(
    "/devices",
    methods=["GET"]
)
def get_devices():

    try:

        devices = get_all_devices()


        return jsonify({

            "success": True,

            "devices":
                devices

        }), 200


    except Exception as error:

        return jsonify({

            "success": False,

            "message":
                str(error)

        }), 500


# =====================================================
# GET ALL FEEDBACK
# =====================================================

@admin_bp.route(
    "/feedback",
    methods=["GET"]
)
def get_feedback():

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

            "message":
                str(error)

        }), 500


# =====================================================
# GET ALL BORROWING RECORDS
# =====================================================

@admin_bp.route(
    "/borrowings",
    methods=["GET"]
)
def get_borrowings():

    try:

        borrowings = get_all_borrowings()


        return jsonify({

            "success": True,

            "borrowings":
                borrowings

        }), 200


    except Exception as error:

        return jsonify({

            "success": False,

            "message":
                str(error)

        }), 500