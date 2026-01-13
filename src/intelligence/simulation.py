SIMULATION_MODE = False

SIMULATED_INSTANCES = {
    "i-simulated-idle": {
        "state": "running",
        "avg_cpu_7d": 0.2,
        "network_mb_7d": 1.0,
        "tags": {
            "Name": "simulated-idle-dev",
            "Environment": "dev",
            "AutoOptimize": "true"
        }
    }
}
