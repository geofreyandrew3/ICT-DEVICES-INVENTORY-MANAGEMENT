import mysql.connector
from mysql.connector import Error

from config import (
    DB_HOST,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
    DB_PORT
)


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db_connection():

    connection = mysql.connector.connect(

        host=DB_HOST,

        user=DB_USER,

        password=DB_PASSWORD,

        database=DB_NAME,

        port=DB_PORT

    )

    return connection


# ==========================================
# INITIALIZE DATABASE TABLES
# ==========================================

def initialize_database():

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor()

        # ==================================
        # USERS TABLE
        # ==================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (

                user_id INT AUTO_INCREMENT PRIMARY KEY,

                full_name VARCHAR(150) NOT NULL,

                phone VARCHAR(30) NOT NULL,

                email VARCHAR(150) NOT NULL UNIQUE,

                password VARCHAR(255) NOT NULL,

                role VARCHAR(30) NOT NULL DEFAULT 'user',

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP

            )
        """)


        # ==================================
        # ADD ROLE IF OLD TABLE EXISTS
        # ==================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.COLUMNS

            WHERE TABLE_SCHEMA = %s

            AND TABLE_NAME = 'users'

            AND COLUMN_NAME = 'role'
        """, (DB_NAME,))

        role_exists = cursor.fetchone()[0]


        if role_exists == 0:

            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN role
                VARCHAR(30)
                NOT NULL
                DEFAULT 'user'
                AFTER password
            """)


        # ==================================
        # DEVICES TABLE
        # ==================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS devices (

                device_id INT AUTO_INCREMENT PRIMARY KEY,

                device_code VARCHAR(50)
                    NOT NULL UNIQUE,

                device_name VARCHAR(100)
                    NOT NULL,

                total_quantity INT
                    NOT NULL DEFAULT 0,

                available_quantity INT
                    NOT NULL DEFAULT 0,

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP

            )
        """)


        # ==================================
        # BORROWING TABLE
        # ==================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrowing (

                borrowing_id INT AUTO_INCREMENT PRIMARY KEY,

                user_id INT NOT NULL,

                device_id INT NOT NULL,

                quantity INT NOT NULL,

                borrow_date DATE NOT NULL,

                borrow_time TIME NOT NULL,

                status VARCHAR(30)
                    NOT NULL DEFAULT 'Borrowed',

                FOREIGN KEY (user_id)
                    REFERENCES users(user_id)

                    ON DELETE CASCADE,

                FOREIGN KEY (device_id)
                    REFERENCES devices(device_id)

                    ON DELETE CASCADE

            )
        """)


        # ==================================
        # FEEDBACK TABLE
        # ==================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (

                feedback_id INT AUTO_INCREMENT PRIMARY KEY,

                user_id INT NULL,

                full_name VARCHAR(150) NOT NULL,

                email VARCHAR(150) NOT NULL,

                description TEXT NOT NULL,

                submitted_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                    REFERENCES users(user_id)

                    ON DELETE SET NULL

            )
        """)


        # ==================================
        # DEFAULT DEVICES
        # ==================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM devices
        """)

        result = cursor.fetchone()

        device_count = result[0]


        if device_count == 0:

            devices = [

                (
                    "DEV001",
                    "Computer",
                    20,
                    20
                ),

                (
                    "DEV002",
                    "Printer",
                    10,
                    10
                ),

                (
                    "DEV003",
                    "Other",
                    5,
                    5
                )

            ]


            cursor.executemany("""
                INSERT INTO devices
                (
                    device_code,
                    device_name,
                    total_quantity,
                    available_quantity
                )

                VALUES
                (%s, %s, %s, %s)

            """, devices)


        connection.commit()

        print(
            "Database tables initialized successfully."
        )


    except Error as error:

        print(
            "Database initialization error:",
            error
        )


    finally:

        if cursor:

            cursor.close()


        if connection:

            connection.close()