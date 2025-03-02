import asyncio
import logging
from dataclasses import dataclass
from typing import BinaryIO
from uuid import uuid4

from miniopy_async import Minio  # type:ignore[import-untyped]
from miniopy_async.error import MinioException  # type:ignore[import-untyped]

from crudik.adapters.config import FilesConfig
from crudik.application.errors.common import ApplicationError

MINIO_BUCKET_NAME = "images"


class FileUploadError(ApplicationError): ...


@dataclass(slots=True, frozen=True)
class MinioFileManager:
    minio: Minio
    config: FilesConfig

    async def upload(self, file: BinaryIO, ext: str, size: int) -> str:
        fname = f"{uuid4()}.{ext}"
        await asyncio.to_thread(file.seek, 0)

        try:
            found_bucket = await self.minio.bucket_exists(MINIO_BUCKET_NAME)
            if not found_bucket:
                logging.info("Created bucket %s", MINIO_BUCKET_NAME)
                await self.minio.make_bucket(MINIO_BUCKET_NAME)

            info = await self.minio.put_object(
                MINIO_BUCKET_NAME,
                fname,
                file,
                length=size,
                part_size=5 * 1024 * 1024,
            )
            file_path = f"{self.config.file_server}/{info.object_name}"
        except MinioException as exc:
            logging.exception("While uploading image to S3")
            raise FileUploadError from exc

        return file_path
