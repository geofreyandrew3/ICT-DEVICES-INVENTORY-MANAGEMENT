from database import get_db_connection


# ==========================================
# GET ALL DEVICES
# ==========================================

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


# ==========================================
# GET DEVICE BY ID
# ==========================================

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
                available_quantity

            FROM devices

            WHERE device_id = %s
        """, (device_id,))

        return cursor.fetchone()

    finally:

        cursor.close()
        connection.close()


# ==========================================
# ADD DEVICE
# ==========================================

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

            VALUES (%s, %s, %s, %s)
        """, (
            device_code,
            device_name,
            quantity,
            quantity
        ))

        connection.commit()

        return cursor.lastrowid

    finally:

        cursor.close()
        connection.close()