import sqlite3
import schedule
import time
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# --- Database Setup (Mocking data for the example) ---
def setup_database():
    conn = sqlite3.connect('analytics.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                        id INTEGER PRIMARY KEY, 
                        item TEXT, 
                        amount REAL, 
                        date TEXT)''')
    
    # Insert sample data if empty
    cursor.execute("SELECT COUNT(*) FROM sales")
    if cursor.fetchone()[0] == 0:
        data = [
            ('Widget A', 150.00, '2026-04-20'),
            ('Widget B', 200.50, '2026-04-21'),
            ('Service X', 500.00, '2026-04-22')
        ]
        cursor.executemany("INSERT INTO sales (item, amount, date) VALUES (?, ?, ?)", data)
        conn.commit()
    conn.close()

# --- Report Generation Logic ---
def generate_pdf_report():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Report_{timestamp}.pdf"
    
    # 1. Fetch Data
    conn = sqlite3.connect('analytics.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales")
    rows = cursor.fetchall()
    conn.close()

    # 2. Document Setup
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # 3. Add Header
    elements.append(Paragraph(f"Scheduled Sales Report - {timestamp}", styles['Title']))
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    # 4. Create Table
    table_data = [['ID', 'Item Description', 'Amount ($)', 'Date']]
    total_sum = 0
    for row in rows:
        table_data.append(list(row))
        total_sum += row[2]
    
    table_data.append(['', 'TOTAL', f"{total_sum:.2f}", ''])

    t = Table(table_data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
    ]))
    
    elements.append(t)

    # 5. Build PDF
    doc.build(elements)
    print(f"Report generated successfully: {filename}")

# --- Scheduler ---
def run_scheduler():
    setup_database()
    
    # Schedule the task every minute for demonstration (can be .day.at("00:00"))
    schedule.every(1).minutes.do(generate_pdf_report)

    print("Report scheduler started. Press Ctrl+C to stop.")
    
    # Run the task immediately once
    generate_pdf_report()

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()