import os
import discord
from discord.ext import commands
import requests
import json



my_secret = os.environ['botcode']
client = discord.Client()

def get_quoute():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return quote

#def get_time():
#  response = requests.get("http://worldclockapi.com/api/json/est/now")
#  json_data = json.loads(response.text)
#  t = json_data['0']['currentDateTime']
#  return t




@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_member_join(member):
  with open('users.json', 'r') as f:
    users = json.load(f)

  await update_data(users, member)
    

  with open('users.json', 'w') as f:
    json.dump(users, f)


  
@client.event
async def on_message(mesg):

  if mesg.author == client.user:
    return
  
  if mesg.content.startswith('s\'hello'):
    await mesg.channel.send('Hello')

  if mesg.content.startswith('s\'q'):
    q = get_quoute()
    await mesg.channel.send(q)
  
  

  #Json File


  with open('users.json', 'r') as f:
    users = json.load(f)

  await update_data(users, mesg.author)
  await add_experience(users, mesg.author, 1)
  await level_up(users, mesg.author, mesg.channel)
    

  with open('users.json', 'w') as f:
    json.dump(users, f)

 
async def update_data(users, user):
  if not user.id in users:
    users[user.id] = {} 
    users[user.id]['experience'] = 0
    users[user.id]['level'] = 1


async def add_experience(users, user, exp):
  users[user.id]['experience'] += exp

async def level_up(users, user, channel):
  experience = users[user.id]['experience']
  level_start = users[user.id]['level']
  level_end = int(experience) ** (1/4)

  if level_start < level_end:
    await client.send_message(channel, '{} has leveled up to level {}'.format(user.mention, level_end))
    user[user.id]['level'] = level_end



client.run(my_secret)

  