import boto3

# Set up your AWS credentials
aws_access_key_id = 'ASIAT3EXCLIVAJUNSV6E'
aws_secret_access_key = 'iVIjZPp0fSf6G+d+0UMejvD3tf/J6M6TxxcQUCnN'
region_name = 'us-east-1'
session_token = 'FwoGZXIvYXdzEKH//////////wEaDALCJaxu6Bn89G7DSSLCAYQ88kkweCGzyTAupY0SutllnEKmKxG622HFCr4ecpA57e03nFbGhrWHFBN4qOlNn4c3Cey3qP5F6lIps/FLGRRZqlCY7J2MvjaP1zSytDLlGh+xQj1K0TWfsW82qoSYIlRVRzNLzzXBfxz34juSUnJH2pzLXwHfQU98PYsmA1RizlgRNWyzrpq1qSdprmGCjINnYpUVEzF+taFG9ktAr79IVHqw6D8daHbL5E2/5g5UrPi2QlJwCX1R8gPSnhzfqAKOKOWBmZ0GMi0Sc+9er3M3vd9gLb3DdayHsWp1uFH6RjV/oVsAq88EcN3vZonG4H43WWN57QU='

# Create an EC2 client
ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key, region_name=region_name, aws_session_token=session_token)

# Create an EC2 resource
ec2_resource = boto3.resource('ec2', aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key, region_name=region_name, aws_session_token=session_token)

# Set the AMI and instance type for the instances
ami_id = 'ami-0149b2da6ceec4bb0'  # Ubuntu 18.04 LTS
instance_type = 't2.micro'

# Read in the user data files
with open('standalone_userdata.txt', 'r') as f:
    standalone_user_data = f.read()

# Define the security group's parameters
security_group_name = 'MySecurityGroup'
description = 'Security group for my EC2 instance'

# Create a new security group
security_group = ec2_client.create_security_group(
    GroupName=security_group_name,
    Description=description
)

# Get the security group's ID
security_group_id = security_group['GroupId']

# Allow all traffic for the security group
ec2_client.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpPermissions=[{
        'IpProtocol': '-1',
        'FromPort': -1,
        'ToPort': -1,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    }]
)

# create a file to store the key locally
outfile = open('myEc2-keypair.pem', 'w')
# call the boto ec2 function to create a key pair
key_pair = ec2_resource.create_key_pair(KeyName='myEc2-ec2-keypair')
# capture the key and store it in a file
KeyPairOut = str(key_pair.key_material)
print(KeyPairOut)
outfile.write(KeyPairOut)

# Create the standalone MySQL instance
standalone_instance = ec2_resource.create_instances(
    ImageId=ami_id,
    InstanceType=instance_type,
    MinCount=1,
    MaxCount=1,
    UserData=standalone_user_data,
)[0]

print(f'Created standalone MySQL instance: {standalone_instance.id}')

# Create the data node instances
data_node_instances = ec2_resource.create_instances(
    ImageId=ami_id,
    InstanceType=instance_type,
    MinCount=3,
    MaxCount=3,
    KeyName ='myEc2-ec2-keypair',
    SecurityGroupIds=[security_group_id],
)

print('Created data node instances:')
for instance in data_node_instances:
    print(instance.id)

# Create the master node instance
master_node_instance = ec2_resource.create_instances(
    ImageId=ami_id,
    InstanceType=instance_type,
    MinCount=1,
    MaxCount=1,
    KeyName ='myEc2-ec2-keypair',
    SecurityGroupIds=[security_group_id],
)[0]

print(f'Created master node instance: {master_node_instance.id}')

# Create the proxy instance
proxy_instance = ec2_resource.create_instances(
    ImageId=ami_id,
    InstanceType=instance_type,
    MinCount=1,
    MaxCount=1,
    UserData=standalone_user_data,
    KeyName ='myEc2-ec2-keypair',
    SecurityGroupIds=[security_group_id],
)
