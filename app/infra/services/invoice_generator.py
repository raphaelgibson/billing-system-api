from io import BytesIO

from pyboleto.data import BoletoData
from pyboleto.pdf import BoletoPDF

from app.data.protocols import GenerateInvoiceService


class InvoiceData(BoletoData):
    @property
    def campo_livre(self):
        return ''.join('0' for _ in range(25))


class InvoiceGenerator(GenerateInvoiceService):
    def generate(self, data: GenerateInvoiceService.Input) -> BytesIO:
        invoice_data = InvoiceData()
        invoice_data.cedente = data.creditor_name
        invoice_data.cedente_documento = data.creditor_document
        invoice_data.sacado_nome = data.debtor_name
        invoice_data.sacado_documento = data.debtor_document
        invoice_data.valor = data.debt_amount
        invoice_data.valor_documento = data.debt_amount
        invoice_data.numero_documento = data.document_number
        invoice_data.data_documento = data.document_date
        invoice_data.data_vencimento = data.debt_due_date
        invoice_data.codigo_banco = data.bank_code
        invoice_data.quantidade = '1'

        invoice_bytes = BytesIO()
        boleto = BoletoPDF(invoice_bytes)
        boleto.drawBoleto(invoice_data)
        boleto.save()

        invoice_bytes.seek(0)

        return invoice_bytes
