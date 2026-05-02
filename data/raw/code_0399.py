"""
Auto-generated Python code
Scenario : Data Storage
Prompt   : response_002.txt
Run      : 1
"""

import os
import shutil
import random

# Simulated storage nodes as directories
STORAGE_NODES = ['node1', 'node2', 'node3']
REPLICATION_FACTOR = 2

# Setup storage nodes as directories
for node in STORAGE_NODES:
    os.makedirs(node, exist_ok=True)

# Metadata Service: Keep track of where files are stored
metadata = {}

def store_file(filename, data):
    # Pick random nodes based on the replication factor
    chosen_nodes = random.sample(STORAGE_NODES, REPLICATION_FACTOR)
    metadata[filename] = chosen_nodes

    # Store the file in the chosen nodes
    for node in chosen_nodes:
        with open(os.path.join(node, filename), 'w') as f:
            f.write(data)

def read_file(filename):
    # Retrieve the nodes where the file is stored
    if filename in metadata:
        for node in metadata[filename]:
            filepath = os.path.join(node, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return f.read()
    print("File not found or corrupt!")
    return None

def simulate_node_failure(node):
    print(f"Simulating failure of node {node}")
    if node in STORAGE_NODES:
        shutil.rmtree(node)
        STORAGE_NODES.remove(node)
        for file, nodes in metadata.items():
            if node in nodes:
                nodes.remove(node)

def main():
    try:
        store_file('example.txt', 'This is some important data.')
        print("Reading file:", read_file('example.txt'))
        simulate_node_failure('node2')
        print("Reading file after node failure:", read_file('example.txt'))
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()