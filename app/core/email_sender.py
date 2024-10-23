from typing import AsyncGenerator
import aiosmtplib
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from app.db.repositories.email import EmailRepo
from app.schemas.email import EmailRead


class EmailSender:
    """Class for producing and sending emails from admin to users"""
    def __init__(
                 self,
                 async_session_maker: async_sessionmaker[AsyncSession],
                 admin_email: str,
                 admin_email_password:str,
                 smtp_port: int,
                 smtp_server: str,
            ):
        self._async_session_maker = async_session_maker
        self._mail = aiosmtplib.SMTP(hostname=smtp_server, port=smtp_port)
        self._sender = admin_email
        self._password = admin_email_password

    async def start(self):
        """Logs in and prepares for sending emails"""
        await self._mail.connect()
        await self._mail.login(self._sender, self._password)

    async def send_email(self, recipient: str, content: str, nickname: str):
        """Sends an email from one user to another"""
        message = f"Hello, {nickname}!\n" + content
        await self._mail.sendmail(self._sender, recipient, message)

    async def close(self):
        """Closes smtp server and quits all the processes"""
        await self._mail.quit()

    async def distribute_emails(self, batch_size: int = 100):
        """General distribution function"""
        offset = 0
        async with self._async_session_maker() as _session:
            email_repo = EmailRepo(_session)
            while True:
                email_infos = await _fetch_emails(email_repo, offset, batch_size)
                stop_iterating = await self.iterate_to_send(email_infos)
                if stop_iterating:
                    break
                offset += batch_size

    async def iterate_to_send(self, email_infos: AsyncGenerator[EmailRead, None]) -> bool:
        generator_is_empty = True
        async for info in email_infos:
            generator_is_empty = False
            await self.send_email(info.email, info.message, info.nickname)
        return generator_is_empty

async def _fetch_emails(
        email_repo: EmailRepo,
        offset: int,
        batch_size: int
) -> AsyncGenerator[EmailRead, None]:
    """Fetches emails using EmailRepo"""
    return email_repo.get_notes_to_send(offset, batch_size + offset)