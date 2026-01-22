import discord
from anilist.parser import getTitle, formatDate
import datetime

class SearchView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=60)
        try:
            
            self.media = data["data"]["Page"]["media"]
            self.idx = 0
        
            self.username = ""
            self.watchButton = discord.ui.Button(label="Watch on HiAnime", url=f"https://hianime.to/search?keyword={str(getTitle(self.media[self.idx])).replace(' ', '+')}", style=discord.ButtonStyle.link)
            self.anilistButton = discord.ui.Button(label="Anilist", url=f"https://anilist.co/anime/{self.media[self.idx]['id']}", style=discord.ButtonStyle.link)
            self.add_item(self.anilistButton)
            self.add_item(self.watchButton)
        except Exception as e:
            print(e)

    def currentEmbed(self, username: str):
        self.username = username
        media: dict = self.media[self.idx]
        title = getTitle(media)

        watchUrl = f"https://hianime.to/search?keyword={str(title).replace(' ', '+')}"

        embed = discord.Embed(
                    title=title,
                    url=f"https://anilist.co/anime/{media['id']}",
                    colour=discord.Colour.teal()
                    )


        genres = ', '.join(media.get('genres', "N/A"))
        episodes = media.get('episodes', "N/A")
        status = media.get('status', "N/A")
        score = media.get('averageScore', "N/A")
        format = media.get('format', "N/A")

        start = formatDate(media.get('startDate', []))

        end = formatDate(media.get('endDate', []))

        info = f"Episodes: {episodes}\nGenres: {genres}\nStatus: {status.title()}\nScore: {score}\nFormat: {format}\nStart Date: {start}\nEnd Date: {end}"
        embed.set_image(url=media["coverImage"]["large"])
        embed.add_field(name="", value=info)
        

        embed.set_footer(text=f"Search result {self.idx  + 1} of {len(self.media)}. Command run by {username}")
        embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
        return embed
    
    @discord.ui.button(label="Next result")
    async def retry(self, interaction: discord.Interaction, button):

        self.idx = (self.idx + 1) % len(self.media)
        
        media: dict = self.media[self.idx]
        title = getTitle(media)

        watchUrl = f"https://hianime.to/search?keyword={str(title).replace(' ', '+')}"
        self.watchButton.url = watchUrl
        self.anilistButton.url = f"https://anilist.co/anime/{media['id']}"
        await interaction.response.edit_message(
            embed=self.currentEmbed(self.username),
            view=self
        )

class NextView(discord.ui.View):
        def __init__(self, data):
            super().__init__(timeout=60)
            self.page = data["data"]["Page"]
            self.username = ""

        def embedData(self, username: str, num: int):
            self.username = username
            embed = discord.Embed(
            title = f"Next {num} anime airing",
            color = discord.Color.teal()
            )
            for idx, item in enumerate(self.page['airingSchedules'], start=1):
                media = item['media']
                title = getTitle(media)
                episode = item['episode']
                airing = item['airingAt']
                genres = ', '.join(media.get('genres', ["N/A"]))
                main = f"{idx}. {title} (Ep. {episode})"
                info = f"Genres: {genres}\nAirs: <t:{airing}:F> (<t:{airing}:R>)"
                embed.add_field(name=main, value=info, inline=False)
                if idx >= 25:
                    break
                embed.set_footer(text=f"Next {min(num, 25)} anime. Command run by {username}")
                embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
            return embed