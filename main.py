import os
import discord
import requests
import json
import random
from replit import db
from keepAlive import keep_alive


client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
  "Cheer Up!",
  "Hang in there!",
  "You are a great person <3"
  "Just don't kill yourself"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements

@client.event
async def on_ready():
  #init
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  #if the message is the user (bot)
  if message.author == client.user: 
    return

  msg = message.content

  if message.content.startswith('$hello'):
    await message.channel.send('Hello Vincent, my Master.')
  
  if message.content.startswith ('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"] == True:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added. Thank you!")
  
  if msg.startswith ("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragements(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
    
  if msg.startswith("$list2"):
    encouragements = []
    if "responding" in db.keys():
      encouragements = db["responding"]
    await message.channel.send(encouragements)
  
  if msg.startswith("$responding"):
    value = msg.split("responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")


keep_alive()
client.run(os.environ['TOKEN'])
