import json
import boto3

# init s3 client
s3 = boto3.client('s3')


def get_call_data(bucket_name, file_name):
    # retrieve call data file from s3
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        content = response['Body'].read().decode('utf-8')
        return json.loads(content)
    except Exception as e:
        print(f"❌ Error retrieving file from S3: {e}")
        return []


def analyze_call_data(call_data):
    # analyze call durations and wait times
    if not call_data:
        print("Uh...there's no data to analyze.")
        return {}

    total_calls = len(call_data)
    avg_duration = sum(call["duration"] for call in call_data) / total_calls
    avg_wait = sum(call["wait_time"] for call in call_data) / total_calls
    high_priority = sum(1 for call in call_data if call["priority"] == "high")

    return {
        "total_calls": total_calls,
        "avg_duration_sec": round(avg_duration, 2),
        "avg_wait_time_sec": round(avg_wait, 2),
        "high_priority_calls": high_priority
    }


if __name__ == "__main__":
    # fetch and analyze call data from S3
    bucket_name = "call-volume-data"
    file_name = "simulated_calls.json"

    call_data = get_call_data(bucket_name, file_name)
    results = analyze_call_data(call_data)

    print(json.dumps(results, indent=4))
