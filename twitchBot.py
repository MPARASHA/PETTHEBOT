import threading
from irc.bot import SingleServerIRCBot
import time
import json
import random
import os

NAME = "PETTHEBOT" # Bot Account Name
OWNERS = os.environ['CHANNEL_LIST'].split(" ") # Channels on which to deploy the bot

# Command Prefixes
PREFIX = "!"
PREFIX2 = "%"

# CREDIT: https://stackoverflow.com/a/52942600/17844690
def randomcase(s):
	result = ''
	for c in s:
		case = random.randint(0, 1)
		if case == 0:
			result += c.upper()
		else:
			result += c.lower()
	return result



class Bot(SingleServerIRCBot):
	def __init__(self, OWNER):
		self.HOST = "irc.chat.twitch.tv"
		self.PORT = 6667
		self.USERNAME = NAME.lower()
		self.CLIENT_ID = os.getenv('C_ID') # Client ID for bot account
		self.TOKEN = os.getenv('TOKEN') # OAuth Token for bot account
		self.CHANNEL= f"#{OWNER}"

		super().__init__([(self.HOST, self.PORT, f"oauth:{self.TOKEN}")], self.USERNAME, self.USERNAME)

	def process(self, user, message):

		try:
			if message.startswith(PREFIX):
				cmd = message.split(" ")[0][len(PREFIX):]
				args = message.split(" ")[1:]
				self.perform(user, cmd, args)

				return

		except:
			if message.startswith(PREFIX):
				cmd = message.split(" ")[0][len(PREFIX):]
				self.perform(user, cmd)

				return


		if message.startswith(PREFIX2):
			if len(message.split(" ")) > 1:
				num = random.randint(0,100)
				self.send_message(str(num) + "% " + user['name'])

			return

		num = random.randint(0,100)

		if user["name"].lower() == "filomaj":
			
			if(num > 97):
				self.send_message("Loser " + randomcase(message))
			elif(num < 3):
				self.send_message("@" + user['name'] + " modCheck who asked?")
		else:
			
			if(num > 97):
				self.send_message("@" + user['name'] + " modCheck who asked?")
			elif(num < 3):
				self.send_message(randomcase(message))

		if(num>=3 and num<6):
			with open('insults.txt') as f:
				lines = f.read().splitlines()
				myline =random.choice(lines)
				self.send_message("@" + user['name'] + " " + myline)


	def perform(self, user, cmd, args = None):
		if cmd == "love" and args is not None:
			num = random.randint(0,100)
			message = f"There is {num}% love between {user['name']} and {args[0]}"
			self.send_message(message)

		if cmd == "joke":
			with open('reddit_jokes_filtered.json') as fp:
				data = json.load(fp)
				random_index = random.randint(0, len(data)-1)
				
				self.send_message(data[random_index]["title"])
				self.send_message(data[random_index]["body"])

		if cmd == "scareme":
			with open('twosentencehorror_filtered.json') as fp:
				data = json.load(fp)
				random_index = random.randint(0, len(data)-1)
				
				self.send_message(data[random_index]["title"])
				self.send_message(data[random_index]["body"])

	def on_welcome(self, cxn, event):
		for req in ("membership", "tags", "commands"):
			cxn.cap("REQ", f":twitch.tv/{req}")

		cxn.join(self.CHANNEL)
		self.send_message("yo MrDestructoid")

	def on_pubmsg(self, cxn, event):
		tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
		user = {"name": tags["display-name"], "id": tags["user-id"]}
		message = event.arguments[0]

		if user["name"] != NAME:
			self.process(user, message)

	def send_message(self, message):
		self.connection.privmsg(self.CHANNEL, message)
		time.sleep(5)


class MyBotThread(threading.Thread) :
	def __init__(self, channel):
		self.channel = channel
		super(MyBotThread, self).__init__()

	def run(self):
		bot = Bot(self.channel)
		bot.start()

if __name__ == "__main__":

	for channel in OWNERS:
		thread = MyBotThread(channel=channel)
		thread.start()
		print("Thread started for channel:" , channel)



