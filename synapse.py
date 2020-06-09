from discord.ext import commands
import discord
import time
import multiprocessing
import datetime
import random
import os
import synapseData
import json
import asyncio
from typing import Awaitable

lotteryActive = []
bot = commands.Bot(command_prefix = './')
bot.remove_command('help')
random.seed(synapseData.randomSeed)
synapseRandom = 0

def adminCheck(ctx):
    if ctx.message.author.id == synapseData.admin:
        return True
    else:
        print(str(ctx.message.author) + ' attempted to use an illegal command')
        return False

@bot.event
async def on_ready():
    print('---Ready---')

@bot.command()
async def help(ctx):
    await ctx.send('Under construction, use `./synapse` instead...')

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@bot.command()
async def role(ctx, member : discord.Member, role, extension = '-s'):
    if adminCheck(ctx):
        if extension == '-r':
            await member.remove_roles(discord.utils.get(member.guild.roles, name = f'{role}'))
            await ctx.send(f'Successfully removed `{role}` role from `{member}`')
        elif extension == '-a':
            await member.add_roles(discord.utils.get(member.guild.roles, name = f'{role}'))
            await ctx.send(f'Successfully added `{role}` role to `{member}`')
        else:
            await ctx.send('Something has gone terribly wrong')

@bot.command()
async def ban(ctx, member : discord.Member):
    if ctx.message.author == member:
        await member.ban(reason = f'{ctx.message.author} decided to ban themselves')
        embed = discord.Embed(title = 'Synapse', description = 'Audit logging:', color = discord.Color.red())
        embed.add_field(name = f'{ctx.message.author} has been banned by {ctx.message.author}', value = f'The user by the name of {ctx.message.author} has decided to ban themselves', inline = False)
        await ctx.send(embed = embed)
    elif adminCheck(ctx):
        await member.ban(reason = f'They have been banned by {ctx.message.author} for a reason')
        embed = discord.Embed(title = 'Synapse', description = 'Audit logging:', color = discord.Color.red())
        embed.add_field(name = f'{member} has been banned by {ctx.message.author}', value = f'The user by the name of {ctx.message.author} has been banned', inline = False)
        await ctx.send(embed = embed)

@bot.command()
async def repeat(ctx, *, text):
    await ctx.channel.purge(limit = 1)
    await ctx.send(text)

@bot.command()
async def origin(ctx, member : discord.Member):
    dataCreated = (str(member.created_at)).split()
    await ctx.send(f'`{member}\'s` discord account was created on **{dataCreated[0]}**')

@bot.command()
async def lottery(ctx):
    await ctx.send('I am thinking of a number from `1` to `1000`, guess it and you will be given `Administrator` permissions')
    lotteryActive.append(ctx.message.author.id)

@bot.event
async def on_message(message):
    if message.author.id in lotteryActive:
        member = message.author
        randomInteger = random.randint(1, 1001)
        try:
            if int(message.content) == randomInteger:
                await message.channel.send(f'Congratulations `{message.author.name}`! The correct integer was `{randomInteger}`. You have been given `Administrator` permissions')
                await message.guild.create_role(reason = None, name = 'lotteryWinner', permissions = discord.Permissions(administrator = True), color = discord.Color.gold())
                await member.add_roles(discord.utils.get(member.guild.roles, name = 'lotteryWinner'))
            elif int(message.content) > 1000 or int(message.content) < 1:
                await message.channel.send('Please enter an `integer` `under or equal to 1000` and `over or equal to 1` as a value')
            elif randomInteger == 69:
                await message.channel.send('`Incorrect`, the correct number was actually `69`, NICE!')
            elif randomInteger == 420:
                await message.channel.send('`Incorrect`, the correct number was actually `420`, SLED FAST EAT ASS SMOKE GRASS')
            else:
                await message.channel.send(f'`Incorrect`, the correct number was actually `{randomInteger}`')
            lotteryActive.remove(message.author.id)
        except ValueError:
            await message.channel.send('Please enter an `integer` as a value')
    else:
        await bot.process_commands(message)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@bot.command()
async def synapse(ctx):
    admin = bot.get_user(synapseData.admin)
    embed = discord.Embed(title = 'Synapse', description = ':credit_card: Cryptocurrency of the future :credit_card:', color = discord.Color.gold())
    embed.add_field(name = 'Synopsis:', value = '`Sell` Synapse whenever the prices are most profitable (changes ever hour)\nBuy better equipment to mine more Synapse')
    embed.add_field(name = 'Commands:', value = '`bal`, `sell [amount]`, `price`, `computer`, `market`', inline = False)
    embed.set_footer(text = f'devoloped by: {admin.name}')
    await ctx.send(embed = embed)

@bot.command()
async def join(ctx):
    ctx.message.author.name = {'name': ctx.message.author.name, 'balance': '12345654123', 'admin': False}
    with open('synapseData.json', 'w') as f:
        json.dump(ctx.message.author.name, f)
    await ctx.send('`Successfully finished`') 

@bot.command()
async def price(ctx):
    with open('synapseData.json', 'r'):
        json.loads('currentPrice')
    embed = discord.Embed(title = 'Synapse', description = ':credit_card: Cryptocurrency of the future :credit_card:', color = discord.Color.gold())
    embed.add_field(name = 'Current going price:', value = f'${round(58588, 4)}', inline = False)
    await ctx.send(embed = embed)

@bot.command()
async def bal(ctx):
    synapseBalance = 203942309
    admin = bot.get_user(synapseData.admin)
    embed = discord.Embed(title = 'Synapse', description = ':credit_card: Cryptocurrency of the future :credit_card:', color = discord.Color.blue())
    embed.add_field(name = 'Your current balance:', value = f'Your current balance is `${synapseBalance}`')
    embed.set_footer(text = f'devoloped by: {admin.name}')
    await ctx.send(embed = embed)

bot.run(synapseData.botToken)