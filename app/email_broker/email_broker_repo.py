from abc import ABC, abstractmethod
import logging


class AbstractEmailBroker(ABC):
    _log = logging.getLogger()

    @abstractmethod
    async def connect(self) -> None:
        self._log.debug("Email broker was connected successfully")

    @abstractmethod
    async def close(self) -> None:
        self._log.debug("Email broker was closed successfully")

    @abstractmethod
    async def send_email(self, recipient: str, content: str, nickname: str) -> None:
        self._log.debug("Email was send successfully")

    @abstractmethod
    async def distribute_emails(self) -> None:
        self._log.debug("Email broker began distributing emails")


class EmailBrokerRepo(AbstractEmailBroker):
    def __init__(self, email_broker: AbstractEmailBroker):
        self._email_broker = email_broker

    async def connect(self) -> None:
        return await self._email_broker.connect()

    async def close(self) -> None:
        return await self._email_broker.close()

    async def send_email(self, recipient: str, content: str, nickname: str) -> None:
        return await self._email_broker.send_email(recipient, content, nickname)

    async def distribute_emails(self) -> None:
        return await self._email_broker.distribute_emails()
