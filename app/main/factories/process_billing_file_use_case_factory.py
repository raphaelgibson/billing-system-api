from app.data.use_cases import ProcessBillingFileUseCase
from app.infra.services import InvoiceGenerator
from app.main.env import Env


def make_process_billing_file_use_case() -> ProcessBillingFileUseCase:
    invoice_generator = InvoiceGenerator()
    sender_email = Env.sender_email
    sender_password = Env.sender_password
    smtp_server = Env.smtp_server
    smtp_port = Env.smtp_port

    return ProcessBillingFileUseCase(invoice_generator, sender_email, sender_password, smtp_server, smtp_port)
