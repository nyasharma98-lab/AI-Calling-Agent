from src.call_manager import (
    add_call,
    get_all_calls,
    get_customer_calls
)
from src.call_analysis import analyze_calls
from src.visualization import generate_dashboard
from fastapi.responses import FileResponse
from src.database import initialize_database
from src.report_generator import generate_csv_report
from src.call_executor import simulate_call
from pydantic import BaseModel
from src.database import get_connection
from src.customer_manager import (
    add_customer,
    get_all_customers,
    get_customer_by_id
)
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi import FastAPI

# Create FastAPI application
app = FastAPI(
    title="AI Calling Agent",
    description="A Python-based AI Calling Agent",
    version="1.0.0"
)
# Call execution request model
class CallRequest(BaseModel):
    customer_id: int
    call_type: str
    duration_seconds: int
    summary: str

# Home API
@app.get("/")
def home():
    return {
        "project": "AI Calling Agent",
        "message": "Welcome to AI Calling Agent!",
        "status": "Running"
    }


# Health check API
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "API is working properly"
    }


# Project information API
@app.get("/about")
def about():
    return {
        "name": "AI Calling Agent",
        "language": "Python",
        "framework": "FastAPI",
        "database": "SQLite"
    }
# Initialize SQL database
initialize_database()


# Customer request model
class Customer(BaseModel):
    name: str
    phone: str


# Add customer API
@app.post("/customers")
def create_customer(customer: Customer):

    result = add_customer(customer.name, customer.phone)

    if "error" in result:
        raise HTTPException(
            status_code=409,
            detail=result["error"]
        )

    return result


# Get all customers API
@app.get("/customers")
def read_customers():

    return get_all_customers()


# Search customer API
@app.get("/customers/{customer_id}")
def read_customer(customer_id: int):

    customer = get_customer_by_id(customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer
# Call request model
class CallRecord(BaseModel):
    customer_id: int
    call_type: str
    duration_seconds: int
    status: str
    summary: str
    # Add new call API
@app.post("/calls")
def create_call(call: CallRecord):

    customer = get_customer_by_id(call.customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if call.duration_seconds < 0:
        raise HTTPException(
            status_code=400,
            detail="Call duration cannot be negative"
        )

    result = add_call(
        call.customer_id,
        call.call_type,
        call.duration_seconds,
        call.status,
        call.summary
    )

    return result
# View all calls API
@app.get("/calls")
def read_calls():

    return get_all_calls()
# View customer call history API
@app.get("/customers/{customer_id}/calls")
def read_customer_calls(customer_id: int):

    customer = get_customer_by_id(customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return get_customer_calls(customer_id)

# Call analytics API
@app.get("/analytics")
def read_call_analytics():
    return analyze_calls()


# Analytics Dashboard API
@app.get("/dashboard")
def get_dashboard():

    generate_dashboard()

    return FileResponse(
        "analytics_dashboard.png",
        media_type="image/png"
    )
# Download Analytics CSV Report
@app.get("/download-report")
def download_report():

    report_path = generate_csv_report()

    return FileResponse(
        path=report_path,
        filename="call_analytics_report.csv",
        media_type="text/csv"
    )
# Execute a call API
@app.post("/execute-call")
def execute_call_api(request: CallRequest):

    customer = get_customer_by_id(request.customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if request.duration_seconds < 0:
        raise HTTPException(
            status_code=400,
            detail="Call duration cannot be negative"
        )

    result = simulate_call(
        request.customer_id,
        request.call_type,
        request.duration_seconds,
        request.summary
    )

    return {
        "message": "Call execution completed",
        "result": result
    }
# Get executed call history
@app.get("/execution-history")
def get_execution_history():

    calls = get_all_calls()

    return {
        "total_executed_calls": len(calls),
        "execution_history": calls
    }
# Call execution statistics API
@app.get("/execution-statistics")
def execution_statistics():

    calls = get_all_calls()

    total_calls = len(calls)

    completed_calls = sum(
        1 for call in calls
        if call[5] == "completed"
    )

    return {
        "total_calls": total_calls,
        "completed_calls": completed_calls
    }
# Call performance summary API
@app.get("/call-performance")
def call_performance():

    calls = get_all_calls()

    total_calls = len(calls)

    completed_calls = sum(
        1 for call in calls
        if call[5] == "completed"
    )

    failed_calls = sum(
        1 for call in calls
        if call[5] == "failed"
    )

    pending_calls = sum(
        1 for call in calls
        if call[5] == "pending"
    )

    completion_rate = (
        (completed_calls / total_calls) * 100
        if total_calls > 0 else 0
    )

    return {
        "total_calls": total_calls,
        "completed_calls": completed_calls,
        "failed_calls": failed_calls,
        "pending_calls": pending_calls,
        "completion_rate": round(completion_rate, 2)
    }
# Average call duration API
@app.get("/average-call-duration")
def average_call_duration():

    calls = get_all_calls()

    total_calls = len(calls)

    if total_calls == 0:
        return {
            "total_calls": 0,
            "average_duration_seconds": 0
        }

    total_duration = sum(
        call[4] for call in calls
    )

    average_duration = total_duration / total_calls

    return {
        "total_calls": total_calls,
        "total_duration_seconds": total_duration,
        "average_duration_seconds": round(
            average_duration, 2
        )
    }
# Call duration analysis API
@app.get("/call-duration-analysis")
def call_duration_analysis():

    calls = get_all_calls()

    short_calls = sum(
        1 for call in calls
        if call[4] < 60
    )

    medium_calls = sum(
        1 for call in calls
        if 60 <= call[4] <= 180
    )

    long_calls = sum(
        1 for call in calls
        if call[4] > 180
    )

    return {
        "total_calls": len(calls),
        "short_calls": short_calls,
        "medium_calls": medium_calls,
        "long_calls": long_calls
    }

@app.get("/call-execution-summary")
def call_execution_summary():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM calls")
    calls = cursor.fetchall()

    connection.close()

    total_calls = len(calls)

    completed_calls = sum(
        1 for call in calls if call[5] == "completed"
    )

    failed_calls = sum(
        1 for call in calls if call[5] == "failed"
    )

    pending_calls = sum(
        1 for call in calls if call[5] == "pending"
    )

    total_duration = sum(
        call[4] for call in calls
    )

    average_duration = (
        total_duration // total_calls
        if total_calls > 0 else 0
    )

    return {
        "total_calls": total_calls,
        "completed_calls": completed_calls,
        "failed_calls": failed_calls,
        "pending_calls": pending_calls,
        "total_duration_seconds": total_duration,
        "average_duration_seconds": average_duration
    }
@app.get("/call-outcome-analysis")
def call_outcome_analysis():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM calls
        GROUP BY status
    """)

    results = cursor.fetchall()

    connection.close()

    outcome_counts = {
        "completed": 0,
        "failed": 0,
        "pending": 0
    }

    for status, count in results:
        outcome_counts[status] = count

    total_calls = sum(outcome_counts.values())

    outcome_percentages = {}

    for status, count in outcome_counts.items():

        percentage = (
            round((count / total_calls) * 100, 2)
            if total_calls > 0 else 0
        )

        outcome_percentages[status] = percentage

    return {
        "total_calls": total_calls,
        "outcome_counts": outcome_counts,
        "outcome_percentages": outcome_percentages
    }
@app.get("/call-outcome-distribution")
def call_outcome_distribution():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM calls
        GROUP BY status
    """)

    results = cursor.fetchall()

    connection.close()

    total_calls = sum(count for status, count in results)

    distribution = []

    for status, count in results:

        percentage = (
            round((count / total_calls) * 100, 2)
            if total_calls > 0 else 0
        )

        distribution.append({
            "status": status,
            "count": count,
            "percentage": percentage
        })

    return {
        "total_calls": total_calls,
        "distribution": distribution
    }
@app.get("/call-success-rate")
def call_success_rate():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END)
        FROM calls
    """)

    result = cursor.fetchone()

    connection.close()

    total_calls = result[0] or 0
    successful_calls = result[1] or 0

    success_rate = (
        round((successful_calls / total_calls) * 100, 2)
        if total_calls > 0 else 0
    )

    return {
        "total_calls": total_calls,
        "successful_calls": successful_calls,
        "success_rate_percentage": success_rate
    }
@app.get("/call-failure-rate")
def call_failure_rate():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END)
        FROM calls
    """)

    result = cursor.fetchone()

    connection.close()

    total_calls = result[0] or 0
    failed_calls = result[1] or 0

    failure_rate = (
        round((failed_calls / total_calls) * 100, 2)
        if total_calls > 0 else 0
    )

    return {
        "total_calls": total_calls,
        "failed_calls": failed_calls,
        "failure_rate_percentage": failure_rate
    }
@app.get("/call-pending-rate")
def call_pending_rate():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(
                CASE
                    WHEN status = 'pending' THEN 1
                    ELSE 0
                END
            )
        FROM calls
    """)

    result = cursor.fetchone()

    connection.close()

    total_calls = result[0] or 0
    pending_calls = result[1] or 0

    pending_rate = (
        round((pending_calls / total_calls) * 100, 2)
        if total_calls > 0 else 0
    )

    return {
        "total_calls": total_calls,
        "pending_calls": pending_calls,
        "pending_rate_percentage": pending_rate
    }
@app.get("/call-status-summary")
def call_status_summary():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END)
        FROM calls
    """)

    result = cursor.fetchone()

    connection.close()

    total_calls = result[0] or 0
    completed_calls = result[1] or 0
    failed_calls = result[2] or 0
    pending_calls = result[3] or 0

    success_rate = (
        round((completed_calls / total_calls) * 100, 2)
        if total_calls > 0 else 0
    )

    return {
        "total_calls": total_calls,
        "completed_calls": completed_calls,
        "failed_calls": failed_calls,
        "pending_calls": pending_calls,
        "success_rate_percentage": success_rate
    }
@app.get("/call-status-count")
def call_status_count():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status, COUNT(*) AS total
        FROM calls
        GROUP BY status
        ORDER BY status
    """)

    results = cursor.fetchall()

    connection.close()

    status_counts = {}

    for status, count in results:
        status_counts[status] = count

    return {
        "status_counts": status_counts
    }
@app.get("/call-status-percentage")
def call_status_percentage():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM calls
        GROUP BY status
    """)

    results = cursor.fetchall()

    connection.close()

    total_calls = sum(count for status, count in results)

    status_percentages = {}

    for status, count in results:

        percentage = (
            round((count / total_calls) * 100, 2)
            if total_calls > 0 else 0
        )

        status_percentages[status] = percentage

    return {
        "total_calls": total_calls,
        "status_percentages": status_percentages
    }
@app.get("/call-status-detailed-analysis")
def call_status_detailed_analysis():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM calls
        GROUP BY status
    """)

    results = cursor.fetchall()

    connection.close()

    total_calls = sum(count for status, count in results)

    status_analysis = {}

    for status, count in results:

        percentage = (
            round((count / total_calls) * 100, 2)
            if total_calls > 0 else 0
        )

        status_analysis[status] = {
            "count": count,
            "percentage": percentage
        }

    return {
        "total_calls": total_calls,
        "status_analysis": status_analysis
    }
@app.get("/overall-call-performance")
def overall_call_performance():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END),
            COALESCE(SUM(duration_seconds), 0),
            COALESCE(AVG(duration_seconds), 0)
        FROM calls
    """)

    result = cursor.fetchone()

    connection.close()

    total_calls = result[0] or 0
    completed_calls = result[1] or 0
    failed_calls = result[2] or 0
    pending_calls = result[3] or 0
    total_duration = result[4] or 0
    average_duration = round(result[5] or 0, 2)

    success_rate = (
        round((completed_calls / total_calls) * 100, 2)
        if total_calls > 0 else 0
    )

    failure_rate = (
        round((failed_calls / total_calls) * 100, 2)
        if total_calls > 0 else 0
    )

    return {
        "total_calls": total_calls,
        "completed_calls": completed_calls,
        "failed_calls": failed_calls,
        "pending_calls": pending_calls,
        "total_duration_seconds": total_duration,
        "average_duration_seconds": average_duration,
        "success_rate_percentage": success_rate,
        "failure_rate_percentage": failure_rate
    }
@app.get("/call-duration-by-status")
def call_duration_by_status():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            status,
            COUNT(*),
            COALESCE(SUM(duration_seconds), 0),
            COALESCE(AVG(duration_seconds), 0)
        FROM calls
        GROUP BY status
        ORDER BY status
    """)

    results = cursor.fetchall()

    connection.close()

    duration_analysis = {}

    for status, count, total_duration, average_duration in results:

        duration_analysis[status] = {
            "call_count": count,
            "total_duration_seconds": total_duration,
            "average_duration_seconds": round(average_duration, 2)
        }

    return {
        "duration_analysis": duration_analysis
    }
@app.get("/call-duration-performance")
def call_duration_performance():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(duration_seconds), 0),
            COALESCE(AVG(duration_seconds), 0),
            COALESCE(MIN(duration_seconds), 0),
            COALESCE(MAX(duration_seconds), 0)
        FROM calls
    """)

    result = cursor.fetchone()

    connection.close()

    total_calls = result[0] or 0
    total_duration = result[1] or 0
    average_duration = round(result[2] or 0, 2)
    shortest_call = result[3] or 0
    longest_call = result[4] or 0

    return {
        "total_calls": total_calls,
        "total_duration_seconds": total_duration,
        "average_duration_seconds": average_duration,
        "shortest_call_seconds": shortest_call,
        "longest_call_seconds": longest_call
    }
    print("AI CALLING AGENT MAIN FILE IS RUNNING")