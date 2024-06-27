import aiosmtplib

from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from infra.notificators.base import BaseNotificator


@dataclass
class EmailNotificator(BaseNotificator):
    smtp_server: str
    smtp_port: str
    smtp_username: str
    smtp_password: str


    async def send_notification(self, recipient: str, subject: str, body: str) -> None:
        msg = MIMEMultipart()
        msg['From'] = self.smtp_username
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        smtp = aiosmtplib.SMTP(hostname=self.smtp_server, port=self.smtp_port)
        await smtp.connect()
        await smtp.login(self.smtp_username, self.smtp_password)
        await smtp.send_message(msg)
        await smtp.quit()
