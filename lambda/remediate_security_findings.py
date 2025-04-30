import boto3
import json

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    sns = boto3.client('sns')
    
    print("Event received:", json.dumps(event))

    # Extract instance ID from Security Hub finding (if present)
    try:
        finding = event['detail']['findings'][0]
        for resource in finding['Resources']:
            if resource['Type'] == 'AwsEc2Instance':
                instance_id = resource['Id'].split("/")[-1]

                # Notify via SNS
                sns.publish(
                    TopicArn='arn:aws:sns:eu-north-1:<id>:<topic>',
                    Subject='[Approval Needed] High Severity Security Finding',
                    Message=f'    Instance ID: {Instance ID} Action: This instance will be automatically stopped in 2 minutes unless action is taken.'
                )

                # Stop EC2 instance
                ec2.stop_instances(InstanceIds=[instance_id])
                return {'status': 'stopped', 'instance': instance_id}
    except Exception as e:
        print("Error:", str(e))
        return {'error': str(e)}
