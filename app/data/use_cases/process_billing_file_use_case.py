import aiosmtplib
from asyncio import create_task, gather
from csv import DictReader
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from io import TextIOWrapper
from uuid import uuid4
from typing import BinaryIO


from app.domain.use_cases import ProcessBillingFileUseCaseInterface
from app.data.protocols import GenerateInvoiceService


class ProcessBillingFileUseCase(ProcessBillingFileUseCaseInterface):
    def __init__(
        self,
        generate_invoice_service: GenerateInvoiceService,
        sender_email: str,
        sender_password: str,
        smtp_server: str,
        smtp_port: int,
    ):
        self.__generate_invoice_service = generate_invoice_service
        self.__sender_email = sender_email
        self.__sender_password = sender_password
        self.__smtp_server = smtp_server
        self.__smtp_port = smtp_port

    async def execute(self, billing_file: BinaryIO) -> ProcessBillingFileUseCaseInterface.Output:
        billing_file_text = TextIOWrapper(billing_file, encoding='utf-8')
        billing_file_data = DictReader(billing_file_text)

        smtp = aiosmtplib.SMTP(hostname=self.__smtp_server, port=self.__smtp_port, start_tls=True)
        await smtp.connect()
        await smtp.login(self.__sender_email, self.__sender_password)

        tasks = []
        actual_date = datetime.now().date()

        for row in billing_file_data:
            if datetime.strptime(row['debtDueDate'], '%Y-%m-%d').date() < actual_date:
                continue

            debtor_name = row['name']
            debtor_email = row['email']

            invoice_data = GenerateInvoiceService.Input(
                creditor_name='Kanastra',
                creditor_document='00.000.000/0001-91',
                debtor_name=debtor_name,
                debtor_document='000.000.000-00',
                debt_amount=row['debtAmount'],
                document_number=row['governmentId'],
                document_date=datetime.now().date(),
                debt_due_date=datetime.strptime(row['debtDueDate'], '%Y-%m-%d').date(),
                bank_code='001',
            )

            invoice = self.__generate_invoice_service.generate(invoice_data)

            msg = MIMEMultipart()
            msg['Subject'] = 'Pagamento pendente'
            msg['From'] = self.__sender_email
            msg['To'] = debtor_email

            attachment = MIMEApplication(invoice.read(), _subtype='pdf')
            attachment_name = f"{debtor_name.lower().replace(' ', '_')}_pending_debts.pdf"
            attachment.add_header('Content-Disposition', 'attachment', filename=attachment_name)
            msg.attach(attachment)

            task = create_task(smtp.send_message(msg))
            tasks.append(task)

        await gather(*tasks)
        await smtp.quit()

        return ProcessBillingFileUseCaseInterface.Output(
            id=str(uuid4()), uploaded_at=datetime.now().astimezone().isoformat()
        )
