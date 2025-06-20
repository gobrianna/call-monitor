# formats simulated data for AWS S3 storage
import json
# generates random values for realistic call volumes
import random
# AWS SDK for Python
import boto3


# init s3 client
s3 = boto3.client('s3')


def generate_call_data(num_calls=100):
    # generates call data using list comprehension
    return [
        {
            "id": i + 1,
            "duration": random.randint(1, 600),
            "status": random.choice(["active", "waiting", "completed"]),
            "priority": random.choice(["low", "medium", "high"]),
            "wait_time": random.randint(10, 300)
        }
        for i in range(num_calls)
    ]


def s3_data_upload(data, bucket_name, file_name):
    # upload call data to s3 bucket
    try:
        # convert to json
        json_data = json.dumps(data, indent=4)
        # upload json to s3 bucket
        s3.put_object(
            Bucket=bucket_name, 
            Key=file_name, 
            Body=json_data,
            ContentType="application/json"
            )
        print(f"Uploaded '{file_name}' to S3 bucket '{bucket_name}' successfully! Yay!")
    except Exception as e:
        print(f"Yikes! There was an error uploading the file to S3: {e}")


if __name__ == "__main__":
    # upload data to s3
    bucket_name = "call-volume-data"
    file_name = "simulated_calls.json"

    # generate call data
    data = generate_call_data()
    # print data for verification
    print(json.dumps(data, indent=4))
    # upload to s3
    s3_data_upload(data, bucket_name, file_name)
