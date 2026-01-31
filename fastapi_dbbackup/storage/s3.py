import boto3
from pathlib import Path
from typing import List, Optional
from fastapi_dbbackup.storage.base import StorageBackend

class S3Storage(StorageBackend):
    def __init__(self, bucket: str, region: Optional[str] = None, prefix: str = ""):
        self.bucket_name = bucket
        self.prefix = prefix.strip("/")
        self.s3 = boto3.client("s3", region_name=region)

    def _get_key(self, name: str) -> str:
        if self.prefix:
            return f"{self.prefix}/{name}"
        return name

    def upload(self, local_path: Path) -> str:
        key = self._get_key(local_path.name)
        self.s3.upload_file(str(local_path), self.bucket_name, key)
        return key

    def download(self, remote_path: str, local_path: Path):
        self.s3.download_file(self.bucket_name, remote_path, str(local_path))

    def list_backups(self) -> List[str]:
        paginator = self.s3.get_paginator("list_objects_v2")
        backups = []
        for page in paginator.paginate(Bucket=self.bucket_name, Prefix=self.prefix):
            for obj in page.get("Contents", []):
                backups.append(obj["Key"])
        return backups

    def delete(self, remote_path: str):
        self.s3.delete_object(Bucket=self.bucket_name, Key=remote_path)
