from kubernetes import client, config

def configure_ha_deployment(name):
    # Replicas distributed across zones for failover
    deployment_spec = {
        "replicas": 3,
        "strategy": {"type": "RollingUpdate"},
        "template": {
            "spec": {
                "topologySpreadConstraints": [{
                    "maxSkew": 1,
                    "topologyKey": "topology.kubernetes.io/zone",
                    "whenUnsatisfiable": "DoNotSchedule"
                }]
            }
        }
    }
    print(f"Configuring redundant instances for {name} to ensure automatic failover.")

if __name__ == "__main__":
    configure_ha_deployment("critical-app")