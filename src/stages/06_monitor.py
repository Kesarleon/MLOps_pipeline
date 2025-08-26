import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, ClassificationPreset

def monitor_model():
    """
    This function generates a dashboard with data drift and classification performance.
    """
    # Load data
    train_df = pd.read_csv("data/processed/train.csv")
    test_df = pd.read_csv("data/processed/test.csv")

    # Create a report
    report = Report(
        metrics=[
            DataDriftPreset(),
            ClassificationPreset(),
        ]
    )

    # Run the report
    report.run(reference_data=train_df, current_data=test_df)

    # Save the report
    report.save_html("monitoring/dashboard.html")

if __name__ == "__main__":
    monitor_model()
