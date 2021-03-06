import discord, os, io, datetime, time, json, asyncio, random, collections, humanize, goslate
from discord.user import User
from discord.utils import get
from jishaku import codeblocks
from discord.ext import commands
from discord.shard import ShardInfo
from discord.ext.commands import context
from discord.ext.commands.cooldowns import BucketType

class misc(commands.Cog, command_attrs={'cooldown': commands.Cooldown(1, 3, commands.BucketType.user)}):
    '''Miscellaneous Commands'''
    def __init__(self, bot):
        self.bot = bot
        self.gs = goslate.Goslate()
        
    @commands.command()
    @commands.cooldown(1,5,BucketType.user)
    async def joke(self, ctx):
        '''Get a joke'''
        async with self.bot.session.get("https://dadjoke-api.herokuapp.com/api/v1/dadjoke") as r:
            resp = await r.json()
        await ctx.send(resp['joke'])
        
    @commands.command()
    async def translate(self, ctx, lang: str, *, message: str = None):
        '''Translate text to english.'''
        if ctx.message.reference:
            if ctx.message.reference.cached_message:
                message = ctx.message.reference.cached_message.content
            else:
                message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                message = message.content
        await ctx.send(embed=discord.Embed(title="Translate", description=f"Original: {message}\nTranslation: {self.gs.translate(message, lang)}", color=self.bot.color).set_footer(text=f"Translated to {self.gs.get_languages()[lang]}"))

    @commands.command()
    async def choose(self, ctx, *choices):
        '''Choose something'''
        await ctx.send('Not enough choices to pick from' if len(choices) < 2 else random.choice(choices))
        
    @commands.command()
    async def binary(self, ctx, *, text: str):
        '''Change text into binary'''
        if len(text) > 25:
            await ctx.send(f"Text given is too long.")
        else:
            async with self.bot.session.get(f'https://some-random-api.ml/binary?text={text}') as resp:
                resp = await resp.json()
            await ctx.send(resp['binary'])
        
    @commands.command()
    async def reddit(self, ctx, *, subreddit: str):
        '''Get content from a subreddit'''
        async with self.bot.session.get(f"https://www.reddit.com/r/{subreddit}/new.json") as resp:
            r = await resp.json()
        if r.get("error", None) is not None:
            return await ctx.send("Couldn't find a subreddit with that name.")

        posts = r["data"]["children"]
        if not posts:
            return await ctx.send("Apparently there are no posts in this subreddit...")
        random_post = random.choice(posts)["data"]
        posted_when = datetime.datetime.now() - datetime.datetime.fromtimestamp(random_post["created"])

        embed = discord.Embed(
            title = random_post["title"], url=random_post["url"],
            description = f"Posted by `u/{random_post['author']}` {humanize.naturaldelta(posted_when)} ago",
            colour = self.bot.color)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_image(url=random_post["url"])
        embed.set_footer(text=random_post['subreddit_name_prefixed'])

        if random_post["over_18"] and ctx.channel.is_nsfw:
            await ctx.send('⚠️ You cannot see nsfw content in a non-nsfw channel.')
        else:
            await ctx.send(embed=embed)

    @commands.command(aliases=['mc'])
    async def minecraft(self, ctx, *, username):
        '''Get a minecraft users stats'''
        async with self.bot.session.get(f'https://api.mojang.com/users/profiles/minecraft/{username}?at=') as resp:
            resp = await resp.json()
        embed=discord.Embed(title=resp['name'], description=f"ID: `{resp['id']}`", color=self.bot.color)
        embed.set_image(url=f"https://minecraftskinstealer.com/api/v1/skin/render/fullbody/{username}/800")
        embed.set_thumbnail(url=f"https://mc-heads.net/avatar/{username}/{username}.png")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=self.bot.footer)
        await ctx.send(embed=embed)

    @commands.command(aliases=['mcs'])
    async def minecraftserver(self, ctx, *, server):
        '''Get a minecraft servers stats'''
        async with self.bot.session.get(f'http://mcapi.xdefcon.com/server/{server}/full/json') as resp:
            resp = await resp.json()
                            
        embed=discord.Embed(title=f"Stats for {server}", description=f"IP: {resp['serverip']}\nStatus: {resp['serverStatus']}\nPing: {resp['ping']}\nVersion: {resp['version']}\nPlayers: {resp['players']}\nMax Players: {resp['maxplayers']}", color=self.bot.color)
        embed.set_thumbnail(url=f"https://api.minetools.eu/favicon/{server}/25565")
        embed.set_footer(text=self.bot.footer)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def hot(self, ctx, *, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        user = user or ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        emoji = "💔"
        if hot > 25:
            emoji = "❤"
        if hot > 50:
            emoji = "💖"
        if hot > 75:
            emoji = "💞"

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    '''
    @commands.cooldown(1, 15, BucketType.user)
    @commands.command()
    async def run(self, ctx, lang: str, *, code: str):
        ''Run code and get the output''
        code = codeblocks.codeblock_converter(code)[1]
        try:
            r = await self.bot.session.post("https://emkc.org/api/v1/piston/execute", json={"language": lang, "source": code})
            r = await r.json()
            out = r['output']
            if len(out) > 1000:
                await ctx.send('Output too long')
            else:
                await ctx.remove(f"```{out}```")
        except Exception as e:
            await ctx.send(f'There was an error running your code.\nError:\n```{e}```')
    '''

    @commands.cooldown(1,10,BucketType.user)
    @commands.command()
    async def weather(self, ctx, *, city_name:str):
        """Get the weather of a city/town by its name. State code is US only."""
        url = "http://api.openweathermap.org/data/2.5/weather?q=" + city_name + "&appid=168ced82a72953d81d018f75eec64aa0&units=imperial"
        async with self.bot.session.get(url) as resp:
                weather_response = await resp.json()
                if weather_response['cod'] != 200:
                    await ctx.send(f"An error ocurred: `{weather_response['message']}`.")
                else:
                    currentUnix = time.time()
                    localSunrise = weather_response['sys']['sunrise'] + weather_response['timezone']
                    sunriseTime = datetime.datetime.utcfromtimestamp(localSunrise)
                    localSunset = weather_response['sys']['sunset'] + weather_response['timezone']
                    sunsetTime = datetime.datetime.utcfromtimestamp(localSunset)
                    localTimeUnix = currentUnix + weather_response['timezone']
                    localTime = datetime.datetime.utcfromtimestamp(localTimeUnix)
                    embed = discord.Embed(
                        title=f"Weather in {weather_response['name']}, {weather_response['sys']['country']}",
                        url = f"https://openweathermap.org/city/{weather_response['id']}",
                        description=weather_response['weather'][0]['description'],
                        color=self.bot.color,
                    )
                    embed.add_field(name='Location:', value=f"**🏙️ City:** {weather_response['name']}\n**<:coordinates:727254888836235294> Longitude:** {weather_response['coord']['lon']}\n **<:coordinates:727254888836235294> Latitude:** {weather_response['coord']['lat']}", inline=False)
                    embed.add_field(name='Weather', value=f"**🌡️ Current Temp:** {weather_response['main']['temp']}°F\n**🌡️ Feels Like:** {weather_response['main']['feels_like']}°\n**🌡️ Daily High:** {weather_response['main']['temp_max']}°\n**🌡️ Daily Low:** {weather_response['main']['temp_min']}°\n**<:humidity:727253612778094683> Humidity:** {weather_response['main']['humidity']}%\n**🌬️ Wind:** {weather_response['wind']['speed']} mph", inline=False)
                    embed.add_field(name='Time', value=f"**🕓 Local Time:** {localTime.strftime('%I:%M %p')}\n **🌅 Sunrise Time:** {sunriseTime.strftime('%I:%M %p')}\n **🌇 Sunset Time:** {sunsetTime.strftime('%I:%M %p')}")
                    embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{weather_response['weather'][0]['icon']}@2x.png")
                    embed.set_footer(text=f"Weather in Fahrenheit | {self.bot.footer}", icon_url=f"https://openweathermap.org/img/wn/{weather_response['weather'][0]['icon']}@2x.png")
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)

    @commands.command()
    async def replace(self, ctx, char, *, text):
      '''Send a message with an emoji in between each word'''
      await ctx.send(text.replace(" ", f" {char} "))

    @commands.command()
    async def poll(self, ctx, title, *options):
        '''Make a quick poll'''
        reactions = {1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣", 10: "🔟"}
        s = ""
        num = 1
        for i in options: 
            s += f"{num} - {i}\n" 
            num += 1
        embed = discord.Embed(title = title, description = s, color=self.bot.color)
        embed.set_footer(text=self.bot.footer)
        try:
            await ctx.channel.purge(limit=1)
        except:
            pass
        msg = await ctx.send(embed=embed)
        for i in range(1, len(options) + 1): await msg.add_reaction(reactions[i])

    @commands.command()
    async def bossbadi(self, ctx):
        await ctx.reply('bossbadi is a cool dude and a great bot dev')

    @commands.group(invoke_without_command=True)
    async def todo(self, ctx):
        """Todo Commands"""
        s = await self.bot.db.fetchrow("SELECT things FROM todo WHERE id = $1", ctx.author.id)
        if s:
            try:
                p = self.bot.utils.SimpleMenu(entries=s['things'] or ['No todos'], per_page=10)
                await p.start(ctx)
            except Exception as e:
                await ctx.send(f'{e}')
        else:
            await self.bot.db.execute("INSERT INTO todo(id) VALUES ($1)", ctx.author.id)
            await ctx.send("Registered a todo list for you.")
            
    @todo.command()
    async def add(self, ctx, *, thing:str):
        '''Add something to the todo list'''
        s = await self.bot.db.fetchrow("SELECT * FROM todo WHERE id = $1", ctx.author.id)
        list = s['things']
        if s:
            if len(list) > 25:
                await ctx.send('Currently you can only have 25 todo items.')
            elif thing in list:
                await ctx.send('Thats already in your list.')
            elif len(thing) > 25:
                await ctx.send('Please shorten your task.')
            else:
                list.append(thing)
                await self.bot.db.execute("UPDATE todo SET things = $1 WHERE id = $2", list, ctx.author.id)
                await ctx.send(f'Added `{thing}` to your todo list!')

    @todo.command(aliases=['remove'])
    async def delete(self, ctx, *, thing):
        '''Delete an item from your todo list'''
        s = await self.bot.db.fetchrow("SELECT * FROM todo WHERE id = $1", ctx.author.id)
        list = s['things']
        if s:
            if thing.isdigit():
                list.pop(int(thing)-1)
            else:
                if not thing in list:
                    await ctx.send('Item not found.')
                else:
                    list.remove(thing)
            await self.bot.db.execute("UPDATE todo SET things = $1 WHERE id = $2", list, ctx.author.id)
            await ctx.send(f'Removed `{thing}` from your todo list!')

    @todo.command()
    async def clear(self, ctx):
        '''Clears your todo list'''
        s = await self.bot.db.fetchrow("SELECT * FROM todo WHERE id = $1", ctx.author.id)
        if s:
            confirm_embed = self.bot.utils.ConfirmMenu(discord.Embed(title="Are you sure you want to clear your todos?", colour=ctx.bot.color), delete_message_after=False)
            confirm = await confirm_embed.prompt(ctx)
            if confirm:
                await self.bot.db.execute("DELETE FROM todo WHERE id = $1", ctx.author.id)
                await confirm_embed.message.edit(embed=discord.Embed(title="Successfully cleared your todos.", colour=self.bot.color))
            else:
                await confirm_embed.message.edit(embed=discord.Embed(title="Cancelled", colour=self.bot.color))
                                     
def setup(bot):
    bot.add_cog(misc(bot))
