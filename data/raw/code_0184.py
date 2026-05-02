import shutil
import os

class RedundantFileSystem:
    def __init__(self, primary_node, replica_nodes):
        self.primary = primary_node
        self.replicas = replica_nodes
        for path in [self.primary] + self.replicas:
            os.makedirs(path, exist_ok=True)

    def store_file(self, filename, content):
        primary_path = os.path.join(self.primary, filename)
        with open(primary_path, 'w') as f:
            f.write(content)
        
        for node in self.replicas:
            replica_path = os.path.join(node, filename)
            shutil.copy2(primary_path, replica_path)

    def access_file(self, filename):
        nodes = [self.primary] + self.replicas
        for node in nodes:
            target = os.path.join(node, filename)
            if os.path.exists(target):
                with open(target, 'r') as f:
                    return f.read()
        raise FileNotFoundError("File lost across all nodes")

if __name__ == "__main__":
    rfs = RedundantFileSystem("./node1", ["./node2", "./node3"])
    rfs.store_file("config.txt", "redundant_data_v1")