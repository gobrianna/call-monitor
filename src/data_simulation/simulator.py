# Format of simulated data for AWS S3 storage
import json
# Generation of random values for realistic call volumes
import random


def generate_call_data(num_calls=100):
    calls = []
    for i in range(num_calls):
        call = {
            "id": i + 1,
            "duration": random.randint(1, 600),
            "status": random.choice(["active", "waiting", "completed"])
        }
        calls.append(call)
    return calls


if __name__ == "__main__":
    data = generate_call_data()
    print(json.dumps(data, indent=4))
