from src.call_manager import add_call


# Simulate a customer call
def simulate_call(
    customer_id,
    call_type,
    duration_seconds,
    summary
):

    status = "completed"

    # Save call details in database
    add_call(
        customer_id,
        call_type,
        duration_seconds,
        status,
        summary
    )

    print("Call executed successfully!")

    return {
        "customer_id": customer_id,
        "call_type": call_type,
        "duration_seconds": duration_seconds,
        "status": status,
        "summary": summary
    }