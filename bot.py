import discord
from discord.ext import commands
from api import *
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import *
import discord_slash
from discord_buttons import *

TOKEN = os.environ.get('AUTHTOKEN')

client = commands.Bot(command_prefix="$")
slash = SlashCommand(client, sync_commands=True)
ddb = DiscordButton(client)
guilds = [814596744472952902, 453460088590434305]

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="{} vehicles".format(getActiveNumber())))
    print("Bot Ready!")

#/locatebus
@slash.slash(
    name="locate",
    description="Locate a bus",
    guild_ids=guilds,
    options=[
        create_option(
            name="bus-id",
            description="set the bus ID",
            required=True,
            option_type=3
        )
    ]
)
async def _locate(ctx:SlashContext, busNo:str):
    msg = await ctx.send("`Loading Bus: {}`".format(busNo.upper()))
    data = getVehicle(busNo.upper())
    if not data == None:
        embed = discord.Embed(title=":{}:  [Details for {}: {}]".format(data["type"], data["type"].capitalize(), data["route_short"]), description=data["route_description"], color=0x00ff00)
        embed.add_field(name="Location", value="https://www.google.com/maps/search/?api=1&query={},{}".format(data["latitude"], data["longitude"]), inline=False)
        embed.add_field(name="Speed", value="{:.1f} km/h".format(data["speed"]), inline=False)
        embed.add_field(name="Destination/Next Stop: {}".format(data["next_stop"]), value="Location: {}\nTime: {}".format(data["next_stop_name"], data["next_stop_time"]), inline=False)
        await ctx.channel.send(embed=embed)
    else:
        await ctx.send("`Sorry, no vehicle with ID: {} was found!`".format(busNo.upper()))

client.run(TOKEN)