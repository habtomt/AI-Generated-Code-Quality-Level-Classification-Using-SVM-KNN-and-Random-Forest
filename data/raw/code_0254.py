import time
import schedule
import threading
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- In-Memory Job Queue ---
# In production, use Redis and Celery/RQ for persistence
post_queue = []

# --- Mock Social Media API ---
class SocialMediaAPI:
    @staticmethod
    def post_content(platform, content):
        """
        Simulates an API call to a social media platform.
        """
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        print(f"EXECUTING POST TO: {platform}")
        print(f"CONTENT: {content}")
        print("-" * 30)
        return True

# --- Scheduler Logic ---
def execute_scheduled_post(post_id):
    global post_queue
    # Find the post in the queue
    post = next((p for p in post_queue if p['id'] == post_id), None)
    
    if post and not post['posted']:
        success = SocialMediaAPI.post_content(post['platform'], post['content'])
        if success:
            post['posted'] = True

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# --- API Endpoints ---
@app.route('/schedule-post', methods=['POST'])
def add_to_queue():
    data = request.json
    
    # Required data: content, platform, time (format "HH:MM")
    new_post = {
        "id": len(post_queue) + 1,
        "content": data.get('content'),
        "platform": data.get('platform'),
        "scheduled_time": data.get('time'),
        "posted": False
    }
    
    post_queue.append(new_post)
    
    # Add job to the scheduler
    schedule.every().day.at(new_post['scheduled_time']).do(
        execute_scheduled_post, 
        post_id=new_post['id']
    ).tag(f"post-{new_post['id']}")
    
    return jsonify({
        "status": "success", 
        "message": f"Post scheduled for {new_post['scheduled_time']}"
    }), 201

@app.route('/queue', methods=['GET'])
def get_queue():
    return jsonify(post_queue)

if __name__ == '__main__':
    # Start the scheduler in a background thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Example usage instructions:
    # POST to /schedule-post with JSON:
    # {
    #   "content": "Automated post from Python!",
    #   "platform": "LinkedIn",
    #   "time": "14:30"
    # }
    
    # Required: pip install Flask schedule
    app.run(debug=False, port=5000)