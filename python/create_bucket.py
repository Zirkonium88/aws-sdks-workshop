# So importieren wir Pakete in Python
import boto3
from botocore.exceptions import ClientError
import logging

# Defintiion einer Funktion
def create_my_bucket(name: str, client):
    """Create a bucket.
    :param: name: str, the name of the bucket
    :param: client: obj, boto3 client object for s3
    returns: str, location URL of the bucket

    """
    logging.info("Creating bucket with name {}".format(name))
    try:
        # API call
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.create_bucket
        response = client.create_bucket(
            Bucket=name,
            CreateBucketConfiguration={
                'LocationConstraint': 'eu-central-1'
            },
        )
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
            logging.error("Error: BucketAlreadyExists")
    return response["Location"]

# Dient zur Steuerung des Programm von Außen
if __name__ == '__main__':
    # Bau des boto3 clients: Das ist die Pythonschnittstelle zu AWS
    s3_client = boto3.client("s3")

    # Schönes Logging; einfacher geht's mit print()
    # info, error, debug, exception sind vershciede Log Level
    logging.info("Starting bucket creation ...")

    # try ... except dient in PYthon dem Fehlerhandling
    try:
        create_my_bucket(
            client = s3_client,
            name='ipo8098jljl32j213bkj-my-bucket'
        )
    # ClientError ist auf AWS ausgerichtet, um Fehler der API zu handeln
    except ClientError as e:
        logging.error("Error: Bucket creation failed with {}".format(e))
        # Raise bricht das Programm ab, wenn ein ClientError auftritt
        raise
    logging.info("Finished bucket creation ...")
