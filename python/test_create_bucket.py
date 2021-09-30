from botocore.exceptions import ClientError
from unittest.mock import MagicMock
from botocore.stub import Stubber
import botocore.session
import pytest
import os

# Ein Pytest fixture steht überall zur Zeit des Testausführung zur Verfügung
# Bau von Fake Credentials
@pytest.fixture(scope="function")
def aws_credentials():
    """Mock AWS Credentials for boto3 client creation."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


# Bau eines S3 client mit fake credentials
@pytest.fixture(scope="function")
def s3(aws_credentials):
    """Mock s3 boto3 client.

    Params:
        aws_credentials: mocked aws credentials
    """
    yield botocore.session.get_session().create_client("s3")

class TestCreateBucket():
    """Testklassen, machen manches einfacher und anderes schwieriger."""
    def test_s3_create_bucket(self, s3):
        """Test boto3 API call create_bucket.
        :param scope
        :param s3: obj, mocked boto3 client
        :return: no returns
        """
        # Baue von Unittests in der Give-When-Then Strategie
        # Give
        stubber = Stubber(s3)
        bucket_name = "examplebucket"
        response = {
            'Location': 'http://{}.s3.amazonaws.com/'.format(bucket_name),
            'ResponseMetadata': {
                '...': '...',
            },
        }

        expected_params = {
            "Bucket": bucket_name,
            "CreateBucketConfiguration": {
                'LocationConstraint': 'eu-central-1'
            },
        }

        # When
        stubber.add_response("create_bucket", response, expected_params)
        # with baut besonder Kontexte in Funktionen auf
        # Zum Beispiel hier die Stubbererstellung, oder auch für das Einlesen von Dateien in Python
        with stubber:
            service_response = s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': 'eu-central-1'
                },
            )

        # Then
        # Mit assert Vergelichen wie die Inhalten von service_response und response
        # Wenn True, dann ist der Assert ohne Fehler
        # Wenn False, kommt ein AssertionError
        assert service_response == response

    def test_create_my_bucket_success(self):
        """Test der Hauptfunktion mit Erfolg.
        :param scope
        :return: no returns
        """
        # Give
        from create_bucket import create_my_bucket as uat
        bucket_name = "examplebucket"

        # Mit MagicMock, kann man das Verhalten von oÓbjekte in Python nachstellen
        # Hier soll s3 gemockt werden
        s3 = MagicMock()

        # Wenn der API call create_bucket kommt, soll der MagicMock Folgendes zurückwerfen
        s3.create_bucket.return_value = {
            'Location': 'http://{}.s3.amazonaws.com/'.format(bucket_name),
            'ResponseMetadata': {
                '...': '...',
            },
        }

        # When
        # Ausführen des user acceptance test
        response = uat(
            name=bucket_name,
            client=s3,
        )

        # Then
        # Prüfe ob create_bucket mit den folgende Argumenten udn Paremtern ausgeführt wurde
        s3.create_bucket.assert_called_with(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'eu-central-1'
            },
        )

        # Wir wollen den in Zeile 87 ff definierten Rückgabewert gegen den eigentlichen prüfen
        assert response == 'http://{}.s3.amazonaws.com/'.format(bucket_name)

    def test_create_my_bucket_error(self):
        """Test der Hauptfunktion ohne Erfolg (gewollt).
        :param scope
        :return: no returns
        """
        # Give
        from create_bucket import create_my_bucket as uat

        # Wieder die Erstellung des MagicMocks für den s3 client
        s3 = MagicMock()

        # Bauen eines Fehlers
        model = botocore.session.get_session().get_service_model("s3")
        factory = botocore.errorfactory.ClientExceptionsFactory()
        exceptions = factory.create_client_exceptions(model)

        # Dies Mal soll ein Fehler geworfen werden, wenn create_bucketaufgerufen wird: BucketAlreadyExists
        s3.create_bucket.side_effect = exceptions.BucketAlreadyExists(
            error_response={
                "Error": {
                    "Code": "BucketAlreadyExists",
                    "Message": "BucketAlreadyExists",
                }
            },
            operation_name="CreateBucket",
        )

        bucket_name = "examplebucket"

        # When
        # Wir wollen die Fehlemeldung auffangen und prüfen
        try:
            uat(
                name=bucket_name,
                client=s3,
            )
            # Wenn kein Fehler geworfen wird (gegen unseren Willen), soll des Test fehlschlagen.
            assert False
        except ClientError as e:
            # Wenn der Fehler BucketAlreadyExists geworfen wird (in unserem Sinn), soll des Test erfolgreich verlaufen.
            if e.response['Error']['Code'] == "BucketAlreadyExists":
                assert True
        # Then
        # Wir prüfen aber auch ob create_bucket ausgeüfhrt wurde
        s3.create_bucket.assert_called_with(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'eu-central-1'
            },
        )
