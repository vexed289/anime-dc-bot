import discord
from anilist.parser import getTitle
import time

class SearchView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=60)

        self.media = data["data"]["Page"]["media"]
        self.idx = 0
        self.username = ""

    def currentEmbed(self, username: str):
        self.username = username
        currentAnime = self.media[self.idx]
        title = getTitle(currentAnime)

        watchUrl = f"https://hianime.to/search?keyword={str(title).replace(' ', '+')}"

        embed = discord.Embed(
                    title=title,
                    url=watchUrl,
                    colour=discord.Colour.teal()
                    )
        
        embed.set_image(url=currentAnime["coverImage"]["large"])
        embed.set_footer(text=f"Search result {self.idx  + 1} of {len(self.media)}. Command run by {username} at <t:{int(time.time())}:t>.")
        return embed
    
    @discord.ui.button(label="Next result")
    async def retry(self, interaction: discord.Interaction, button):
        self.idx = (self.idx + 1) % len(self.media)
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
                embed.set_footer(text=f"Next {min(num, 25)} anime. Command run by {username} at <t:{int(time.time())}:t>.")
            return embed