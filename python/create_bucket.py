# So importieren wir Pakete in Python
import boto3
from botocore.exceptions import ClientError

# Erstellung einer Funktion in Python
def create_my_bucket(name: str, client):
    """Create a bucket.
    :param: name: str, the name of the bucket
    :param: client: obj, boto3 client object for s3
    returns: str, location URL of the bucket or none

    """
    print("Creating bucket with name {}".format(name))
    try:
        # API call
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.create_bucket
        response = client.create_bucket(
            Bucket=name,
            CreateBucketConfiguration={
                'LocationConstraint': 'eu-central-1'
            },
        )    
        return response["Location"]
    except ClientError as e:
        # So parst man die JSON-Ausgabe der AWS API
        # {
        #    "Error": {
        #        "Code": "BucketAlreadyExists"
        #    }    
        # }
        # if-Bedingung in Python enden mit einem Doppelpunkt
        # if foo:
        #     print(foo)
        # else:
        #     print(bar)
        if e.response['Error']['Code'] == "BucketAlreadyExists":
            print("Error: BucketAlreadyExists")
            raise
        if e.response['Error']['Code'] == "BucketAlreadyOwnedByYou":
            print("Error: BucketAlreadyOwnedByYou")
            raise
        return None


# Dient zur Steuerung des Programm von Außen
if __name__ == '__main__':

    # Bau des boto3 s3 clients: Das ist die Pythonschnittstelle zu AWS
    # Es gibt auch boto3 resource Objekte
    session = boto3.Session(profile_name="myaws")
    s3_client = session.client("s3")

    # Schönes Logging; einfacher geht's mit print()
    # info, error, debug, exception sind verschiedene Log Level
    print("Starting bucket creation ...")
    # try ... except dient in Python dem Fehlerhandling
    response = create_my_bucket(
        client = s3_client,
        name='ipo8098jljl32j213bkj-my-bucket'
    )
    if response is not None:
        print("Finished bucket creation {}".format(response))
    else:
        print("Failed bucket creation ...")
