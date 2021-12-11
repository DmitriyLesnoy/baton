import discord
from discord.ext import commands

grankin_bot=['Бот','ботик','Фейнморк','Феинморк','Сраня','Граня','Сранкин']

prefix='>'

client = discord.Client()
bot = commands.Bot(command_prefix='>')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg=message.content.lower()
    msg_list=msg.split()
    print(msg_list,'-',str(message.author)+' / # '+ str(message.channel))


    if 'даун' in msg:
        await message.channel.send(f' {message.author.mention} сам ты даун')
    if len(msg_list+grankin_bot)<(len(msg_list)+len(grankin_bot)):
        await message.channel.send(f'<@{694813758328930306}> тебя зовут')
    if msg_list[0]==prefix+'help':
        await message.channel.send(open('help.txt', 'r')) 


    if msg==prefix+'addrole':
        role=msg_list[1]
        user = ctx.message.author
        role = discord.utils.get(user.server.roles, name="Test")
        await client.add_roles(user, role)

client.run('ODk2NzExNjY2MjE2MDkxNjUw.YWLF0Q.G4IJ2RRjSONyXsHf65LuP5Q0Wbw')


 