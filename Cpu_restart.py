#!/usr/bin/env python3

import psutil
import time
import subprocess

# Threshold for CPU usage percentage
CPU_USAGE_THRESHOLD = 80
# Interval in seconds to check CPU usage
CHECK_INTERVAL = 10
# Command to restart Laravel service
LARAVEL_SERVICE_RESTART_CMD = ["systemctl", "restart", "laravel-backend"]

def get_cpu_usage():
    """Returns the current CPU usage as a percentage."""
    return psutil.cpu_percent(interval=1)

def restart_service():
    """Restarts the Laravel backend service."""
    try:
        print("Restarting Laravel backend service...")
        subprocess.run(LARAVEL_SERVICE_RESTART_CMD, check=True)
        print("Laravel backend service restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart Laravel service: {e}")

def monitor_cpu_and_restart():
    """Monitors CPU usage and restarts Laravel service if threshold is exceeded."""
    while True:
        cpu_usage = get_cpu_usage()
        print(f"Current CPU usage: {cpu_usage}%")

        if cpu_usage > CPU_USAGE_THRESHOLD:
            print(f"CPU usage {cpu_usage}% exceeds threshold {CPU_USAGE_THRESHOLD}%. Restarting service.")
            restart_service()
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    print("Starting CPU usage monitoring...")
    monitor_cpu_and_restart()
