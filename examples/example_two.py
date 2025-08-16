
import asyncio
from engine import GoogleEngine


API_KEY = "ABCDEFGHIJKLMNOPQ"
CSE_ID = "123ab456c789de012"


async def main():
    engine = GoogleEngine(API_KEY, CSE_ID)
    await engine.connect()
    results = await engine.search("pyrogram", num=3)
    print(results)
    await engine.close()


if __name__ == "__main__":
    asyncio.run(main())
