import random
from discord import channel, guild, mentions, message, role, voice_client,VoiceChannel
from discord.ext import commands
from discord.ext.commands.core import command
from discord.utils import get
import discord
from discord import FFmpegPCMAudio

intents = discord.Intents.all()
client = commands.Bot(command_prefix='>', intents=intents)


White_list={1025342413620908104:[657906035675365387]}
Black_list={}


queues_local = {}
	
def check_queue_local(ctx, id):
    if queues_local[id] != []:
        voice = ctx.guild.voice_client
        source = queues_local[id].pop(0)
        player = voice.play(source)

def str2bool(string):
    if string.lower()=='true':
        return True
    elif string.lower()=='false':
        return False


@client.event
async def on_ready():
    print('Бот {0.user} был авторизирован'.format(client))

@client.command(pass_context = True)
async def info(ctx):
    i=open('help.txt')
    p=i.read()
    await ctx.send(p)

@client.command(pass_context = True)
async def add(ctx, role: discord.Role, user: guild.Member):
    text=['Add:',
         "    -server: "+ctx.message.guild.name,
         "    -author: "+ctx.message.author.name,
         "    -args: "+role.name+" "+user.name]
    author=ctx.message.author
    guild=ctx.guild
    if author.id in Black_list[guild.id] and not author.id in Black_list[guild.id]:
        await ctx.message.add_reaction('⛔')
        text[0]=" Add: member in black list"
    else:
        await user.add_roles(role)
        text[0]=" Add: adding success"
        await ctx.message.add_reaction('✅')
    print("\n".join(text))

@client.command(pass_context = True)
async def remove(ctx, role: discord.Role, user: guild.Member):
    error=''
    text=['Remove:',
         "    -server: "+ctx.message.guild.name,
         "    -author: "+ctx.message.author.name,
         "    -args: "+role.name+" "+user.name,
         "    -error: "+error]
    author=ctx.message.author
    guild=ctx.guild
    if author.id in Black_list[guild.id] and not author.id in Black_list[guild.id]:
        await ctx.message.add_reaction('⛔')
        error="Member in black list"
        await ctx.message.reply(error)
    else:
        await user.remove_roles(role)
        await ctx.message.add_reaction('✅')
    text[4]="    -error: "+error
    print("\n".join(text))
   
@client.command(pass_context = True)
async def create(ctx, name_:str, r:int,g:int,b:int, func1=None, arg1=None, func2=None, arg2=None, reason=None):
    author=ctx.message.author
    guild = ctx.guild
    if author.id in Black_list[guild.id] and not author.id in Black_list[guild.id]:
        await ctx.message.add_reaction('⛔')
        return
    
    if r is None and g is None and b is None:
        r,g,b=130, 130, 130   
    mentionable=True
    hoist=False
    reason_=''
    error=''

    if arg1 is not None and arg1!='True' and arg1!='False':
        error='wrong argument '+str(arg1)
    if arg2 is not None and (arg2!='True' and arg2!='False'):
        error='wrong argument '+str(arg2)
        
    if func1 is not None:
        if func1.lower()=='mentionable':
            mentionable=str2bool(arg1)
        elif func1.lower()=='hoist':
            hoist=str2bool(arg1)
        else:
            error='wrong argument name '+str(func1)
    else:
        func1,arg1='',''
    if func2 is not None:
        if func2.lower()=='mentionable':
            mentionable=str2bool(arg2)
        elif func2.lower()=='hoist':
            hoist=str2bool(arg2)
        else:
            error='wrong argument name '+str(func2)
    else:
        func2,arg2='',''

    if reason is not None:
        reason_=reason
    if error=='':
        await guild.create_role(name=name_, colour=discord.Colour.from_rgb(int(r),int(g),int(b)), hoist=hoist, mentionable=mentionable, reason=reason_)
        await ctx.message.add_reaction('✅')
    else:
        await ctx.message.reply(error)
        await ctx.message.add_reaction('⛔')
    text=['Create:',
         "    -guild: "+ctx.message.guild.name,
         "    -author: "+ctx.message.author.name,
         "    -abs args: "+name_+" "+str(r)+" "+str(g)+" "+str(b),
         "    -add args: "+func1+" "+arg1+" "+func2+" "+arg2,
         "    -reason: "+reason_,
         "    -error: "+error]
    print("\n".join(text))

@client.command(pass_context=True)
async def edit(ctx, role:discord.Role, function=None, arg1= None, arg2=None, arg3=''):
    author=ctx.message.author
    guild = ctx.guild
    if author.id in Black_list[guild.id] and not author.id in Black_list[guild.id]:
        await ctx.message.add_reaction('⛔')
        return
    error=''
     

    if function is not None and function.lower()=='position':
        if arg1 is not None and arg1.lower()=='up' and arg2 is not None:
            pos=int(arg2)
            pos_=role.position+pos
            member= guild.get_member(896711666216091650)
            bot_m=member.top_role
            if pos_>=bot_m.position:
                error='Missing permissions to mevo role up'
            else:
                await role.edit(position=pos_)
                await ctx.message.add_reaction('✅')
        elif arg1 is not None and arg1.lower()=='down' and arg2 is not None:
            pos=int(arg2)
            pos_=role.position-pos
            if pos_<=0:
                error='Can`t move role down'
            else:
                await role.edit(position=pos_)
                await ctx.message.add_reaction('✅')
        elif arg1 is not None and arg1.lower()=='max':
            baton=guild.get_member(896711666216091650)
            m_pos=baton.top_role.position
            await role.edit(position=m_pos-1)
            await ctx.message.add_reaction('✅')
        elif arg1 is not None and arg1.lower()=='min':
            await role.edit(position=1)
            await ctx.message.add_reaction('✅')
        else:
            error='Wrong argument'


    elif function is not None and function.lower()=='color':
        if arg1 is not None and arg2 is not None and arg3 is not None:
            await role.edit(colour=discord.Colour.from_rgb(int(arg1),int(arg2),int(arg3)))
            await ctx.message.add_reaction('✅')
        else:
            error='Wrong argument '
    elif function is not None and function.lower()=='hoist':
        if arg1 is not None:
            await role.edit(hoist=str2bool(arg1))
            await ctx.message.add_reaction('✅')
        else:
            error='Wrong argument'
    elif function is not None and function.lower()=='mentionable':
        if arg1 is not None:
            await role.edit(mentionable=str2bool(arg1))
            await ctx.message.add_reaction('✅')
        else:
            error='Wrong argument'
    elif function is not None and function.lower()=='name':
        if arg1 is not None:
            await role.edit(name=arg1)
            await ctx.message.add_reaction('✅')
        else:
            error='Wrong argument'
    else:
        error='Wrong function name: '+function
    if error!='':
        await ctx.message.reply(error)
        await ctx.message.add_reaction('⛔')

    if arg3 is None:
        arg3=''
    if arg2 is None:
        arg2=''
    text=['edit:',
         "    -function: "+function,
         "    -guild: "+ctx.message.guild.name,
         "    -author: "+ctx.message.author.name,
         "    -args: "+role.name+' '+arg1+' '+arg2+' '+arg3,
         "    -error: "+error]

    text[5]="    -error: "+error
    print("\n".join(text))

@client.command(pass_context = True)
async def delete(ctx, role: discord.Role):
    author=ctx.message.author
    guild = ctx.guild
    if author.id in Black_list[guild.id] and not author.id in Black_list[guild.id]:
        await ctx.message.add_reaction('⛔')
        return
    text=['Delete:',
         "    -server: "+ctx.message.guild.name,
         "    -author: "+ctx.message.author.name,
         "    -args: "+role.name]
    await role.delete()
    await ctx.message.add_reaction('✅')
    print("\n".join(text))


#------------- ADMIN --------------        

@client.command(pass_context = True)
async def white(ctx, a="list", func = None, member: guild.Member = None):
    if a!="list": return
    guild=ctx.guild.id
    author=ctx.message.author.id
    admin=ctx.message.author.guild_permissions.administrator
    if func is not None and member is not None:
        if not guild in White_list.keys() and admin:
           White_list[guild]=[author]
        print(White_list)
        if admin or author in White_list[guild]:
                if func=="add":
                    White_list[guild].append(member.id)
                elif func=="remove":
                    White_list[guild].remove(member.id)
                await ctx.message.add_reaction('✅')
                print(White_list)
        else:
            await ctx.message.add_reaction('⛔')
    else:
        await ctx.send("White list: "+ str(White_list[guild]))

async def Black(ctx, a="list", func = None, member: guild.Member = None):
    if a!="list": return
    guild=ctx.guild.id
    author=ctx.message.author.id
    admin=ctx.message.author.guild_permissions.administrator
    if func is not None and member is not None:
        if not guild in Black_list.keys() and admin:
           Black_list[guild]=[author]
        print(Black_list)
        if admin or author in Black_list[guild]:
                if func=="add":
                    Black_list[guild].append(member.id)
                elif func=="remove":
                    Black_list[guild].remove(member.id)
                await ctx.message.add_reaction('✅')
                print(Black_list)
        else:
            await ctx.message.add_reaction('⛔')
    else:
        await ctx.send("Black list: "+ str(Black_list[guild]))

@client.command(pass_context = True)
async def off(ctx):
    if ctx.message.author.id in White_list:
        await ctx.message.add_reaction('🫡')
        exit()

@client.command(pass_context = True)
async def rand(ctx,one,two):
    number=random.randint(int(one),int(two))
    await ctx.send(f"Я выбираю число.....  "+str(number))

#------------- MUSIC --------------

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.message.add_reaction('✅')
    else:
        await ctx.message.add_reaction('⛔')

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.author.voice):
        await ctx.guild.voice_client.disconnect()
        await ctx.message.add_reaction('✅')
    else:
        await ctx.message.add_reaction('⛔')

@client.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.message.add_reaction('⏸️')
    else:
        await ctx.message.add_reaction('⏸️')

@client.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.message.add_reaction('▶️')

    else:
        await ctx.message.add_reaction('▶️')

@client.command(pass_context = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()
    await ctx.message.add_reaction('⏹️')

@client.command(pass_context = True)
async def play_local(ctx, arg):

    channel = ctx.author.voice.channel
    await ctx.message.add_reaction('✅')

    voice=ctx.guild.voice_client
    source = FFmpegPCMAudio(arg+'.mp3')
    player = voice.play(source, after=lambda x=None: check_queue_local(ctx, ctx.message.guild.id))
    await ctx.message.add_reaction('👍')

@client.command(pass_context = True)
async def queue_local(ctx, arg):
    voice=ctx.guild.voice_client
    song = arg+'.mp3'
    source = FFmpegPCMAudio(song)

    guild_id = ctx.message.guild.id
    if guild_id in queues_local:
        queues_local[guild_id].append(source)
    else:
        queues_local[guild_id] = [source]
    await ctx.message.add_reaction('➕')

@client.command(pass_context = True)
async def skip_local(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()
    await ctx.message.add_reaction('⏭️')
    voice = ctx.guild.voice_client

    source = queues_local[id].pop(0)
    player = voice.play(source, after=lambda x=None: check_queue_local(ctx, ctx.message.guild.id))

@client.command(pass_context = True)
async def RickRoll(ctx):
    if (ctx.author.voice):
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.message.add_reaction('⛔')
    voice=ctx.guild.voice_client
    source = FFmpegPCMAudio('RickRoll.mp3')
    player = voice.play(source)
    await ctx.message.add_reaction('✅')


client.run(open("token.txt","r").read())