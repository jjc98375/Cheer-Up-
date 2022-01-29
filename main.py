import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


client = discord.Client()

starter_sadwords = ["ㅠㅠ"]
starter_encouragements = ["할수있어!"]

if "responding" not in db.keys():
  db["responding"] = True


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def update_sad(sad_words):
  if "sad" in db.keys():
    sad = db["sad"]
    sad.append(sad_words)
    db["sad"] = sad
  else:
    db["sad"] = [sad_words]



def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

def delete_sad(index):
  sad = db["sad"]
  if len(sad) > index:
    del sad[index]
    db["sad"] = sad


def clear_encouragement():
  db["encouragements"].clear()

def clear_sad():
  db["sad"].clear()




@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  msg = msg.lower()
  # print(msg)

  if msg.startswith('$help'):
    # file = open("help.txt")
    # for line in file:
    #   await message.channel.send(line)
    file = open("help.txt")
    await message.channel.send(file.read())

  if msg.startswith('$hello'):
    await message.channel.send("안녕!")

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    full_enc = starter_encouragements
    if "encouragements" in db.keys():
      full_enc =  full_enc + list(db["encouragements"])
    
    full_sad = starter_sadwords
    if "sad" in db.keys():
      full_sad = full_sad + list(db["sad"])

    if any(word in msg for word in full_sad) and ("$" not in msg):
      await message.channel.send(random.choice(full_enc))

  if msg.startswith('$add_enc'):
    encouraging_message = msg.split("$add_enc ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith('$add_sad'):
    sad_message = msg.split("$add_sad ", 1)[1]
    # if sad_message == "sad":
    #   await message.channel.send("The word 'sad' can't be added due to the duplication of command keys")
    # else:
    update_sad(sad_message)
    await message.channel.send("New sad word added.")

  if msg.startswith("$del_enc"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del_enc", 1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(list(encouragements))

  if msg.startswith("$del_sad"):
    sad = []
    if "sad" in db.keys():
      index = int(msg.split("$del_sad", 1)[1])
      delete_sad(index)
      sad = db["sad"]
    await message.channel.send(list(sad))

  if msg.startswith("$list_enc"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(list(encouragements))

  if msg.startswith("$list_sad"):
    sad = []
    if "sad" in db.keys():
      sad = db["sad"]
    await message.channel.send(list(sad))

  if msg.startswith("$clear_enc"):
    clear_encouragement()
    await message.channel.send("Encouraging messages has been cleared")
  
  if msg.startswith("$clear_sad"):
    clear_sad()
    await message.channel.send("Sad words has been cleared")
  
  

  
  if msg.startswith("$responding"):
    value = msg.split("responding ", 1)[1]
    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")


keep_alive()
client.run(os.getenv("TOKEN"))