import json
import boto3
from datetime import datetime, timezone

s3 = boto3.client('s3')
cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    try:
        # extract bucket and file name from S3 event trigger
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']

        # grab uploaded JSON file from S3
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        call_data = json.loads(response['Body'].read().decode('utf-8'))

        # call metrics
        active_calls = sum(1 for call in call_data if call['status'] == 'active')
        high_priority_calls = sum(1 for call in call_data if call['priority'] == 'high')
        short_calls = sum(1 for call in call_data if call['duration'] < 60)
        completed_calls = [call for call in call_data if call['status'] == 'completed']
        avg_wait_time = (
            sum(call.get('wait_time', 0) for call in completed_calls) / len(completed_calls)
            if completed_calls else 0
        )

        # send metrics to cloudwatch
        timestamp = datetime.now(timezone.utc)
        cloudwatch.put_metric_data(
            Namespace='callMetrics',
            MetricData=[
                {'MetricName': 'ActiveCalls', 'Value': active_calls, 'Unit': 'Count', 'Timestamp': timestamp},
                {'MetricName': 'HighPriorityCalls', 'Value': high_priority_calls, 'Unit': 'Count', 'Timestamp': timestamp},
                {'MetricName': 'ShortCalls', 'Value': short_calls, 'Unit': 'Count', 'Timestamp': timestamp},
                {'MetricName': 'AverageWaitTime', 'Value': avg_wait_time, 'Unit': 'Seconds', 'Timestamp': timestamp}
            ]
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Got it. Metrics processed and sent over to CloudWatch.')
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Oops. Looks like there was an Error processing file: {str(e)}")
        }
