import bcrypt
from database import get_connection


def register_user(full_name, email, password):
    full_name = full_name.strip()
    email = email.strip().lower()

    if not full_name or not email or not password:
        return False, "All fields are required."

    if len(password) < 8:
        return False, "Password must be at least 8 characters."

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO users (full_name, email, password_hash)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (full_name, email, password_hash))
        connection.commit()

        return True, "Account created successfully."

    except Exception as error:
        if connection is not None:
            connection.rollback()

        if getattr(error, "errno", None) == 1062:
            return False, "This email is already registered."

        print("Registration error:", error)
        return False, "Could not create account. Check the database connection."

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def login_user(email, password):
    email = email.strip().lower()

    if not email or not password:
        return None, "Enter your email and password."

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT user_id, full_name, email, password_hash
            FROM users
            WHERE email = %s
        """

        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user is None:
            return None, "Invalid email or password."

        password_matches = bcrypt.checkpw(
            password.encode("utf-8"),
            user["password_hash"].encode("utf-8")
        )

        if not password_matches:
            return None, "Invalid email or password."

        user.pop("password_hash")
        return user, "Login successful."

    except Exception as error:
        print("Login error:", error)
        return None, "Could not log in. Check the database connection."

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()