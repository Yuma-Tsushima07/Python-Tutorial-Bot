import discord
from discord.ext import commands
import random
import json

def get_prefix(client,message):
    with open('prefixes.json','r') as f:
        prefixs = json.load(f)

    return prefixs[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix) # bot prefix

@client.event
async def on_ready():
    print("Bot is online") # check if the bot is online 

@client.event
async def on_guild_join(guild): # prefix json set up
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '^'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.command(aliases=['pg']) # ping command 
async def ping(ctx):
    await ctx.send('Pong!')

@client.command(aliases=['prefix']) # prefix change command
async def setprefix(ctx, prefixset= None):
    if(not ctx.author.guild_permissions.manage_channels):
        await ctx.send('This command requires `Manage Channels` permissions!')
        return

    if(prefixset == None):
        prefixset = '^'

    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefixset

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
        await ctx.send(f'The bot prefix has been changed to `{prefixset}`')



@client.command(aliases=['8b','8ball']) # 8ball command 
async def eightball(ctx, *, question):
    responses = [
            'Hell no.',
        'Prolly not.',
        'Idk bro.',
        'Prolly.',
        'Hell yeah my dude.',
        'It is certain.',
        'It is decidedly so.',
        'Without a Doubt.',
        'Yes - Definately.',
        'You may rely on it.',
        'As i see it, Yes.',
        'Most Likely.',
        'Outlook Good.',
        'Yes!',
        'No!',
        'Signs a point to Yes!',
        'Reply Hazy, Try again.',
        'Better not tell you know.',
        'Cannot predict now.',
        'Concentrate and ask again.',
        "Don't Count on it.",
        'My reply is No.',
        'My sources say No.',
        'Outlook not so good.',
        'Very Doubtful']
    await ctx.send(f'Question: {question}\n 8ball: Answer {random.choice(responses)}')




@client.command()
async def kick(ctx, member:discord.Member, *, reason=None): # kick command
    if(not ctx.author.guild_permissions.kick_members):
        await ctx.send('This command requires `Kick Members` permissions!')
        return 
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked from the server!')



@client.command()
async def ban(ctx, member:discord.Member, *, reason=None): # ban command
    if(not ctx.author.guild_permissions.ban_members):
        await ctx.send('This command requires `Ban Members` permissions!')
        return 
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned from the server!')



@client.command() 
async def unban(ctx, *, member): #unban command
    if(not ctx.author.guild_permissions.ban_members):
        await ctx.send('This command requires `Ban Members` permissions!')
        return 
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


@client.command(aliases=['purge'])
async def clear(ctx,amount=11): # purge command
    if(not ctx.author.guild_permissions.manage_messages):
        await ctx.send('This command requires `Manage Messages` permissions!')
        return
    ammount = amount+1
    if amount > 101:
        await ctx.send('Can not delete more than 100 messages at a time!')
    else:
        await ctx.channel.purge(limit=amount)
        await ctx.send('Cleared messages in this channel')

@client.command()
async def mute(ctx, member : discord.Member, *, reason=None):
    if(not ctx.author.guild_permissions.manage_messages):
        await ctx.send('This command requires `Manage Messages` permissions!')
        return
        
    guild = ctx.guild
    muteRole = discord.utils.get(guild.roles, name="Muted")

    if not muteRole:
        await ctx.send('The `Muted` role has not been created, make one yourself please!')
        muteRole = await guild.create_role(name='Muted')

    for channel in guild.channels:
        await channel.set_permissions(muteRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)
        await member.add_roles(muteRole,reason=reason)
        await member.send(f"You have been muted from `{guild.name}` | Reason: `{reason}` ")
        await ctx.send('User has been muted')


client.run('TOKEN')