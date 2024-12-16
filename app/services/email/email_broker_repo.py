from abc import ABC, abstractmethod
import logging


class AbstractEmailBroker(ABC):
    _log = logging.getLogger()

    @abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def send_email(self, recipient: str, content: str, nickname: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def distribute_emails(self) -> None:
        raise NotImplementedError


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
