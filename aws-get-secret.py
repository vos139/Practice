import boto3
from botocore.exceptions import ClientError


def get_secret():

    secret = []
    secret_name = ["htz.devsecops.wiz.prod.client.id"]
    region_name = "us-east-1"

    # Create a Secrets Manager client
    boto3.setup_default_session(profile_name='hertz-dvps-core')
    # session = boto3.session.Session(profile_name='hertz-dvps-core')
    client = boto3.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    for i in secret_name:
	
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=i
            )
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e
    secret_value = get_secret_value_response['SecretString']
    secret = secret.append(secret_value)
    return(secret)

print(get_secret())
