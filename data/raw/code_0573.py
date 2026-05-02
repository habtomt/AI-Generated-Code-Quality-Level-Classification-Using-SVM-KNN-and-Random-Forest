"""
Auto-generated Python code
Scenario : Serverless Deployment
Prompt   : response_002.txt
Run      : 1
"""

# Import necessary libraries
import schedule
import time
from sqlalchemy import create_engine
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy import text

# Setup the database engine
DATABASE_URI = 'postgresql://YOUR_USER:YOUR_PASSWORD@localhost/YOUR_DBNAME'
engine = create_engine(DATABASE_URI)

# Function to retrieve data from the database
def fetch_data():
    query = "SELECT * FROM your_table"
    with engine.connect() as connection:
        # execute the query and fetch one row
        data = connection.execute(text(query)).fetchall()
        # convert to pandas DataFrame
        df = pd.DataFrame([dict(row) for row in data])
    return df

# Function to generate a report from the data
def generate_report(data):
    # Define the file path
    report_file = 'report.pdf'

    # Create a PDF report
    c = canvas.Canvas(report_file, pagesize=letter)
    c.setFont("Helvetica", 12)

    # Add content to the PDF
    text = c.beginText(50, 750)
    text.setFont("Helvetica", 12)
    text.setLeading(14)

    # Add column headers
    text.textLine('Report')
    text.textLine('--------------')
    
    # Convert data to text for report
    for index, row in data.iterrows():
        line = ', '.join([f'{col}: {row[col]}' for col in data.columns])
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()

    print(f"Report generated: {report_file}")

# Scheduler function
def scheduled_job():
    print("Fetching data and generating report...")
    try:
        data = fetch_data()
        generate_report(data)
    except Exception as e:
        print("Error generating report:", str(e))

# Schedule the job at a particular interval, e.g., every day at 9:00 AM
schedule.every().day.at("09:00").do(scheduled_job)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)  # Wait a minute before checking again