from irc.bot import SingleServerIRCBot
import time
import json
import random
import os

NAME = "PETTHEBOT" # Bot Account Name
OWNER = "filomaj" # Channel on which to deploy the bot

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

def process(bot, user, message):

	try:
		if message.startswith(PREFIX):
			cmd = message.split(" ")[0][len(PREFIX):]
			args = message.split(" ")[1:]
			perform(bot, user, cmd, args)

	except:
		if message.startswith(PREFIX):
			cmd = message.split(" ")[0][len(PREFIX):]
			perform(bot, user, cmd)


	if message.startswith(PREFIX2):
		if len(message.split(" ")) > 1:
			num = random.randint(0,100)
			bot.send_message(str(num) + "% " + user['name'])

	if user["name"].lower() == "filomaj":
		num = random.randint(0,100)
		if(num > 95):
			bot.send_message("Loser " + randomcase(message))
		elif(num < 5):
			bot.send_message("@" + user['name'] + " modCheck who asked?")
	else:
		num = random.randint(0,100)
		if(num > 95):
			bot.send_message("@" + user['name'] + " modCheck who asked?")
		elif(num < 5):
			bot.send_message(randomcase(message))

		


def perform(bot, user, cmd, args = None):
	if cmd == "love" and args is not None:
		num = random.randint(0,100)
		message = f"There is {num}% love between {user['name']} and {args[0]}"
		bot.send_message(message)

	if cmd == "joke":
		with open('reddit_jokes_filtered.json') as fp:
			data = json.load(fp)
			random_index = random.randint(0, len(data)-1)
			
			bot.send_message(data[random_index]["title"])
			bot.send_message(data[random_index]["body"])
				
			


class Bot(SingleServerIRCBot):
	def __init__(self):
		self.HOST = "irc.chat.twitch.tv"
		self.PORT = 6667
		self.USERNAME = NAME.lower()
		self.CLIENT_ID = os.getenv('C_ID') # Client ID for bot account
		self.TOKEN = os.getenv('TOKEN') # OAuth Token for bot account
		self.CHANNEL = f"#{OWNER}"

		super().__init__([(self.HOST, self.PORT, f"oauth:{self.TOKEN}")], self.USERNAME, self.USERNAME)

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
			process(bot, user, message)

	def send_message(self, message):
		self.connection.privmsg(self.CHANNEL, message)
		time.sleep(5)


if __name__ == "__main__":
	bot = Bot()
	bot.start()

