from database import get_db_connection


# =========================================================
# GET ALL DEVICES
# =========================================================

def get_all_devices():

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute("""
            SELECT
                device_id,
                device_code,
                device_name,
                total_quantity,
                available_quantity,
                created_at
            FROM devices
            ORDER BY device_id ASC
        """)

        return cursor.fetchall()

    finally:

        cursor.close()
        connection.close()


# =========================================================
# GET DEVICE BY ID
# =========================================================

def get_device_by_id(device_id):

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute("""
            SELECT
                device_id,
                device_code,
                device_name,
                total_quantity,
                available_quantity,
                created_at
            FROM devices
            WHERE device_id = %s
            LIMIT 1
        """, (device_id,))

        return cursor.fetchone()

    finally:

        cursor.close()
        connection.close()


# =========================================================
# GET DEVICE BY CODE
# =========================================================

def get_device_by_code(device_code):

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute("""
            SELECT
                device_id,
                device_code,
                device_name,
                total_quantity,
                available_quantity,
                created_at
            FROM devices
            WHERE device_code = %s
            LIMIT 1
        """, (device_code,))

        return cursor.fetchone()

    finally:

        cursor.close()
        connection.close()


# =========================================================
# ADD DEVICE
# =========================================================

def add_device(
    device_code,
    device_name,
    quantity
):

    connection = get_db_connection()

    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO devices
            (
                device_code,
                device_name,
                total_quantity,
                available_quantity
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
        """, (
            device_code,
            device_name,
            quantity,
            quantity
        ))

        connection.commit()

        return cursor.lastrowid

    except Exception:

        connection.rollback()

        raise

    finally:

        cursor.close()
        connection.close()


# =========================================================
# UPDATE DEVICE
# =========================================================

def update_device(
    device_id,
    device_name,
    total_quantity
):

    connection = get_db_connection()

    cursor = connection.cursor()

    try:

        # Get current device
        cursor.execute("""
            SELECT
                total_quantity,
                available_quantity
            FROM devices
            WHERE device_id = %s
            LIMIT 1
        """, (device_id,))

        device = cursor.fetchone()


        if not device:

            raise ValueError(
                "Device not found."
            )


        old_total = int(
            device[0]
        )

        old_available = int(
            device[1]
        )


        borrowed = (
            old_total -
            old_available
        )


        new_total = int(
            total_quantity
        )


        if new_total < borrowed:

            raise ValueError(
                "Total quantity cannot be less than currently borrowed quantity."
            )


        new_available = (
            new_total -
            borrowed
        )


        cursor.execute("""
            UPDATE devices
            SET
                device_name = %s,
                total_quantity = %s,
                available_quantity = %s
            WHERE device_id = %s
        """, (
            device_name,
            new_total,
            new_available,
            device_id
        ))


        connection.commit()

        return True

    except Exception:

        connection.rollback()

        raise

    finally:

        cursor.close()
        connection.close()


# =========================================================
# DELETE DEVICE
# =========================================================

def delete_device(device_id):

    connection = get_db_connection()

    cursor = connection.cursor()

    try:

        cursor.execute("""
            DELETE FROM devices
            WHERE device_id = %s
        """, (device_id,))


        connection.commit()

        return cursor.rowcount > 0

    except Exception:

        connection.rollback()

        raise

    finally:

        cursor.close()
        connection.close()