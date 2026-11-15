import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from src.call_manager import get_all_calls


# Step 1: Retrieve and organize call records
def load_call_data():

    calls = get_all_calls()

    columns = [
        "call_id",
        "customer_id",
        "call_type",
        "call_date",
        "duration_seconds",
        "status",
        "summary"
    ]

    df = pd.DataFrame(calls, columns=columns)

    return df


# Step 2: Analyze call records
def analyze_calls():

    df = load_call_data()

    if df.empty:
        return {
            "message": "No call records available."
        }

    total_calls = len(df)

    completed_calls = len(
        df[df["status"] == "completed"]
    )

    average_duration = np.mean(
        df["duration_seconds"]
    )

    total_duration = np.sum(
        df["duration_seconds"]
    )

    unique_customers = df["customer_id"].nunique()

    return {
        "total_calls": int(total_calls),
        "completed_calls": int(completed_calls),
        "average_duration": round(float(average_duration), 2),
        "total_duration": int(total_duration),
        "unique_customers": int(unique_customers)
    }


# Step 3: Generate call analysis charts
def generate_call_charts():

    df = load_call_data()

    if df.empty:
        print("No call records available for visualization.")
        return

    reports_folder = Path("reports")
    reports_folder.mkdir(exist_ok=True)

    # Chart 1: Calls by status
    status_counts = df["status"].value_counts()

    plt.figure(figsize=(8, 5))

    status_counts.plot(kind="bar")

    plt.title("Calls by Status")
    plt.xlabel("Call Status")
    plt.ylabel("Number of Calls")

    plt.tight_layout()

    plt.savefig(reports_folder / "calls_by_status.png")

    plt.close()

    # Chart 2: Average call duration
    plt.figure(figsize=(8, 5))

    df.groupby("call_type")["duration_seconds"].mean().plot(
        kind="bar"
    )

    plt.title("Average Call Duration")
    plt.xlabel("Call Type")
    plt.ylabel("Duration in Seconds")

    plt.tight_layout()

    plt.savefig(reports_folder / "average_call_duration.png")

    plt.close()

    print("Call analysis charts generated successfully!")


# Step 4: Display the call analysis report
def generate_call_report():

    report = analyze_calls()

    print("\n========== AI CALLING AGENT REPORT ==========\n")

    for key, value in report.items():
        print(f"{key}: {value}")

    print("\n=============================================\n")


if __name__ == "__main__":

    generate_call_report()

    generate_call_charts()