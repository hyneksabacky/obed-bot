import os
import discord
import random
import json
#from keep_alive import keep_alive

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


client = discord.Client()
url = "https://obed.cucin.eu/fit/?json"
menu = []


@client.event
async def on_ready():
    global menu
    print('Logged in as {0.user}'.format(client))
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(2)
    #print(driver.page_source)
    content = driver.find_element_by_tag_name('pre').text
    menu = json.loads(content)
    print("done\n")
    #print(menu.items())
    #print(menu["restaurants"]["bistro-53"])
    


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content == '!cus':
    await message.channel.send('{0.author.name} je tupec'.format(message))

  if message.content.endswith('?'):
    if random.randint(0, 1) == 0:
      await message.add_reaction('👍')
    else:
      await message.add_reaction('👎')

  if message.content == '!obed':
    global menu
    restr = ""
    for restaurace, dishes in menu.items():
      #restaurace = restaurace[:-1]
      if restaurace.startswith("restaurants"):
        for jidla in dishes:
          restr = restr + "------------------\n| **" + dishes[jidla]["title"] + "**\n------------------\n"
          for primo in dishes[jidla]["dishes"]:
            restr = restr + " > " + primo["number"]+ "   " + primo["name"] + "\n    " + primo["price"] + "\n"
          restr = restr+""
          await message.channel.send(restr)
          restr = ""
          
client.run('ODU5NzA5ODA0MDcwOTYxMTYy.YNwpJQ.e-XsxzKfvUe7_GbTcSH8YlixAw8')
