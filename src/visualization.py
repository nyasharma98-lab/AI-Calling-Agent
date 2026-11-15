import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from pathlib import Path

from src.call_analysis import analyze_calls, load_call_data


# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Dashboard image location
CHART_PATH = BASE_DIR / "analytics_dashboard.png"


# Generate analytics dashboard
def generate_dashboard():

    # Get analytics data
    analytics = analyze_calls()

    # Create dashboard
    fig, axes = plt.subplots(2, 2, figsize=(10, 6))

    fig.suptitle(
        "AI Calling Agent - Analytics Dashboard",
        fontsize=16,
        fontweight="bold"
    )

    # Dashboard metrics
    metrics = [
        ("Total Calls", analytics["total_calls"]),
        ("Completed Calls", analytics["completed_calls"]),
        ("Average Duration", f'{analytics["average_duration"]} sec'),
        ("Unique Customers", analytics["unique_customers"])
    ]

    fig.text(0.15, 0.90, f"Total Calls: {metrics[0][1]}", fontsize=11)
    fig.text(0.38, 0.90, f"Completed Calls: {metrics[1][1]}", fontsize=11)
    fig.text(0.60, 0.90, f"Average Duration: {metrics[2][1]}", fontsize=11)
    fig.text(0.82, 0.90, f"Unique Customers: {metrics[3][1]}", fontsize=11)

    # Load call data
    df = load_call_data()

    if not df.empty:

        # Chart 1: Call Status Distribution
        status_counts = df["status"].value_counts()

        axes[0, 0].clear()

        axes[0, 0].pie(
            status_counts,
            labels=status_counts.index,
            autopct="%1.1f%%",
            startangle=90
        )

        axes[0, 0].set_title("Call Status Distribution")

        # Chart 2: Average Call Duration
        duration_data = df.groupby("call_type")["duration_seconds"].mean()

        axes[0, 1].clear()

        duration_data.plot(
            kind="bar",
            ax=axes[0, 1]
        )

        axes[0, 1].set_title("Average Call Duration")
        axes[0, 1].set_xlabel("Call Type")
        axes[0, 1].set_ylabel("Duration (seconds)")

        # Chart 3: Calls Per Customer
        customer_counts = df.groupby("customer_id").size()

        axes[1, 0].clear()

        axes[1, 0].bar(
            customer_counts.index.astype(str),
            customer_counts.values
        )

        axes[1, 0].set_title("Calls Per Customer")
        axes[1, 0].set_xlabel("Customer ID")
        axes[1, 0].set_ylabel("Number of Calls")

        # Hide unused fourth panel
        axes[1, 1].axis("off")

    # Adjust dashboard layout
    plt.tight_layout(rect=[0, 0, 1, 0.85])

    # Save dashboard
    plt.savefig(CHART_PATH)

    plt.close()