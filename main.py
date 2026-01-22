import asyncio
from bot import createBot
from commands.search import Search
from commands.next import Schedule

async def main():
    bot = createBot()

    await bot.add_cog(Search(bot))
    await bot.add_cog(Schedule(bot))

    with open("otherStuff/token.txt", "r") as f:
        token = f.read().strip()

    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
    print("bot running")