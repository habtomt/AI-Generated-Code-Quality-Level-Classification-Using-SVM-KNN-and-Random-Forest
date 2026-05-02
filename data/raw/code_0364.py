"""
Auto-generated Python code
Scenario : Container Orchestration
Prompt   : response_002.txt
Run      : 3
"""

# Import required libraries
import docker
import psutil
import time

# Create a Docker client
client = docker.from_env()

# Function to get the current system resources
def get_system_resources():
    try:
        # Get the current system CPU and memory usage
        cpu_usage = psutil.cpu_percent()
        mem_usage = psutil.virtual_memory().percent
        return cpu_usage, mem_usage
    except Exception as e:
        print(f"Error: {e}")

# Function to allocate container resources based on real-time application demand
def allocate_container_resources():
    try:
        # Get the current system resources
        cpu_usage, mem_usage = get_system_resources()
        
        # Check if the CPU usage is higher than 80%
        if cpu_usage > 80:
            # Create a new container with increased CPU resources
            container = client.containers.run(
                'python:3.9-slim',
                detach=True,
                cpu_shares=1024,
                mem_limit='512m',
                name='resource-intensive-container'
            )
            print(f"Container created with increased CPU resources: {container.short_id}")
        
        # Check if the memory usage is higher than 80%
        elif mem_usage > 80:
            # Create a new container with increased memory resources
            container = client.containers.run(
                'python:3.9-slim',
                detach=True,
                cpu_shares=512,
                mem_limit='1024m',
                name='memory-intensive-container'
            )
            print(f"Container created with increased memory resources: {container.short_id}")
        
        # If neither condition is met, check if there are any idle containers
        else:
            # Get a list of all containers
            containers = client.containers.list()
            
            # Iterate over the containers
            for container in containers:
                # Check if the container is idle (i.e., not running any processes)
                if container.status != 'running':
                    # Remove the idle container
                    client.containers.remove(container.id)
                    print(f"Idle container removed: {container.short_id}")
    except Exception as e:
        print(f"Error: {e}")

# Function to manage container resources based on real-time application demand
def manage_container_resources():
    try:
        # Allocate container resources based on real-time application demand
        allocate_container_resources()
        
        # Continuously monitor the system resources and allocate container resources as needed
        while True:
            time.sleep(30)  # Wait 30 seconds before checking again
            allocate_container_resources()
    except KeyboardInterrupt:
        print("\nStopping the container resource management process...")
    except Exception as e:
        print(f"Error: {e}")

# Start the container resource management process
if __name__ == "__main__":
    manage_container_resources()