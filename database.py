"""MySQL access layer. Only feedback is stored; all queries are parameterized."""
import os
import mysql.connector
from mysql.connector import Error


class DatabaseError(Exception):
    """Raised for any DB problem so the app never shows raw MySQL errors."""


def get_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "covid_awareness_db"),
            connection_timeout=5,
        )
    except (Error, ValueError) as exc:
        raise DatabaseError("Could not connect to the database.") from exc


def save_feedback(name, email, category, message):
    """Insert one feedback row. %s placeholders prevent SQL injection."""
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO feedback (name, email, category, message) VALUES (%s, %s, %s, %s)",
            (name or None, email or None, category, message),
        )
        conn.commit()
    except Error as exc:
        raise DatabaseError("Could not save feedback.") from exc
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
