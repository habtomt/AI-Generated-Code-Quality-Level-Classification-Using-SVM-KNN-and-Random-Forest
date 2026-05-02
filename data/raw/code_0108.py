import time
import threading
import schedule
from datetime import datetime
import requests
import os

# Mock social media tokens
TOKENS = {
    "facebook": os.getenv("FACEBOOK_TOKEN", "mock_facebook_token"),
    "twitter": os.getenv("TWITTER_TOKEN", "mock_twitter_token"),
}

# Job queue
post_queue = []


def mock_post_to_facebook(content):
    token = TOKENS["facebook"]
    payload = {"message": content, "access_token": token}
    return {"platform": "facebook", "status": "posted", "payload": payload}


def mock_post_to_twitter(content):
    token = TOKENS["twitter"]
    payload = {"text": content, "bearer": token}
    return {"platform": "twitter", "status": "posted", "payload": payload}


def enqueue_post(content, platform, post_time):
    post_queue.append({
        "content": content,
        "platform": platform,
        "post_time": post_time,
        "status": "scheduled"
    })


def process_queue():
    now = datetime.now()

    for job in post_queue:
        if job["status"] == "scheduled":
            run_time = datetime.strptime(job["post_time"], "%Y-%m-%d %H:%M:%S")

            if now >= run_time:
                content = job["content"]
                platform = job["platform"]

                if platform == "facebook":
                    result = mock_post_to_facebook(content)
                elif platform == "twitter":
                    result = mock_post_to_twitter(content)
                else:
                    result = {"status": "unknown platform"}

                job["status"] = "done"
                job["result"] = result

                print(f"[POSTED] {result}")


def scheduler_loop():
    schedule.every(5).seconds.do(process_queue)

    while True:
        schedule.run_pending()
        time.sleep(1)


def seed_jobs():
    now = datetime.now()

    enqueue_post(
        "Hello Facebook scheduled post!",
        "facebook",
        (now + timedelta(seconds=10)).strftime("%Y-%m-%d %H:%M:%S")
    )

    enqueue_post(
        "Hello Twitter scheduled post!",
        "twitter",
        (now + timedelta(seconds=15)).strftime("%Y-%m-%d %H:%M:%S")
    )


if __name__ == "__main__":
    from datetime import timedelta

    seed_jobs()

    print("Scheduler started...")
    thread = threading.Thread(target=scheduler_loop)
    thread.start()