import boto3
from pathlib import Path
from typing import List, Optional
from fastapi_dbbackup.storage.base import StorageBackend

class S3Storage(StorageBackend):
    def __init__(
        self, 
        bucket: str, 
        region: Optional[str] = None, 
        prefix: str = "",
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        default_acl: str = "private"
    ):
        self.bucket_name = bucket
        self.prefix = prefix.strip("/")
        self.default_acl = default_acl
        
        client_kwargs = {"region_name": region}
        if access_key and secret_key:
            client_kwargs["aws_access_key_id"] = access_key
            client_kwargs["aws_secret_access_key"] = secret_key
        if endpoint_url:
            client_kwargs["endpoint_url"] = endpoint_url
            
        self.s3 = boto3.client("s3", **client_kwargs)

    def _get_key(self, name: str) -> str:
        if self.prefix:
            return f"{self.prefix}/{name}"
        return name

    def upload(self, local_path: Path) -> str:
        key = self._get_key(local_path.name)
        extra_args = {}
        if self.default_acl:
            extra_args["ACL"] = self.default_acl
            
        self.s3.upload_file(
            str(local_path), 
            self.bucket_name, 
            key,
            ExtraArgs=extra_args
        )
        return key

    def upload_fileobj(self, fileobj: BinaryIO, remote_path: str) -> str:
        key = self._get_key(remote_path)
        extra_args = {}
        if self.default_acl:
            extra_args["ACL"] = self.default_acl
            
        self.s3.upload_fileobj(
            fileobj,
            self.bucket_name,
            key,
            ExtraArgs=extra_args
        )
        return key

    def download(self, remote_path: str, local_path: Path):
        key = self._get_key(remote_path)
        self.s3.download_file(self.bucket_name, key, str(local_path))

    def list_backups(self) -> List[str]:
        paginator = self.s3.get_paginator("list_objects_v2")
        backups = []
        for page in paginator.paginate(Bucket=self.bucket_name, Prefix=self.prefix):
            for obj in page.get("Contents", []):
                key = obj["Key"]
                # Return only the filename part if it's within the prefix
                if self.prefix and key.startswith(f"{self.prefix}/"):
                    backups.append(key[len(self.prefix)+1:])
                elif not self.prefix:
                    backups.append(key)
        return backups

    def delete(self, remote_path: str):
        key = self._get_key(remote_path)
        self.s3.delete_object(Bucket=self.bucket_name, Key=key)
