from discord import guild, mentions, message, role
from discord.ext import commands
from discord.ext.commands.core import command
from discord.utils import get
import discord

client = commands.Bot(command_prefix='>',help_command=None)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def addrole(ctx, role: discord.Role, user: guild.Member):
    await user.add_roles(role)
    await ctx.send(f" Роль {role.mention} выдана {user.mention} ")

@client.command()
async def remove(ctx, role: discord.Role, user: guild.Member):
    await user.remove_roles(role)
    await ctx.send(f" Роль {role.mention} убрана  {user.mention} ")
 
# @client.command()
# async def create(ctx,*,rolename):
#     guild=ctx.guild
#     await guild.create_role(name=rolename)
#     await ctx.send(f"Роль {role.mention} успешно создана")

client.run('ODk2NzExNjY2MjE2MDkxNjUw.YWLF0Q.G4IJ2RRjSONyXsHf65LuP5Q0Wbw')