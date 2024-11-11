async def notify(content: str, nickname: str) -> str:
    message = f"Hello, {nickname}! Your notification:\n{content}"
    return message
