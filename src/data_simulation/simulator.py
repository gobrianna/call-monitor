# Formats simulated data for AWS S3 storage
import json
# Generates random values for realistic call volumes
import random
# AWS SDK for Python
import boto3


# Initialize S3 client
s3 = boto3.client('s3')


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


def s3_data_upload(data, bucket_name, file_name):
    """
    Uploads simulated call volume data to an s3 bucket.
    """
    try:
        # Convert to JSON
        json_data = json.dumps(data, indent=4)

        # Uploads JSON data to S3
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=json_data)
        print(
            f"File '{file_name}' uploaded successfully to bucket '{bucket_name}'.")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")


if __name__ == "__main__":
    # Generate call data
    data = generate_call_data()

    # Print data for verification
    print(json.dumps(data, indent=4))

    # Upload data to S3
    bucket_name = "call-volume-data"
    file_name = "simulated_calls.json"
    s3_data_upload(data, bucket_name, file_name)
