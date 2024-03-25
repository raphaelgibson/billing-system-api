from abc import ABCMeta, abstractmethod
from datetime import date
from io import BytesIO

from pydantic import BaseModel


class GenerateInvoiceServiceSchema(BaseModel):
    creditor_name: str
    creditor_document: str
    debtor_name: str
    debtor_document: str
    debt_amount: str
    document_number: str
    document_date: date
    debt_due_date: date
    bank_code: str


class GenerateInvoiceService(metaclass=ABCMeta):
    Input = GenerateInvoiceServiceSchema

    @abstractmethod
    def generate(self, data: Input) -> BytesIO:
        raise NotImplemented
