
import asyncio
from engine import GoogleEngine
from engine.exceptions import (
    InvalidAPIKeyError,
    APILimitExceededError,
    NetworkError,
)

API_KEY = "AIzaSyB457AfQGH5Gu9dVu5UYcelJ-1ZrlNC29Y"
CSE_ID = "306df78b399234816"


async def main():
    engine = GoogleEngine(API_KEY, CSE_ID)
    await engine.connect()
    results = await engine.search("pyrogram", num=3)
    print(results)
    await engine.close()


if __name__ == "__main__":
    asyncio.run(main())
