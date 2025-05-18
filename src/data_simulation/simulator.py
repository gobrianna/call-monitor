# Formats simulated data for AWS S3 storage
import json
# Generates random values for realistic call volumes
import random


def generate_call_data(num_calls=100):
    """
    Simulates call volume data as a list of directories.
    Each directory represents a call with various attributes.
    """
    calls = []  # Initialzes empty list to store simulated calls
    for i in range(num_calls):
        call = {
            "id": i + 1,
            "caller_name": f"Caller_{i+1}",
            "duration": random.randint(1, 600),
            "status": random.choice(["active", "waiting", "completed"]),
            "priority": random.choice(["low", "medium", "high"])
        }
        calls.append(call)
    return calls


if __name__ == "__main__":
    data = generate_call_data()
    print(json.dumps(data, indent=4))
