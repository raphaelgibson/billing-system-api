from abc import ABCMeta, abstractmethod
from typing import BinaryIO

from pydantic import BaseModel


class UploadedFileSchema(BaseModel):
    id: str
    uploaded_at: str


class ProcessBillingFileUseCaseInterface(metaclass=ABCMeta):
    Output = UploadedFileSchema

    @abstractmethod
    async def execute(self, file: BinaryIO) -> Output:
        raise NotImplemented
