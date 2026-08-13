from datetime import datetime

from database import get_db_connection


# ==========================================
# BORROW DEVICE
# ==========================================

def borrow_device(
    user_id,
    device_id,
    quantity
):

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        connection.start_transaction()


        # ==================================
        # VALIDATE QUANTITY
        # ==================================

        if quantity <= 0:

            connection.rollback()

            return {

                "success": False,

                "message":
                    "Quantity must be greater than zero."

            }


        # ==================================
        # GET DEVICE
        # ==================================

        cursor.execute("""
            SELECT

                device_id,

                device_code,

                device_name,

                available_quantity

            FROM devices

            WHERE device_id = %s

            FOR UPDATE

        """, (device_id,))


        device = cursor.fetchone()


        if not device:

            connection.rollback()

            return {

                "success": False,

                "message":
                    "Device not found."

            }


        # ==================================
        # CHECK AVAILABILITY
        # ==================================

        if quantity > device["available_quantity"]:

            connection.rollback()

            return {

                "success": False,

                "message":
                    f"Only "
                    f"{device['available_quantity']} "
                    f"{device['device_name']}(s) "
                    f"available."

            }


        # ==================================
        # CURRENT DATE AND TIME
        # ==================================

        now = datetime.now()

        borrow_date = now.date()

        borrow_time = now.time()


        # ==================================
        # INSERT BORROWING
        # ==================================

        cursor.execute("""
            INSERT INTO borrowing
            (
                user_id,
                device_id,
                quantity,
                borrow_date,
                borrow_time,
                status
            )

            VALUES
            (%s, %s, %s, %s, %s, %s)

        """, (
            user_id,
            device_id,
            quantity,
            borrow_date,
            borrow_time,
            "Borrowed"
        ))


        # ==================================
        # REDUCE AVAILABLE QUANTITY
        # ==================================

        cursor.execute("""
            UPDATE devices

            SET available_quantity =
                available_quantity - %s

            WHERE device_id = %s

        """, (
            quantity,
            device_id
        ))


        connection.commit()


        return {

            "success": True,

            "message":
                f"{device['device_name']} "
                f"successfully borrowed.",

            "device_name":
                device["device_name"],

            "quantity":
                quantity

        }


    except Exception as error:

        connection.rollback()

        return {

            "success": False,

            "message": str(error)

        }


    finally:

        cursor.close()

        connection.close()


# ==========================================
# GET USER BORROWING REPORT
# ==========================================

def get_user_borrowings(user_id):

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute("""
            SELECT

                borrowing.borrowing_id,

                devices.device_code,

                devices.device_name,

                borrowing.quantity,

                borrowing.borrow_date,

                borrowing.borrow_time,

                borrowing.status

            FROM borrowing

            INNER JOIN devices

                ON borrowing.device_id =
                   devices.device_id

            WHERE borrowing.user_id = %s

            ORDER BY
                borrowing.borrowing_id DESC

        """, (user_id,))


        return cursor.fetchall()


    finally:

        cursor.close()

        connection.close()


# ==========================================
# GET ALL BORROWINGS - ADMIN
# ==========================================

def get_all_borrowings():

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute("""
            SELECT

                borrowing.borrowing_id,

                users.full_name,

                users.email,

                devices.device_code,

                devices.device_name,

                borrowing.quantity,

                borrowing.borrow_date,

                borrowing.borrow_time,

                borrowing.status

            FROM borrowing

            INNER JOIN users

                ON borrowing.user_id =
                   users.user_id

            INNER JOIN devices

                ON borrowing.device_id =
                   devices.device_id

            ORDER BY
                borrowing.borrowing_id DESC

        """)


        return cursor.fetchall()


    finally:

        cursor.close()

        connection.close()