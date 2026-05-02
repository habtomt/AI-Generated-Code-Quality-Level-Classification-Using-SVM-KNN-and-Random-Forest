import random
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# --- Mock Data Generator for Analytics ---
def generate_analytics_data():
    days = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7, 0, -1)]
    
    return {
        "platforms": ["Twitter", "Instagram", "LinkedIn"],
        "labels": days,
        "engagement": {
            "Twitter": [random.randint(100, 500) for _ in range(7)],
            "Instagram": [random.randint(300, 800) for _ in range(7)],
            "LinkedIn": [random.randint(50, 200) for _ in range(7)]
        },
        "follower_growth": {
            "Twitter": [5000 + (i * random.randint(10, 50)) for i in range(7)],
            "Instagram": [12000 + (i * random.randint(20, 100)) for i in range(7)],
            "LinkedIn": [2000 + (i * random.randint(5, 20)) for i in range(7)]
        },
        "top_posts": [
            {"platform": "Instagram", "content": "Product Launch Video", "reach": "25.4k", "engagement": "8.2%"},
            {"platform": "Twitter", "content": "Thread on Python Tips", "reach": "12.1k", "engagement": "5.4%"},
            {"platform": "LinkedIn", "content": "Company Culture Update", "reach": "5.8k", "engagement": "12.1%"}
        ]
    }

# --- Dashboard HTML Template (using Chart.js for visualizations) ---
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Social Analytics Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: auto; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
        .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .full-width { grid-column: span 2; }
        h2 { color: #333; margin-top: 0; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { text-align: left; padding: 12px; border-bottom: 1px solid #eee; }
        th { background: #fafafa; color: #666; }
        .metric-badge { padding: 4px 8px; border-radius: 4px; font-size: 0.85em; font-weight: bold; background: #e3f2fd; color: #1976d2; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Social Media Analytics Dashboard</h1>
        
        <div class="grid">
            <div class="card">
                <h2>Engagement Trends</h2>
                <canvas id="engagementChart"></canvas>
            </div>
            <div class="card">
                <h2>Follower Growth</h2>
                <canvas id="growthChart"></canvas>
            </div>
            <div class="card full-width">
                <h2>Top Performing Posts</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Platform</th>
                            <th>Content Snippet</th>
                            <th>Reach</th>
                            <th>Engagement Rate</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for post in data.top_posts %}
                        <tr>
                            <td><strong>{{ post.platform }}</strong></td>
                            <td>{{ post.content }}</td>
                            <td>{{ post.reach }}</td>
                            <td><span class="metric-badge">{{ post.engagement }}</span></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        const data = {{ data | tojson }};

        // Engagement Chart
        new Chart(document.getElementById('engagementChart'), {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [
                    { label: 'Twitter', data: data.engagement.Twitter, borderColor: '#1DA1F2', tension: 0.3 },
                    { label: 'Instagram', data: data.engagement.Instagram, borderColor: '#E1306C', tension: 0.3 },
                    { label: 'LinkedIn', data: data.engagement.LinkedIn, borderColor: '#0077B5', tension: 0.3 }
                ]
            }
        });

        // Follower Growth Chart
        new Chart(document.getElementById('growthChart'), {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [
                    { label: 'Twitter', data: data.follower_growth.Twitter, backgroundColor: 'rgba(29, 161, 242, 0.6)' },
                    { label: 'Instagram', data: data.follower_growth.Instagram, backgroundColor: 'rgba(225, 48, 108, 0.6)' },
                    { label: 'LinkedIn', data: data.follower_growth.LinkedIn, backgroundColor: 'rgba(0, 119, 181, 0.6)' }
                ]
            },
            options: { scales: { y: { beginAtZero: false } } }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    analytics_data = generate_analytics_data()
    return render_template_string(DASHBOARD_TEMPLATE, data=analytics_data)

@app.route('/api/metrics')
def get_metrics():
    return jsonify(generate_analytics_data())

if __name__ == '__main__':
    # Required: pip install Flask
    app.run(debug=True, port=5000)