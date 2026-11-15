from src.database import get_connection


# Add a new call record
def add_call(customer_id, call_type, duration_seconds, status, summary):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO calls (
            customer_id,
            call_type,
            duration_seconds,
            status,
            summary
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            customer_id,
            call_type,
            duration_seconds,
            status,
            summary
        )
    )

    connection.commit()

    call_id = cursor.lastrowid

    connection.close()

    return {
        "call_id": call_id,
        "customer_id": customer_id,
        "call_type": call_type,
        "duration_seconds": duration_seconds,
        "status": status,
        "summary": summary,
        "message": "Call record saved successfully"
    }


# Get all call records
def get_all_calls():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM calls ORDER BY call_id"
    )

    calls = cursor.fetchall()

    connection.close()

    return calls


# Get calls for a specific customer
def get_customer_calls(customer_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM calls
        WHERE customer_id = ?
        ORDER BY call_id
        """,
        (customer_id,)
    )

    calls = cursor.fetchall()

    connection.close()

    return calls