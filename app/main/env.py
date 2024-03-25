from os import getenv


class Env:
    sender_email = getenv('SENDER_EMAIL', '')
    sender_password = getenv('SENDER_PASSWORD', '')
    smtp_server = getenv('SMTP_SERVER', '')
    smtp_port = int(getenv('SMTP_PORT', '587'))
