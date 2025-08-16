
import asyncio
from engine import GoogleEngine


API_KEY = "ABCDEFGHIJKLMNOPQ"
CSE_ID = "123ab456c789de012"


async def main():
    async with GoogleEngine(API_KEY, CSE_ID) as engine:
        results = await engine.search("pyrogram", num=3)
        print(results)


if __name__ == "__main__":
    asyncio.run(main())
