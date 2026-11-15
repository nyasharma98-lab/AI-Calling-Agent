from pathlib import Path

from src.call_analysis import load_call_data


# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Reports directory
REPORTS_DIR = BASE_DIR / "reports"

# CSV report location
CSV_PATH = REPORTS_DIR / "call_analytics_report.csv"


# Generate CSV analytics report
def generate_csv_report():

    # Get call records
    df = load_call_data()

    # Create reports folder if it does not exist
    REPORTS_DIR.mkdir(exist_ok=True)

    # Save call records as CSV
    df.to_csv(CSV_PATH, index=False)

    return CSV_PATH