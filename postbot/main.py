import discord
from discord.ext import commands
import logging
import json
import os
from discord import SelectOption, SelectMenu
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(funcName)s][%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
# 遍覽 cogs 並 get logger
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        logger = logging.getLogger(f'cogs.{filename[:-3]}')
        logger.setLevel(logging.INFO)
        logger.info(f'Loaded {filename}')

with open('config.json', 'r') as f:
    config = json.load(f)
    TOKEN = config['TOKEN']

bot = commands.Bot(command_prefix='!', intents=intents)

# 當啟動機器人時
@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    logging.info(f"載入 {len(slash)} 個斜線指令")
    logging.info(f'Logged in as {bot.user.name}')
    # await reload_cogs()

# 載入所有 cogs 資料夾中的檔案
async def reload_cogs():
    # 載入 所有 cogs 資料夾中的檔案
    for filename in os.listdir('./cogs'):
        try:
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logging.info(f'Loaded {filename}')
        except Exception as e:
            logging.error(f'Failed to load {filename} with error: {e}')

# 重新載入所有 cogs
@bot.tree.command(name = "reload", description = "重新載入所有 cogs")
async def reload(ctx):
    if ctx.user.id != 959977374471028779:
        await ctx.response.send_message("你沒有權限執行此指令", ephemeral=True)
        return
    await reload_cogs()
    cogs = [cog for cog in bot.cogs]
    embed = discord.Embed(title = "重新載入 cogs", description = f"已經重新載入所有 cogs", color=discord.Color.green())
    for cog in cogs:
        embed.add_field(name = cog + ".py", value = "✅", inline = True)
    embed.set_thumbnail(url = "https://img.onl/AuuWMV")
    await ctx.response.send_message(embed=embed, ephemeral=True)

# 所有 cogs 的下拉選單
class CogSelect(SelectMenu):
    def __init__(self, cogs):
        options = [SelectOption(label=cog, value=cog) for cog in cogs]

        super().__init__(custom_id="cog_select", placeholder="選擇一個 cog...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction):
        cog_name = interaction.data["values"][0]
        await bot.unload_extension(f'cogs.{cog_name}')
        embed = discord.Embed(title = "卸載 cogs", description = f"已經卸載 {cog_name}", color=discord.Color.green())
        embed.set_thumbnail(url = "https://img.onl/AuuWMV")
        await interaction.response.send_message(embed=embed, ephemeral=True)

# 由下拉選單中卸載指定 cog
@bot.tree.command(name="unload", description="由下拉選單中卸載指定 cog")
async def unload(ctx):
    if ctx.user.id != 959977374471028779:
        await ctx.response.send_message("你沒有權限執行此指令", ephemeral=True)
        return
    cogs = [cog for cog in bot.cogs]
    select = CogSelect(cogs)
    await ctx.response.send_message("請選擇一個 cog 來卸載：", components=[select])

# 暫時讓機器人down
@bot.tree.command(name = "down", description = "關閉機器人")
async def down(ctx):
    if ctx.user.id != 959977374471028779:
        await ctx.response.send_message("你沒有權限執行此指令", ephemeral=True)
        return
    await ctx.response.send_message("機器人已關閉", ephemeral=True)
    await bot.close()

# 同步Slash Command
@bot.tree.command(name = "sync", description = "同步Slash Command")
async def sync(ctx):
    if ctx.user.id != 959977374471028779:
        await ctx.response.send_message("你沒有權限執行此指令", ephemeral=True)
        return
    await ctx.response.defer(ephemeral=True)
    slash = await bot.tree.sync()
    embed = discord.Embed(title = "同步斜線指令", description = f"已經同步 {len(slash)} 個斜線指令", color=discord.Color.green())
    embed.set_thumbnail(url = "https://img.onl/AuuWMV")
    await ctx.response.send_message(embed=embed)

bot.run(TOKEN)