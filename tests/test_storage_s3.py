import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from fastapi_dbbackup.storage.s3 import S3Storage

@patch("boto3.client")
def test_s3_storage_initialization(mock_boto_client):
    storage = S3Storage(
        bucket="test-bucket",
        region="us-east-1",
        access_key="test-access",
        secret_key="test-secret",
        endpoint_url="https://test-endpoint.com",
        default_acl="public-read"
    )
    
    mock_boto_client.assert_called_once_with(
        "s3",
        region_name="us-east-1",
        aws_access_key_id="test-access",
        aws_secret_access_key="test-secret",
        endpoint_url="https://test-endpoint.com"
    )
    assert storage.bucket_name == "test-bucket"
    assert storage.default_acl == "public-read"

@patch("boto3.client")
def test_s3_storage_upload(mock_boto_client):
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3
    
    storage = S3Storage(
        bucket="test-bucket",
        default_acl="private"
    )
    
    local_path = Path("test_backup.sql")
    storage.upload(local_path)
    
    mock_s3.upload_file.assert_called_once_with(
        "test_backup.sql",
        "test-bucket",
        "test_backup.sql",
        ExtraArgs={"ACL": "private"}
    )

@patch("boto3.client")
def test_s3_storage_upload_with_prefix(mock_boto_client):
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3
    
    storage = S3Storage(
        bucket="test-bucket",
        prefix="dbback",
        default_acl="private"
    )
    
    local_path = Path("test_backup.sql")
    storage.upload(local_path)
    
    mock_s3.upload_file.assert_called_once_with(
        "test_backup.sql",
        "test-bucket",
        "dbback/test_backup.sql",
        ExtraArgs={"ACL": "private"}
    )

@patch("boto3.client")
def test_s3_storage_list_backups_relative(mock_boto_client):
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3
    
    # Mock paginator output
    mock_paginator = MagicMock()
    mock_s3.get_paginator.return_value = mock_paginator
    mock_paginator.paginate.return_value = [
        {"Contents": [{"Key": "dbback/backup1.sql"}, {"Key": "dbback/backup2.sql"}]}
    ]
    
    storage = S3Storage(bucket="test-bucket", prefix="dbback")
    backups = storage.list_backups()
    
    assert backups == ["backup1.sql", "backup2.sql"]

@patch("boto3.client")
def test_s3_storage_download_relative(mock_boto_client):
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3
    
    storage = S3Storage(bucket="test-bucket", prefix="dbback")
    
    local_path = Path("local.sql")
    storage.download("remote.sql", local_path)
    
    mock_s3.download_file.assert_called_once_with(
        "test-bucket",
        "dbback/remote.sql",
        str(local_path)
    )

@patch("boto3.client")
def test_s3_storage_upload_fileobj(mock_boto_client):
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3
    
    storage = S3Storage(bucket="test-bucket", prefix="dbback")
    
    import io
    fileobj = io.BytesIO(b"test data")
    storage.upload_fileobj(fileobj, "test.sql")
    
    mock_s3.upload_fileobj.assert_called_once_with(
        fileobj,
        "test-bucket",
        "dbback/test.sql",
        ExtraArgs={"ACL": "private"}
    )
