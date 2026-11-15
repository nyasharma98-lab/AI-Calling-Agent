import sqlite3
from src.database import get_connection


# Add a new customer
def add_customer(name, phone):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO customers (name, phone)
            VALUES (?, ?)
            """,
            (name, phone)
        )

        connection.commit()

        customer_id = cursor.lastrowid

        return {
            "customer_id": customer_id,
            "name": name,
            "phone": phone,
            "message": "Customer added successfully"
        }

    except sqlite3.IntegrityError:
        return {
            "error": "Phone number already exists"
        }

    finally:
        connection.close()


# Get all customers
def get_all_customers():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM customers ORDER BY customer_id"
    )

    customers = cursor.fetchall()

    connection.close()

    return customers


# Search customer by ID
def get_customer_by_id(customer_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM customers WHERE customer_id = ?",
        (customer_id,)
    )

    customer = cursor.fetchone()

    connection.close()

    return customer