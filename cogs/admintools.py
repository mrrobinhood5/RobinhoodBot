import discord
from discord.ext import commands
from replit import db
import asyncio
import json

class DmCommands(commands.Cog, name='DM Commands'):
  '''
  Commands for the server admin to track their peeps
  '''

  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='listmembers',aliases=['lm'])
  async def listmembers(self, ctx):
    '''
    READ ALL: Lists all member.name that are NOT bots.
    '''
    allmembers = ctx.guild.members
    returnstr = ""
    for member in allmembers:
      returnstr += f"{member.name}\n" if not member.bot else ""
    await ctx.send(returnstr) 

  @commands.command(name='dbsetup',aliases=['dbs'])
  async def dbsetup(self, ctx):
    '''
    CREATE ALL: Keys in the Database with existing Members. Will not create if it exists already or if they are bots.
    '''
    allmembers = ctx.guild.members
    for member in allmembers:
      if member.id not in db.keys() and not member.bot:
        dumpstr = {member.name: {}}
        db[member.id] = json.dumps(dumpstr)
    await ctx.send("Created All Member Keys") 

  @commands.command(name='dblist',aliases=['dbl'])
  async def dblist(self, ctx, member: discord.Member=False):
    '''
    READ ALL: Lists all keys in DB created. 
    '''
    if not member:
      dbkeys = db.keys()
      returnstr = ""
      for key in dbkeys:
        amember = ctx.guild.get_member(int(key))
        returnstr += f"{amember.name}\n"
      try:
        await ctx.send(returnstr)
      except:
        await ctx.send("Empty Ass DB")
      finally:
        pass
    else:
      amember = db[int(member.id)]
      await ctx.send(amember)

  @commands.command(name='dbpurge',aliases=['dbp'])
  async def dbpurge(self, ctx):
    '''
    DELETE ALL: Delets all keys in DB crated. 
    '''
    dbkeys = db.keys()
    for key in dbkeys:
      del db[key]
    await ctx.send("All Keys Deleted. DB Purged. I hope your are happy.") 

  @commands.command(name='setPC',aliases=['spc'])
  async def set_user_pc(self, ctx, member: discord.Member, PCName):
    '''
    CREATE : adds a PC to a key
    '''
    userdata = json.loads(db[member.id])
    PCName = str("PC-"+PCName)
    userdata.update({PCName:{}})
    db[member.id] = json.dumps(userdata)
    await ctx.send(f"Added {PCName} to {member.name}") 
  
  @commands.command(name='remPC',aliases=['rpc'])
  async def rem_user_pc(self, ctx, member: discord.Member, PCName):
    '''
    DELETE : deletes a PC to a key
    '''
    userdata = json.loads(db[member.id])
    PCName = str("PC-"+PCName)
    try:
      userdata.pop(PCName)
      db[member.id] = json.dumps(userdata)
    except:
      await ctx.send("PC Does not exists for that User. Check it with `dblist`")
    await ctx.send(f"Removed {PCName} from {member.name}") 

  @commands.command(name='approve-v',aliases=['vsa'])
  async def approvev(self, ctx, member: discord.Member):
    '''
    UPDATE: vhseet
    '''
    def chk(msg):
      return msg.author.id == ctx.author.id and msg.channel.id == ctx.channel.id

    await ctx.send("What Player Character?")
    try:
      PCname = await self.bot.wait_for('message', check=chk, timeout=60)
    except asyncio.TimeoutError:
      return await ctx.send('time out')
    #adds the entry
    
    if member.id not in db.items():
      userdata = {}
      userdata.update({member.id: {}})
    else:
      userdata = json.loads(db[member.id])

    if PCname not in userdata.items():
      userdata[member.id].update({})

    await ctx.send("Approve VSHEET?")
    try:
      vsheet = await self.bot.wait_for('message', check=chk, timeout=60)
    except asyncio.TimeoutError:
      return await ctx.send('time out')    
    
    if "yes" in vsheet.content.lower():
      userdata.update({member.id: {PCname: {"vsheet":True}}})
    else:
      userdata.update({member.id: {PCname: {"vsheet":False}}})


  # adds key to db on member join
  @commands.Cog.listener('on_member_join')
  async def member_join_event(self, member):
    if not member.bot:
      db[member.id] = json.dumps("{}") 

  #removes key to db on member removal
  @commands.Cog.listener('on_member_remove')
  async def member_leave_event(self, member):
      if not member.bot:
        db.pop(member.id)

def setup(bot):
  bot.add_cog(DmCommands(bot))