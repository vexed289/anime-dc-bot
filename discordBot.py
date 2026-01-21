import discord
from discord.ext import commands
import requests
import json
from bs4 import BeautifulSoup
#DISCORD BOT SETUP
variables = {}
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def next(ctx, num=5):
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
    variables = {
        "perPage": num
    }

    res = requests.post(url, json={"query": query, "variables": variables})
    if res.status_code == 200:
        data = res.json()
        embed = discord.Embed(
            title = f"Next {num} anime airing",
            color = discord.Color.teal()
        )
        for idx, item in enumerate(data['data']['Page']['airingSchedules'], start=1):
            media = item['media']
            title = media['title']['english'] or media['title']['romaji'] or media['title']['native']
            episode = item['episode']
            airing = item['airingAt']
            genres = ', '.join(media.get('genres', [])) # .get is safer than media['genres'] because it returns default value [] if anilist doesn't have the genres
            main = f"{idx}. {title} (Ep. {episode})"
            info = f"Genres: {genres}\nAirs: <t:{airing}:F> (<t:{airing}:R>)"
            embed.add_field(name=main, value=info, inline=False)
            if idx >= 25:
                break
        await ctx.send(embed=embed)
    else:
        await ctx.send(res.status_code)
def result(res, num=0):
    data = res.json()
    media = data['data']['Page']['media'][num]
    url = f"https://anilist.co/anime/{media['id']}"
    res = requests.get(url)
    if res.status_code == 200:
        parser = BeautifulSoup(res.text, "html.parser")
        attrs = {
            "class": "cover"
        }
        imgs = parser.find("img", attrs=attrs)   # type: ignore
        imgUrl = None
        if imgs:
            if "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/" in imgs["src"]:
                imgUrl = imgs["src"] # type: ignore
                    

        name = (media['title']['english'] or media['title']['romaji'] or media['title']['native'])
        watchUrl = f"https://hianime.to/search?keyword={str(name).replace(' ', '+')}"
        embed = discord.Embed(
            title = name,
            url = watchUrl,
            color = discord.Color.teal()
        )
        genres = ', '.join(media.get('genres', []))
        if genres == []:
            genres = "N/A" 
        episodes = media['episodes']
        status = str(media.get('status', []))
        if status == []: status = "N/A"
        score = media.get('averageScore', [])
        if score == []: score = "N/A"
        format = media.get('format', [])
        if format == []: format = "N/A"
        start = media.get('startDate', [])
        if start is not []: start = f"{start['day']}/{start['month']}/{start['year']}"
        else: start = "N/A"
        end = media.get('endDate', [])
        if end is not []: end = f"{end['day']}/{end['month']}/{end['year']}"
        else: end = "N/A"
        info = f"Episodes: {episodes}\nGenres: {genres}\nStatus: {status.title()}\nScore: {score}\nFormat: {format}\nStart Date: {start}\nEnd Date: {end}"
        embed.set_image(url=imgUrl)
        embed.add_field(name="", value=info, inline=True)
        view = discord.ui.View()
        button = discord.ui.Button(label="AniList", url=url, style=discord.ButtonStyle.link)
        view.add_item(button)

        return embed, view


@bot.command()
async def search(ctx, name=""):
    if name == "":
        await ctx.send("No name provided.")
        return
    url = "https://graphql.anilist.co"
    query ='''
query ($search: String!) {
  Page(perPage: 10) {
    media(search: $search, type: ANIME) {
      id
      title {
        english
        romaji
        native
      }
      genres
      episodes
      status
      format
      duration
      averageScore
      startDate {
        year
        month
        day
      }
      endDate {
        year
        month
        day
      }
    }
  }
}

    '''
    variables = {
        "search": str(name)
    }
    res = requests.post(url, json={"query": query, "variables": variables})
    if res.status_code == 200:
        attempt = 0
        embed, view = result(res, attempt) # type: ignore
        async def retryCallback(interaction): # THIS IS BROKEN
            nonlocal attempt
            attempt += 1
            await interaction.response.defer()
            embed, view = result(res, attempt)
            await interaction.followup.send(embed=embed, view=view)

        retry = discord.ui.Button(label="Wrong result?")
        retry.callback = retryCallback
        view.add_item(retry)
        await ctx.send(embed=embed, view=view)


    else:
        await ctx.send(res.status_code)


with open("token.txt", 'r') as token:
    bot.run(token=token.readline())