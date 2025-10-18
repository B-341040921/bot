import asyncio
import requests
import json
import discord
import discord.ext
import os
from logging import exception
from discord.ext import commands
from discord import app_commands
from web_server import keep_alive

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')
  await tree.sync()
  await client.change_presence(status=discord.Status.online)

@tree.command(name="check_user", description="checks if user is on the list")
async def check_user(interaction: discord.Interaction, user: str)
  if str(interaction.user) in auth:
    if user.lower() in user_list:
        await interaction.response.send_message(f"user {user} is in list")
    else:
        await interaction.response.send_message(f"user {user} not in list")
  else:
      await interaction.response.send_message("not authorized")

@client.event
async def on_message(message):
  global channel
  if message.author == client.user:
    return

  if client.user.mentioned_in(message):
    if str(message.author.name) in auth:
      try:
        response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
          "Authorization": "Bearer "+os.environ.get("API"),
          "Content-Type": "application/json",
         },
         data=json.dumps({
         "preset": "@preset/wide-agent",
         "model": "meta-llama/llama-3.2-3b-instruct:free",
         "messages": [
             {
              "role": str(interaction.user),
              "content": text
               }
          ],

        })
       )
        response_json = response.json()
        channel = client.get_channel(message.channel.id)
        if "choices" in response_json and len(response_json["choices"]) > 0 and "message" in response_json["choices"][0] and "content" in response_json["choices"][0]["message"]:
          await channel.response.send_message(response_json["choices"][0]["message"]["content"])
        else:
          await channel.response.send_message("Could not get a valid response from the API.")
      except:
        await channel.response.send_message("API on cooldown")
    else:
      await channel.response.send_message("not authorized")

auth=["pvz_watermelus100","watermelon.11.","prime_minister_of_egg","sesruirnuien","lgcool2"]
user_list=["budo_1","saket","jotan_0200","elenorsilly","zepz","1yme"]
keep_alive()
client.run(os.environ.get("TOKEN"))
