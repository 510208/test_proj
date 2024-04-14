import discord
from discord.ext import commands
from discord import app_commands
import logging

# 設定 logger
logger = logging.getLogger(__name__)
class Announcement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name = "put_annou", description = "經模態框推送公告")
    async def hello(self, ctx):
        if ctx.author.id != 959977374471028779:
            await ctx.send("你沒有權限執行此指令")
            return
        await annouInput().start(ctx)
        logger.info(f"User {ctx.author} has put an announcement")

# 繼承 discord.ui.Modal 類別，並傳入 title 參數
class annouInput(discord.ui.Modal, title = "公告內容設定"):
    annouTitle = discord.ui.TextInput(label = "公告標題",
                                        placeholder = "請輸入公告標題",
                                        min_length = 1,
                                        max_length = 50,
                                        style=discord.TextStyle.short,
                                        required=True
                                    )
    annouContent = discord.ui.TextInput(label = "公告內容",
                                        placeholder = "請輸入公告內容(可使用 Markdown 語法)",
                                        min_length = 1,
                                        max_length = 200,
                                        style=discord.TextStyle.paragraph,
                                        required=True
                                    )
    annouImage = discord.ui.TextInput(label = "圖片連結",
                                        placeholder = "請輸入圖片連結",
                                        min_length = 1,
                                        style=discord.TextStyle.short
                                    )
    annouColor = discord.ui.TextInput(label = "顏色",
                                        placeholder = "請輸入顏色十六進位色碼，需帶有#",
                                        min_length = 7,
                                        max_length = 7,
                                        style=discord.TextStyle.short,
                                        required=True
                                    )

    # Modal 提交後接著要執行的程式碼
    async def on_submit(self, interaction: discord.Interaction):
        # 以 Embed 方式推送公告
        embed = discord.Embed(title = self.annouTitle.value,
                                description = self.annouContent.value,
                                color = discord.Color.from_rgb(
                                    int(self.annouColor.value[1:3], 16),
                                    int(self.annouColor.value[3:5], 16),
                                    int(self.annouColor.value[5:7], 16)
                                    )
                            )
        if self.annouImage.value:
            embed.set_image(url = self.annouImage.value)
        
        # 傳送到頻道ID 1187756393378353252
        channel = self.bot.get_channel(1187756393378353252)
        await channel.send(embed = embed)

async def setup(bot):
    await bot.add_cog(Announcement(bot))