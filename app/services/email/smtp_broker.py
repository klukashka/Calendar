from app.services.email_broker_repo import AbstractEmailBroker
from aiosmtplib.smtp import SMTP
from aiosmtplib.errors import SMTPException
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from app.db.repositories.email import EmailRepo
from app.schemas.email import EmailRead


class SMTPBroker(AbstractEmailBroker):
    def __init__(
            self,
            mail: SMTP,
            async_session_maker: async_sessionmaker[AsyncSession],
            admin_email: str,
            admin_email_password: str,
    ) -> None:
        self._mail = mail
        self._async_session_maker = async_session_maker
        self._sender = admin_email
        self._password = admin_email_password
        self.batch_size = 1000

    async def connect(self) -> None:
        await self._mail.connect()
        await self._mail.login(self._sender, self._password)
        if not await self._mail.noop():
            raise RuntimeError("Failed to connect SMTP server")

    async def close(self) -> None:
        await self._mail.quit()

    async def send_email(self, recipient: str, content: str, nickname: str) -> None:
        """Send an email from admin server to a user"""
        message = f"Hello, {nickname}!\n" + content
        try:
            await self._mail.sendmail(self._sender, recipient, message)
        except SMTPException as e:
            raise SMTPException(f"Failed to send email to {recipient}") from e

    async def distribute_emails(self) -> None:
        """Main email-distribution function"""
        offset = 0
        async with self._async_session_maker() as _session:
            email_repo = EmailRepo(_session)
            while True:
                email_infos = await self._fetch_emails(email_repo, offset)
                try:
                    # Try to take the first note
                    first_info = await anext(email_infos)
                    await self.send_email(first_info.email, first_info.message, first_info.nickname)
                    offset += self.batch_size
                    # Continue if there was a note
                    async for info in email_infos:
                        await self.send_email(info.email, info.message, info.nickname)
                except StopAsyncIteration:
                    break
                except Exception as e:  # discard changes if Error occurs during distribution
                    await email_repo.roll_back()
                    raise Exception() from e

    async def _fetch_emails(
            self,
            email_repo: EmailRepo,
            offset: int,
    ) -> AsyncGenerator[EmailRead, None] | None:
        """Fetch a batch of emails using EmailRepo"""
        return email_repo.get_notes_to_send(offset, self.batch_size + offset)
