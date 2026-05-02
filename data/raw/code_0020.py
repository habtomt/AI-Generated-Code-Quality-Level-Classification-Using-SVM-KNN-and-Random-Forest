#!/usr/bin/env python3

from flask import Flask, request, jsonify
import subprocess
import os
import time
import threading
import queue
import shutil

app = Flask(__name__)

job_queue = queue.Queue()

STAGING_DIR = "./staging_env"
PROD_DIR = "./production_env"
REPO_DIR = "./repo"


def run_cmd(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def build_code():
    print("Building code...")
    result = run_cmd(["echo", "Building project..."])
    return result.returncode == 0


def run_tests():
    print("Running tests...")
    result = run_cmd(["python", "-m", "unittest", "discover"])
    return result.returncode == 0


def deploy(env):
    print(f"Deploying to {env}...")

    target = STAGING_DIR if env == "staging" else PROD_DIR

    if os.path.exists(target):
        shutil.rmtree(target)

    shutil.copytree(REPO_DIR, target)

    print(f"Deployment to {env} completed.")


def ci_pipeline(commit_id):
    print(f"CI started for commit {commit_id}")

    if not build_code():
        print("Build failed")
        return

    if not run_tests():
        print("Tests failed")
        return

    deploy("staging")

    print("CI pipeline successful")


def cd_pipeline():
    print("CD pipeline triggered")

    time.sleep(2)
    deploy("production")

    print("Production deployment complete")


def worker():
    while True:
        job = job_queue.get()
        if job["type"] == "ci":
            ci_pipeline(job["commit"])
        elif job["type"] == "cd":
            cd_pipeline()
        job_queue.task_done()


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    commit_id = data.get("commit", "unknown")

    job_queue.put({"type": "ci", "commit": commit_id})

    return jsonify({"status": "CI triggered"})


@app.route("/promote", methods=["POST"])
def promote():
    job_queue.put({"type": "cd"})
    return jsonify({"status": "CD triggered"})


def setup_envs():
    os.makedirs(REPO_DIR, exist_ok=True)

    with open(os.path.join(REPO_DIR, "app.py"), "w") as f:
        f.write("print('Hello CI/CD')")

    os.makedirs(STAGING_DIR, exist_ok=True)
    os.makedirs(PROD_DIR, exist_ok=True)


def main():
    setup_envs()

    t = threading.Thread(target=worker, daemon=True)
    t.start()

    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()