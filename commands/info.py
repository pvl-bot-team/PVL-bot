from header import *
async def info(message, args):
  user = getmention(message)
  if user == None:
    if len(args) == 0:
      userid = discorduser_to_id(message.author)
    else:
      cursor.execute(reddit_select_name_str, (args.lower(),))
      result = cursor.fetchone()
      if result == None or result[0] == None:
        await client.send_message(message.channel, 'There is no one on this server with the reddit username ' + args)
        return
      else:
        userid = result[0]
  else:
    userid = discorduser_to_id(user)
    
  cursor.execute(info_dump_str, (userid,))
  result = cursor.fetchone()
  embed = discord.Embed(title="User Info", color=discord.Color(0x85bff8))
  user = id_to_discorduser(userid) #I think this part might work but its inefficent I think, then again I didn't actually read any of your custom functions so I don't know...
  name = discorduser_to_discordname(user)
  embed.add_field(name='Discord Name', value=name)  
  if result != None:
    if result[1] != None:
      embed.add_field(name='Friend Code', value=result[1])
    if result[2] != None:
      embed.set_thumbnail(url=result[2])
    if result[3] != None:
      embed.add_field(name='Reddit Username', value=result[3])
    if result[4] != None:
      embed.add_field(name='Swear Jar Triggers', value=result[4])
    else:
      embed.add_field(name='Swear Jar Triggers', value=0)
    if result[5] != None:
      embed.add_field(name='PVL Coins', value=result[5])
    else:
      embed.add_field(name='PVL Coins', value=0)
    cursor.execute(tsv_select_str, (userid,))
    result = cursor.fetchall()
    if result != None and len(result) > 0:
      for pair in result:
        embed.add_field(name='TSV: '+pair[0], value=pair[1])
  await client.send_message(message.channel, embed=embed)
