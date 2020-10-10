from multiprocessing.connection import Client
import discord
from discord import Embed
from discord.ext import commands
from discord.shard import ShardInfo
from discord.user import User
from discord.utils import get
from datetime import datetime
import os
import collections
import time, datetime
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        '''Get information about the bot.'''
        infoembed = discord.Embed(title="Info", description="A Utilities Discord Bot with reliability and simplicity", color=0x7289DA)
        infoembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        infoembed.add_field(name= "<:news:758781954073821194> News", value="<:translate:758449663517917195> Translators Needed. <:translate:758449663517917195>\nIf you can speak another language fluently or know someone who can DM isirk#0001.", inline=True)
        infoembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/758451109919981580.png?v=1")
        infoembed.add_field(name= ":link: Links", value="[Invite](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&redirect_uri=https%3A%2F%2Fastrobot.carrd.co%2F&response_type=code&scope=bot%20identify)\n[Bot Site](https://asksirk.com/Astro) \n[Github Repository](https://github.com/ISIRK/Astro) \n[Patreon](https://www.patreon.com/Astro_Bot)", inline=False)
        infoembed.set_footer(text="Astro Bot | discord.gg/7yZqHfG")
        await ctx.send(embed=infoembed)

    @commands.command()
    async def support(self, ctx):
        '''Get support information.'''
        supportembed = discord.Embed(title="Support", color=0x7289DA)
        supportembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        supportembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/758453150897799172.png?v=1")
        supportembed.add_field(name="Support Server", value="Support Server: https://discord.gg/7yZqHfG", inline=False)
        supportembed.add_field(name="Contact", value="To contact dm isirk#0001 or email me @ isirk@asksirk.com", inline=False)
        supportembed.add_field(name=":link: Links", value="Bot Site: https://asksirk.com/Astro\nGithub Repository: https://github.com/ISIRK/Astro\nPatreon: https://www.patreon.com/Astro_Bot", inline=False)
        supportembed.set_footer(text="Use [prefix] help or info.")
        await ctx.send(embed=supportembed)
    
    @commands.command()
    async def invite(self , ctx):
        '''Get the invite for the bot.'''
        embed = discord.Embed(title="Invite", description="[Invite](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&redirect_uri=https%3A%2F%2Fastrobot.carrd.co%2F&response_type=code&scope=bot%20identify)", color=0x7289DA)
        embed.add_field(name="Contact", value="To contact either dm @isirk#0001 or\nJoin Our [Discord Server](https://discord.gg/7yZqHfG)\n\nhttps://discord.gg/7yZqHfG", inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/758138226874908705/758729610237837372/astro.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx):

        helpembed1 = discord.Embed(title="Help", description="A Utilities Discord Bot with reliability and simplicity\n Made By isirk#0001", color=0x7289DA)
        helpembed1.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        helpembed1.add_field(name="Prefix", value="`@Astro ,Astro ,astro ,^`", inline=False)
        helpembed1.add_field(name= "Help", value="React below to change the pages.", inline=False)
        helpembed1.add_field(name="Pages", value="```yaml\n1) Info\n2) Utility\n3) Mod\n4) Dev\n```", inline=False)
        helpembed1.add_field(name="About", value="Version 1.0 **Public Beta**\nMade with :heart: in <:python:758139554670313493>\nOwned, Developed, and Run by isirk#0001", inline=False)
        helpembed1.set_footer(text="Astro Bot | discord.gg/7yZqHfG")
        
        info = discord.Embed(title="Info", description="Information Commands", color=discord.Colour.blurple())
        info.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        info.add_field(name="Commands:", value="`info` - Get Info About the Bot.\n`invite` - Get the invite for Astro.\n`support` Get Support Information.", inline=False)
        info.set_footer(text="Astro Bot | discord.gg/7yZqHfG")

        utility = discord.Embed(title="Utility", description="Utiity Commands", color=discord.Colour.blurple())
        utility.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        utility.set_footer(text="Astro Bot | discord.gg/7yZqHfG")
        utility.add_field(name="Syntax:", value="```yaml\n<input> - Input for the Command\n[o] - Optional\n```", inline=False)
        utility.add_field(name="Commands:", value="`avatar|av <[o]mention>` - Get the avatar of the mentioned user.\n`ping` - Get the Bot Ping.\n`server` - Get Info About The Server.\n`stats` - Get the Bot Stats.\n`user <[o]mention>` - Get the Stats of the Mentioned User.", inline=False)
        
        mod = discord.Embed(title="Mod", description="Moderation Commands", color=discord.Colour.blurple())
        mod.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        mod.set_footer(text="Astro Bot | discord.gg/7yZqHfG")
        mod.add_field(name="Syntax:", value="```yaml\n<input> - Input for the Command\n```", inline=False)
        mod.add_field(name="Commands:", value="`kick <user>` - Kick the mentioned user from the server.\n`ban <user>` - Ban the mentioned user from the server.\n`clear <#>` - Delete a number of messages.(Max 100)\n`slowmode <seconds>` - Change the Channel Slowmode to a specified number of seconds.\n~~~`mute <user>` - Mute a User.~~~ (Re-Working)\n~~~`unmute <user>` - Un-mutes a User.~~~ (Re-Working)", inline=False)
        
        dev = discord.Embed(title="Dev", description="Developer Commands\n***Note Only the Bot Owner Can Use These***", color=discord.Colour.blurple())
        dev.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        dev.set_footer(text="Astro Bot | discord.gg/7yZqHfG")
        dev.add_field(name="Syntax:", value="```yaml\n<input> - Input for the Command\n[o] - Optional\n```", inline=False)
        dev.add_field(name="Commands:", value="`jsk` - Jishaku\n`dm <user> <message>` - Dm the mentioned User from the Server.\n`leaveguild` - Leave the current server\n`status <type> <[o]status>` - Change the bot status.\n`say <message>` - Make the bot say a message.", inline=False)
        
        embeds = [
            helpembed1,
            info,
            utility,
            mod,
            dev
        ]

        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()
     
def setup(bot):
    bot.add_cog(info(bot))
