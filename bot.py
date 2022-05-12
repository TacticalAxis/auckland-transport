import discord
from discord.ext import commands
from api import *
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import *
import discord_slash

TOKEN = os.environ.get('AUTHTOKEN')

client = commands.Bot(command_prefix="$")
slash = SlashCommand(client, sync_commands=True)
guilds = [814596744472952902, 453460088590434305, ]

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="{} vehicles".format(getActiveNumber())))
    print("Bot Ready!")

# /locate command
@slash.slash(
    name="locate",
    description="Locate a bus",
    guild_ids=guilds,
    options=[
        create_option(
            name="vehicleid",
            description="set the bus ID",
            required=True,
            option_type=3
        )
    ]
)
async def _locate(ctx:SlashContext, vehicleid:str):
    msg = await ctx.send("`Loading Vehicle: {}`".format(vehicleid.upper()))
    data = getVehicle(vehicleid.upper())
    if not data == None:
        if data["type"] == "ferry":
            embed = discord.Embed(title=":{}:  [Details for {}: {}]".format(data["type"], data["type"].capitalize(), data["label"]), description="Details for Auckland Transport Ferry Service", color=0x00ff00)
            embed.add_field(name="Location", value="https://www.google.com/maps/search/?api=1&query={},{}".format(data["latitude"], data["longitude"]), inline=False)
            embed.add_field(name="Speed", value="{:.1f} km/h".format(data["speed"]), inline=False)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/867736415994511390/872670352843608074/boat.png")
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(title=":{}:  [Details for {}: {}]".format(data["type"], data["type"].capitalize(), data["route_short"]), description=data["route_description"], color=0x00ff00)
            embed.add_field(name="Location", value="https://www.google.com/maps/search/?api=1&query={},{}".format(data["latitude"], data["longitude"]), inline=False)
            embed.add_field(name="Speed", value="{:.1f} km/h".format(data["speed"]), inline=False)
            embed.add_field(name="Destination/Next Stop: {}".format(data["next_stop"]), value="Location: {}\nTime: {}".format(data["next_stop_name"], data["next_stop_time"]), inline=False)
            if data["type"] == "train":
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/867736415994511390/872670376520466442/train.png")
            else:
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/867736415994511390/872670391133421608/bus.png")
            await ctx.channel.send(embed=embed)
    else:
        await ctx.send("`Sorry, no vehicle with ID: {} was found!`".format(vehicleid.upper()))

# /locate command
@slash.slash(
    name="stop",
    description="Get Stop Information",
    guild_ids=guilds,
    options=[
        create_option(
            name="stopid",
            description="Set the stop ID",
            required=True,
            option_type=3
        )
    ]
)
async def _stop(ctx:SlashContext, stopid:str):
    msg = await ctx.send("`Loading Stop: {}`".format(stopid))
    data = getStopInfo(stopid, 5)
    if not data == None:
        embed = discord.Embed(title=":busstop:  [Details for Stop {}]".format(stopid), description="Stop Realtime Board Information", color=0x00ff00)
        
        for i in data:
            embed.add_field(name="@{} >> {} -> {}".format(i["departure_time"], i["route_short_name"], i["trip_headsign"]), value="{}".format(i["route_long_name"]), inline=False)
        
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/867736415994511390/872670391133421608/bus.png")
        await ctx.channel.send(embed=embed)
    else:
        await ctx.send("`Sorry, no Stop ID: {} was found!`".format(stopid))

client.run(TOKEN)