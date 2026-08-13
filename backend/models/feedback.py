from database import get_db_connection


# ==========================================
# CREATE FEEDBACK
# ==========================================

def create_feedback(
    user_id,
    full_name,
    email,
    description
):

    connection = get_db_connection()

    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO feedback
            (
                user_id,
                full_name,
                email,
                description
            )

            VALUES
            (%s, %s, %s, %s)

        """, (
            user_id,
            full_name,
            email,
            description
        ))


        connection.commit()

        return cursor.lastrowid


    finally:

        cursor.close()

        connection.close()


# ==========================================
# GET ALL FEEDBACK
# ==========================================

def get_all_feedback():

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute("""
            SELECT

                feedback_id,

                user_id,

                full_name,

                email,

                description,

                submitted_at

            FROM feedback

            ORDER BY
                feedback_id DESC

        """)


        return cursor.fetchall()


    finally:

        cursor.close()

        connection.close()


# ==========================================
# GET USER FEEDBACK
# ==========================================

def get_user_feedback(user_id):

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute("""
            SELECT

                feedback_id,

                full_name,

                email,

                description,

                submitted_at

            FROM feedback

            WHERE user_id = %s

            ORDER BY
                feedback_id DESC

        """, (user_id,))


        return cursor.fetchall()


    finally:

        cursor.close()

        connection.close()