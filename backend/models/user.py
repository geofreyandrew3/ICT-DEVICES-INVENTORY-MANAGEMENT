from database import get_db_connection


# ==========================================
# CREATE USER
# ==========================================

def create_user(
    full_name,
    phone,
    email,
    password
):

    connection = get_db_connection()

    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO users
            (
                full_name,
                phone,
                email,
                password,
                role
            )

            VALUES
            (%s, %s, %s, %s, %s)

        """, (
            full_name,
            phone,
            email,
            password,
            "user"
        ))


        connection.commit()

        return cursor.lastrowid


    finally:

        cursor.close()

        connection.close()


# ==========================================
# FIND USER BY EMAIL
# ==========================================

def get_user_by_email(email):

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute("""
            SELECT

                user_id,

                full_name,

                phone,

                email,

                password,

                role,

                created_at

            FROM users

            WHERE email = %s

            LIMIT 1

        """, (email,))


        return cursor.fetchone()


    finally:

        cursor.close()

        connection.close()


# ==========================================
# FIND USER BY ID
# ==========================================

def get_user_by_id(user_id):

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute("""
            SELECT

                user_id,

                full_name,

                phone,

                email,

                role,

                created_at

            FROM users

            WHERE user_id = %s

            LIMIT 1

        """, (user_id,))


        return cursor.fetchone()


    finally:

        cursor.close()

        connection.close()


# ==========================================
# GET ALL USERS
# ==========================================

def get_all_users():

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute("""
            SELECT

                user_id,

                full_name,

                phone,

                email,

                role,

                created_at

            FROM users

            ORDER BY user_id DESC

        """)


        return cursor.fetchall()


    finally:

        cursor.close()

        connection.close()