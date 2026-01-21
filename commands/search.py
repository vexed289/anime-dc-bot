from discord.ext import commands
from anilist.client import Client
from anilist.parser import getTitle
from views.embeds import SearchView

client = Client()

query = """
query ($search: String!) {
  Page(perPage: 10) {
    media(search: $search, type: ANIME) {
      id
      title { english romaji native }
      genres
      episodes
      status
      averageScore
      coverImage { large }
    }
  }
}
"""

class Search(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def search(self, ctx: commands.Context, *, name: str):
        data = await client.query(query, {"search": name})
        view: SearchView = SearchView(data)
        embed = view.currentEmbed(ctx.author.display_name)

        await ctx.send(embed=embed, view=view)

