from discord.ext import commands
from discord.ext.commands import CommandNotFound
import discord, asyncio, datetime, random, asyncio, json, requests

APIKEY = "" #TRN API KEY

rankedStats = {}

bot = commands.Bot(command_prefix='!')

def getApexProfile(username):
    r = requests.get(f"https://public-api.tracker.gg/apex/v1/standard/profile/5/{username}",headers={"TRN-Api-Key":APIKEY})
    return json.loads(r.text)

def getRankInformation(username):
    profile = getApexProfile(username)["data"]
    rankName3v3 = profile["stats"][3]["metadata"]["description"]
    rankPoints3v3 = profile["stats"][3]["value"]
    rankNameArena = profile["stats"][4]["metadata"]["description"]
    rankPointsArena = profile["stats"][4]["value"]
    avatarUrl = profile["metadata"]["avatarUrl"]
    level = profile["metadata"]["level"]

    # save to hashmap
    rankedStats[username]=[{"rank3v3":rankName3v3,"rp3v3":rankPoints3v3},{"rankarena":rankNameArena,"rpArena":rankPointsArena}]

    return [username,level,avatarUrl,rankName3v3,rankPoints3v3,rankNameArena,rankPointsArena,profile["metadata"]["rankImage"]]

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=5, name="Apex Legends"))
    print('=> Logged in as {0.user}'.format(bot))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

@bot.command()
async def stats(ctx, username):
    try:
        profile = getRankInformation(username)
        embed=discord.Embed(description="Level " + str(profile[1]),timestamp=datetime.datetime.utcnow())
        embed.set_author(name=username + "'s stats",icon_url=profile[2])
        embed.set_thumbnail(url=profile[7])
        embed.add_field(name="Battle Royale",value=profile[3] + " - " + str(profile[4]))
        embed.add_field(name="Arenas",value=profile[5] + " - " + str(profile[6]))
        await ctx.reply(embed=embed)
    except:
        await ctx.message.add_reaction('❌')

bot.run("")
