import boto3
import requests

session = boto3.Session(profile_name='yourprofile')

# hosted zone and record info
hosted_zone_id = 'yourhostedzone'
record_name = 'yourdnsrecordname'
new_ip = '192.0.2.1'

# get the public ip
def get_public_ip():
    response = requests.get('https://ipinfo.io/json')
    data = response.json()
    return data['ip']


# get the a record
def get_a_record_ipaddr(hosted_zone_id, record_name):
    client = session.client('route53')

    # List the resource record sets for the hosted zone
    response = client.list_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        StartRecordName=record_name,
        StartRecordType='A',
        MaxItems='1'
    )

    for record_set in response['ResourceRecordSets']:
        for records in record_set['ResourceRecords']:
            return records['Value']


# update the a record
def update_a_record(hosted_zone_id, record_name, new_ip):
    client = session.client('route53')

    # Define the change batch for updating the A record
    change_batch = {
        'Comment': 'Update A record',
        'Changes': [
            {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': record_name,
                    'Type': 'A',
                    'TTL': 300,
                    'ResourceRecords': [{'Value': new_ip}]
                }
            }
        ]
    }

    # Submit the change batch to Route 53
    response = client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch=change_batch
    )

    return response

public_ip = get_public_ip()
print("Rasberry PI IP address:", public_ip)

awsipaddr = get_a_record_ipaddr(hosted_zone_id, record_name)
print("AWS IP address:", awsipaddr)

if public_ip != awsipaddr:
    print("AWS and Public IP are different. Updating AWS IP.....")
    awsresponse = update_a_record(hosted_zone_id,record_name, public_ip)
    print(awsresponse)
    print("Done")
else:
    print("No change")
