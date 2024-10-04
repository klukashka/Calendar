import aiosmtplib
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from app.db.repositories.email import EmailRepo


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
        # await self._mail.starttls()
        await self._mail.login(self._sender, self._password)
        # should add catching errors

    async def send(self, recipient: str, subject: str, content: str, nickname: str):
        """Sends an email from one user to another"""
        message = f"Hello, {nickname}!\n" + content
        await self._mail.sendmail(self._sender, recipient, message)

    async def close(self):
        """Closes smtp server and quits all the processes"""
        await self._mail.quit()

    # or is it better to init email_repo once
    async def super_send(self, batch_size: int = 100):
        offset = 0
        async with self._async_session_maker() as _session:
            email_repo = EmailRepo(_session)
            while True:
                email_infos = email_repo.get_notes_to_send(offset, batch_size + offset)
                print(type(email_infos))
                if not email_infos:
                    break
                async for info in email_infos:
                    # needs to be converted into their types (str bool etc...)
                    print(info)
                    await self.send(info.email, "Notification", info.message, info.nickname)
                offset += batch_size
