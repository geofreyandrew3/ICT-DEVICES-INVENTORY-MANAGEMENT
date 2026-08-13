from database import get_db_connection


# =====================================================
# CREATE ADMIN NOTIFICATION
# =====================================================

def create_admin_notification(
    title,
    message
):

    connection = get_db_connection()

    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO notifications
            (
                title,
                message,
                is_read
            )

            VALUES
            (
                %s,
                %s,
                %s
            )

        """, (
            title,
            message,
            0
        ))

        connection.commit()

        return True

    except Exception:

        connection.rollback()

        return False

    finally:

        cursor.close()
        connection.close()


# =====================================================
# GET ADMIN NOTIFICATIONS
# =====================================================

def get_admin_notifications():

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    try:

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

        """)

        return cursor.fetchall()

    finally:

        cursor.close()
        connection.close()


# =====================================================
# MARK NOTIFICATION AS READ
# =====================================================

def mark_notification_read(
    notification_id
):

    connection = get_db_connection()

    cursor = connection.cursor()

    try:

        cursor.execute("""
            UPDATE notifications

            SET is_read = 1

            WHERE notification_id = %s

        """, (
            notification_id,
        ))

        connection.commit()

        return True

    except Exception:

        connection.rollback()

        return False

    finally:

        cursor.close()
        connection.close()