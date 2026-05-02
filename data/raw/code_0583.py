"""
Auto-generated Python code
Scenario : Serverless Deployment
Prompt   : response_002.txt
Run      : 3
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import RGBColor

# Sample database connection (replace with your actual database connection)
import sqlite3
cnx = sqlite3.connect('your_database.db')

# Define the function to generate the report
def generate_report():
    try:
        # Query the database to retrieve data
        query = "SELECT * FROM your_table"
        df = pd.read_sql_query(query, cnx)

        # Create a new document
        document = Document()

        # Add a title to the document
        title = document.add_paragraph()
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title.add_run('Your Report Title').font.bold = True
        title.add_run(' ').font.size = Pt(24)

        # Add a section to the document
        section = document.add_section()
        section.alignment = WD_ALIGN_PARAGRAPH.LEFT

        # Add a table to the section
        table = section.add_table(rows=len(df) + 1, cols=len(df.columns), style='Table Grid')
        for j in range(len(df.columns)):
            table.cell(0, j).text = df.columns[j]

        # Fill the table with data
        for i in range(len(df)):
            for j in range(len(df.columns)):
                table.cell(i + 1, j).text = str(df.iloc[i, j])

        # Save the document to a file
        document.save('report.docx')
        print('Report generated successfully.')

    except Exception as e:
        print(f'Error generating report: {str(e)}')

# Define the scheduler
scheduler = BlockingScheduler()

# Schedule the function to run every day at 8am
scheduler.add_job(generate_report, 'cron', day='*', hour='8', minute='0', timezone='US/Eastern')

# Start the scheduler
scheduler.start()