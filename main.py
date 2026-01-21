from bot import createBot
from commands.search import Search
from commands.next import Schedule

bot = createBot()

# 2 commands - !search {name: str} and !next {num: int}. They should output their respective embeds

bot.run(open("otherStuff/token.txt").read().strip())