from flask import Blueprint, request, jsonify

from models.user import get_all_users

from models.device import get_all_devices

from models.feedback import get_all_feedback

from models.borrowing import get_all_borrowings

from database import get_db_connection


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

            "users": users

        }), 200

    except Exception as error:

        return jsonify({

            "success": False,

            "message": str(error)

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

            "devices": devices

        }), 200

    except Exception as error:

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500


# =====================================================
# ADD NEW DEVICE
# =====================================================

@admin_bp.route(
    "/devices",
    methods=["POST"]
)
def add_device():

    data = request.get_json(
        silent=True
    ) or {}

    device_name = str(
        data.get(
            "device_name",
            ""
        )
    ).strip()

    category = str(
        data.get(
            "category",
            ""
        )
    ).strip()

    description = str(
        data.get(
            "description",
            ""
        )
    ).strip()

    total_quantity = data.get(
        "total_quantity"
    )


    # =================================================
    # VALIDATE DEVICE NAME
    # =================================================

    if not device_name:

        return jsonify({

            "success": False,

            "message":
                "Device name is required."

        }), 400


    # =================================================
    # VALIDATE QUANTITY
    # =================================================

    try:

        total_quantity = int(
            total_quantity
        )

    except (
        TypeError,
        ValueError
    ):

        return jsonify({

            "success": False,

            "message":
                "Total quantity must be a valid number."

        }), 400


    if total_quantity <= 0:

        return jsonify({

            "success": False,

            "message":
                "Total quantity must be greater than zero."

        }), 400


    connection = None
    cursor = None


    try:

        connection = get_db_connection()

        cursor = connection.cursor()


        # =================================================
        # INSERT DEVICE
        # =================================================

        cursor.execute("""
            INSERT INTO devices
            (
                device_name,
                total_quantity,
                available_quantity,
                category,
                description
            )

            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )

        """, (

            device_name,

            total_quantity,

            total_quantity,

            category,

            description

        ))


        connection.commit()


        device_id = cursor.lastrowid


        return jsonify({

            "success": True,

            "message":
                "Device added successfully.",

            "device_id":
                device_id

        }), 201


    except Exception as error:

        if connection:

            connection.rollback()


        return jsonify({

            "success": False,

            "message": str(error)

        }), 500


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


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

            "feedback": feedback

        }), 200


    except Exception as error:

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500


# =====================================================
# GET ALL BORROWINGS
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

            "borrowings": borrowings

        }), 200


    except Exception as error:

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500


# =====================================================
# ADMIN DASHBOARD STATISTICS
# =====================================================

@admin_bp.route(
    "/stats",
    methods=["GET"]
)
def get_stats():

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        # =================================================
        # TOTAL USERS
        # =================================================

        cursor.execute("""
            SELECT
                COUNT(*) AS total_users

            FROM users
        """)

        user_result = cursor.fetchone()


        # =================================================
        # TOTAL DEVICES
        # =================================================

        cursor.execute("""
            SELECT
                COALESCE(
                    SUM(total_quantity),
                    0
                ) AS total_devices

            FROM devices
        """)

        device_result = cursor.fetchone()


        # =================================================
        # BORROWED DEVICES
        # =================================================

        cursor.execute("""
            SELECT
                COALESCE(
                    SUM(quantity),
                    0
                ) AS borrowed_devices

            FROM borrowing

            WHERE LOWER(status) = 'borrowed'
        """)

        borrowed_result = cursor.fetchone()


        # =================================================
        # TOTAL FEEDBACK
        # =================================================

        cursor.execute("""
            SELECT
                COUNT(*) AS total_feedback

            FROM feedback
        """)

        feedback_result = cursor.fetchone()


        return jsonify({

            "success": True,

            "total_users":
                user_result["total_users"]
                if user_result
                else 0,

            "total_devices":
                device_result["total_devices"]
                if device_result
                else 0,

            "borrowed_devices":
                borrowed_result["borrowed_devices"]
                if borrowed_result
                else 0,

            "total_feedback":
                feedback_result["total_feedback"]
                if feedback_result
                else 0

        }), 200


    except Exception as error:

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# =====================================================
# ADMIN REPORTS
# =====================================================

@admin_bp.route(
    "/reports",
    methods=["GET"]
)
def get_reports():

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        # =================================================
        # DEVICE USAGE REPORT
        # =================================================

        cursor.execute("""
            SELECT

                devices.device_name,

                COALESCE(
                    SUM(borrowing.quantity),
                    0
                ) AS borrowed_quantity

            FROM devices

            LEFT JOIN borrowing

                ON devices.device_id =
                   borrowing.device_id

            GROUP BY

                devices.device_id,

                devices.device_name

            ORDER BY
                borrowed_quantity DESC
        """)

        device_usage = cursor.fetchall()


        # =================================================
        # BORROWING SUMMARY
        # =================================================

        cursor.execute("""
            SELECT

                status,

                COUNT(*) AS total

            FROM borrowing

            GROUP BY status

            ORDER BY total DESC
        """)

        borrowing_summary = cursor.fetchall()


        return jsonify({

            "success": True,

            "device_usage":
                device_usage,

            "borrowing_summary":
                borrowing_summary

        }), 200


    except Exception as error:

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# =====================================================
# GET ADMIN NOTIFICATIONS
# =====================================================

@admin_bp.route(
    "/notifications",
    methods=["GET"]
)
def get_notifications():

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        # =================================================
        # CHECK TABLE
        # =================================================

        cursor.execute("""
            SHOW TABLES LIKE 'notifications'
        """)

        table_exists = cursor.fetchone()


        if not table_exists:

            return jsonify({

                "success": True,

                "notifications": []

            }), 200


        # =================================================
        # GET NOTIFICATIONS
        #
        # IMPORTANT:
        # Table uses notification_id, NOT id.
        # =================================================

        cursor.execute("""
            SELECT

                notification_id AS id,

                title,

                message,

                is_read,

                created_at

            FROM notifications

            ORDER BY
                notification_id DESC

            LIMIT 50
        """)

        notifications = cursor.fetchall()


        return jsonify({

            "success": True,

            "notifications":
                notifications

        }), 200


    except Exception as error:

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# =====================================================
# MARK NOTIFICATION AS READ
# =====================================================

@admin_bp.route(
    "/notifications/<int:notification_id>/read",
    methods=["PATCH"]
)
def mark_notification_read(
    notification_id
):

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor()


        # =================================================
        # CHECK TABLE
        # =================================================

        cursor.execute("""
            SHOW TABLES LIKE 'notifications'
        """)

        table_exists = cursor.fetchone()


        if not table_exists:

            return jsonify({

                "success": False,

                "message":
                    "Notifications table does not exist."

            }), 404


        # =================================================
        # UPDATE NOTIFICATION
        #
        # IMPORTANT:
        # Use notification_id.
        # =================================================

        cursor.execute("""
            UPDATE notifications

            SET is_read = 1

            WHERE notification_id = %s

        """, (
            notification_id,
        ))


        connection.commit()


        # =================================================
        # CHECK RECORD
        # =================================================

        if cursor.rowcount == 0:

            return jsonify({

                "success": False,

                "message":
                    "Notification not found."

            }), 404


        return jsonify({

            "success": True,

            "message":
                "Notification marked as read."

        }), 200


    except Exception as error:

        if connection:

            connection.rollback()


        return jsonify({

            "success": False,

            "message": str(error)

        }), 500


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()