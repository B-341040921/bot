import asyncio
import requests
import json
import discord
from logging import exception
from discord.ext import commands
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
async def check_user(interaction: discord.Interaction, user: str):
  if str(interaction.user) in auth:
    if user.lower() in user_list:
        await interaction.response.send_message(f"user {user} is in list")
    else:
        await interaction.response.send_message(f"user {user} not in list")
  else:
      await interaction.response.send_message("not authorized")

@tree.command(name="prompt", description="use melon AI (beta)")
async def prompt(interaction: discord.Interaction, text: str, debug: bool=False):
  if str(interaction.user) in auth:
    try:
      response = requests.post(
      url="https://openrouter.ai/api/v1/chat/completions",
      headers={
        "Authorization": "Bearer "+os.environ.get(API),
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
      if debug:
        await interaction.response.send_message("[NEUTRAL]",response)
        await interaction.response.send_message("[TEXT]",response.text)
      else:
        response_json = response.json()
        if "choices" in response_json and len(response_json["choices"]) > 0 and "message" in response_json["choices"][0] and "content" in response_json["choices"][0]["message"]:
          await interaction.response.send_message(response_json["choices"][0]["message"]["content"])
        else:
          await interaction.response.send_message("Could not get a valid response from the API.")
    except:
       await interaction.response.send_message("API on cooldown")
  else:
    await interaction.response.send_message("not authorized")

@client.event
async def on_message(message):
  if message.author == client.user:
    return

    if message.content.lower() in keywords:
      await message.channel.send('<@&1422797659026231347> Alert: possible raid, report sent to DirWIDE and DirINT')
      member =  client.get_user(936848029179326474)
      await member.send(f"{message.author} sent {message.content}")
      await message.delete()


keywords=[os.environ.get(KEYWORDS)]
auth=[os.environ.get(AUTH)]
user_list=["budo_1","saket","jotan_0200","elenorsilly","zepz","1yme"]
keep_alive()
client.run(os.environ.get("TOKEN"))
