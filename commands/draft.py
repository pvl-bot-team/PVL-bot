from header import *
async def draft(message, args):
  if message.server.id == '372042060913442818':
    user = getmention(message)
    if user == None:
      userid = discorduser_to_id(message.author)
    else:
      userid = discorduser_to_id(user)
    cursor.execute(draft_select_str, (userid,))
    result = cursor.fetchone()
    if result == None:
      await client.send_message(message.channel, "You are not in the draft league")
      return
    sheet = SHEET_IDS[result[0]]
    mon_col = TEAM_COLS[result[1]]
    point_col = POINT_COLS[result[1]]

    rosterpage = service.spreadsheets().values().get(spreadsheetId=sheet, range='Rosters', majorDimension='COLUMNS').execute()
    values = rosterpage.get('values', [])
    roster = values[result[1]*3+2][:-1]
    labels = values[1][:-1]
    embed = discord.Embed(title="Draft Info", color=discord.Color(0x85bff8))
    for s in zip(labels, roster):
      if s[0] != '' and s[1] != '':
        embed.add_field(name=s[0], value=s[1])
    await client.send_message(message.channel, embed=embed)
    return
