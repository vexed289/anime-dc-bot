from anilist.client import Client
from views.embeds import SearchView
from views.embeds import NextView
from discord.ext import commands
client = Client()

url = "https://graphql.anilist.co"
query = '''
query($perPage: Int) { 
    Page (perPage: $perPage){
      airingSchedules(notYetAired: true, sort: TIME) {
    		airingAt
    		episode
    		media {
      		id
          genres
      		title {
        		english
        		romaji
                native
      	}
    	}
  	}
  }
}
'''

class Schedule(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def next(self, ctx: commands.Context, *, perPage: int):
        data = await client.query(query, {"perPage": perPage})
        view: NextView = NextView(data)
        embed = view.embedData(ctx.author.display_name, num=perPage)

        await ctx.send(embed=embed, view=view)