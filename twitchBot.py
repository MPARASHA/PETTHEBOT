import threading
from irc.bot import SingleServerIRCBot
import time
import json
import random
import os
import time
import datetime as dt
import schedule


NAME = "pepe_the_toad" # Bot Account Name
OWNERS = os.environ['CHANNEL_LIST'].split(" ") # Channels on which to deploy the bot

# Command Prefixes
PREFIX = "!"
PREFIX2 = "%"
TZ_UTC = dt.timezone.utc 

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
		self.MAX_MESSAGES = 5

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
			message = f"There is {num}% <3 between {user['name']} and {args[0]}"
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

		if self.USERNAME in self.CHANNEL.lower():
			self.send_message("GotEEM")

		elif "pewdiepie" not in self.CHANNEL and "mizkif" not in self.CHANNEL:
			self.send_message("yo MrDestructoid")
			

	def on_pubmsg(self, cxn, event):
		tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
		user = {"name": tags["display-name"], "id": tags["user-id"]}
		message = event.arguments[0]

		if user["name"] != NAME and "pewdiepie" not in self.CHANNEL and "mizkif" not in self.CHANNEL:
			self.process(user, message)
		if "mizkif" in self.CHANNEL and (message.lower().startswith("im ") or message.lower().startswith("i am ") or message.lower().startswith("i'm ")):
			print(f'@{user["name"]} Hi {message[len(message.lower().split("m",1)[0]) + 2:]}')
			self.send_message(f'@{user["name"]} Hi {message[len(message.lower().split("m",1)[0]) + 2:]}')
			

	def send_message(self, message, timeS = 2):
		self.MAX_MESSAGES = self.MAX_MESSAGES - 1 
		if self.MAX_MESSAGES == 0:
			time.sleep(300)
			self.MAX_MESSAGES = 5
		else:	
			self.connection.privmsg(self.CHANNEL, message)
			time.sleep(timeS)

	def job(self):
		pewTimeS = int(os.getenv('TIMEVAR'))
		self.send_message("/me TriHard ait8k a1hl acoffeer anonymous_nobody_ antimattertape bluepigman5000 dnaflamingo dubstyler6 duskdarker edomer eml64 equinks gtchimp__7 hierotitan_____ ilikewatermelon44 in_uranus infinitegachi joinky_ kuharri doctordankus pepeflat powee2147 progamer42 robinhood187 simon36 straizotv tetyys triplehaitch caverona hunchbackposture blansome mano1188 andreudzn visioisiv sidetrvcked shotbyafkinsuccan fawcan asun4 99froxy slurps m0ntxw parakeetxd poikau togazx", pewTimeS)
		self.send_message("/me TriHard nam_naam haxk xalhs frozennnnnnnnn h_h410 hejjavin isaacaba satanisteen keeev05 mm2pl xqc_goagane danht0308 lastweeknextday lilbyte321 y5or the_bigerm chateye choc_of_boxlates hawichii thewildings razik18 dimburuk tuntematon rosethemagician realroflkopter yosefsaa7 timusp nam_until_ban longtobacco ljackson77 chopped_cheese xerdies marcfryd xanory zreem evacuationz sosil osotaka jessei ethantp gelsonmartins luddinho98 ragnarosthefacelord mronbacond forsenbee", pewTimeS)
		self.send_message("/me TriHard borsen zugren swejerkk peberro golantrev caglapickaxe seambug spyboss mastondzn zolep gocho_ badoge feketebarany kagumiiin garrry_____12 college_boi carlossinhache maiman sushixt4 farbrorbarbro jose king_kong_monkey_dong wrayckage chachnaq miloski1 valeralytvak zanza_31 zemmygo farkasmartinka10 twolettername c4y_ kattah forsenlookingatyou andrewu1 cosmic46 yaxy123 shines_u phuwnaren123 freyr21 depressedpenguin1 jellyfried wishiie obiron05 pcbot1 mouzah_", pewTimeS)
		self.send_message("/me TriHard xsoretro roarnq schneppke teepo_ xx_somalian69soldier_xx katylou seta_7 vladibeer_ nefs behindpro spodemqn thopla tarnar purpledank punsy_ bencie_ spacewalrus hakanairuby cxtrlhard roytonux griphthefrog lazarius ashrynae collapsingwave redpls cloudchopper butterbertha estulence proteinhammer sulphuricwater shadyfey thepayr aakihiro chipdiptripleflips nimmy0 chepy5 widehardo1 rxuz porompti theohun7 direftp mik7 soto0o0 forsenisoffline bananaslayer_", pewTimeS)
		self.send_message("/me TriHard stelize bradleyym bubakmraz unbotherd2 flowering_maid sheirdz fabulouspotato69 phzeera narwhal4_ switchoff_ s4l1_ fatherpucci1 randomwatermelonlover rileyjevs argonchann copsycallum teotheparty phant0mblades forsendiscosnake depressedjew entropicvarash rigoenki imbanbot ooofs zuuber heliosoac snowstormcs bridgecrosser succannn pnblvn spongeb0g dahul_ nam_7_ dab_or_get_banned tiredu xaiu garug faked9 cbdg ixobst mai_desu der_sheff koalapfropfen tomatofield", pewTimeS)
		self.send_message("/me TriHard mariodertrader warriorfall n_e_c_ daniel_coo jar_jar_binks_lul 3gigz kyoci sparler syhwgsh sosil1 secretcolour cnys_ shungite_dealer_ 011097 vloted adriel_ariel jesseab_ lambo_man1 vak14 dwb__ thebridgepig lucas__kn setilix spiiidy264 ratot santana_c55 wabbla kalvarenga sc_yousef snoopadillios ooknumber15 tree_house bombey01 pagshake bajgen jeffboys123 felador viloxow jxjhn skalmanleif nk_sacul minimetiny wideschizojeb alecbirdman ok_reese ki9s codedninja", pewTimeS)
		self.send_message("/me TriHard polishedaqua shungite_dealer_raul muryomo urine_eagler absurdsec wisehardo xqcow1000 shotbyasuccanreprise zneix alazymeme sthic jose_ramiro_q yat1 bnasit lirandom shargo bryanfantasma rockf bigpenmans stangclever xsistinefibel evalover001 5g_frequencies slaming complaint_registar mightyezze gamey_cards treehouseinc scuffed_tyrone omegalyl xqcperson animelel4 back_2_the_roots chreint trihard_anele 4rneee tor_kit ryuuiro adamj04_2 setilix salmanald123", pewTimeS)
		self.send_message("/me TriHard pepedonk roxnr baus0 tenksit ledroy eardintv tommy_lindsey evander137 nekraad cloud9_gamin plsredscreen primelolwcz fiakes tdkumon obz117 toolameforname_ donas880 gofur srcookiemonstr jessevn__ jambiu true_pubg de127 doctor_bubbles saan1ty idemolisherxx panchosk_ csinhache reallyfriendly completoweno noctum2k daumenloser salad4zz steamyfreshmeme kevin_mazter multex_uwu tomplatz zieday highasakit3 kuma3g mrbarnabass qu0te iduuuuz xluks_ schoolwaspoggersxqcl", pewTimeS)
		self.send_message("/me TriHard mediocrefish 0kayga basedbepto juiceromegalul tltiechange_bot titie_changebot desctap forza9 golemq iluh7 yathrall oskart rxll0 justusshg blendzior vicinus aftereight88 pambroise seuss02 lidlfolkungagatan tiltedclone fomegalulrsen65 freevirus421 blitz6450 mormonftp_21 yokota_kazumi blackkk_ l7mon kristidouble26 nabusmain mace__777 smartgamer9 paotrejo_rdg kk4ri moonval maiksyk blad6e hoiic onni__xd bnick_ 4weirdchampp persms einleo", pewTimeS)
		self.send_message("/me TriHard nilethorment niemawiadomosci merry_go__ viemuchu uianbator teemokda 2547techno abrett monricow vixorea varggo_ kreutser vmyk baxpsn sleeplessseas jaeteejee zalux21 dercrxcker abdulla_47 backous gachi_waiting_room dxvidtreek billy3twitch po______ benjabum5 underscorejordan ccc909 hackmagic kawaqa shamelessness bogulent kruzzz__ ndaniei pepto__bismol kodyparbs kawazoo srcstc asaad_9 acrivfx sunsux rawblv onervaaa unsimplewn_ rxxbbie mati_2", pewTimeS)
		self.send_message("/me TriHard hulolo_ senderak namtheweebs koudys_ srjy_ jersonpr_ heriom indoient kannodi ruggedsnake2 faanthiel pbii jelexton eliahtreek soonz_ hecrazy yerdesh narthex__ maxdaxx metriz elias_1812 feelingweirdman plute chrisleon bruhz0ned victorbaya primusky lil_mario223 grataer sp00kycait sinatari otos_naits rfey vicesmile apuclassy turtlerush leekroom am8rosio 99pallas bootyboiy prong_ toy_volao__x_d pinnnnx gaboshiet s0lst1cio lucasev_ fernardo", pewTimeS)
		self.send_message("/me TriHard ugandanwarriarzulul scb45 posturelesshobo benjen5 36png ja77man allerbaster thedankestspecimen notlobu chunchuny silverlxne lnsc triz____ getshrekttwitch kryha5555 xdkaarim bajlata_ culling3 benjxxm kyamire boraflame danielapolo69 putupaula einmax_ sukimizuno tenkfemboy gigudrion lotass paauulli npas76 kiwiddle_ howardhoward sahu2709 peepogroove cheemsfroger maninblakkko jonasplayzbtw hillwoop jaystelly maninblakkko glink00 h3rrro", pewTimeS)
		self.send_message("/me TriHard elpuritoaguabendita pallaslol legro21 roppie smuuuuuuuuurf xxx69killer69xxx kurpyy sevennineeightt nyanzo matiasmanc0 krippkek novlo actuallyalbino velegand trihardjy kolamon insmensch deivid_e sil_sh ypony fullscreen_viewer_123 torikushiii antodee zeux1s pictoco adrkrm graymix0 x9______ leegoe fxl61 6o53 capresemartini ilotterytea israxylol florian_2807 byfredi_ 4kosxd sndkahvi suspiciousmonkey 3crowns_ notobz117 torisu_ oskar5oskar", pewTimeS)
		self.send_message("/me TriHard chopper_897 ludo_1337 frijolito2234 itzalexpl zunf y00nited simone1 psevdxnym bronze_rg forsen_said_what_now madmonqofficial nudelritter69 darkholmellll isildurr surprised_horse markzynk juwna lavardi guikuza bubbabunyip agwoper riflabaconbbx fernand0villarr lparzi fookstee vadikekw elpichu345 gaxd5 danizurbano lexonix khlody shootlikekd docsbathroomroyale law17_t drtrihouse victorv777 jonas_0330 notdhruvil fasim1 takideezy rwa122 cyphy", pewTimeS)
		# Can add couple of names to the line below
		self.send_message("/me TriHard bluedreams__ ttahotra hotbear1110 biertutgut17 katzee16 yeahalexander gentor600 jordyloxd babyeater668 mysztic manux_980 veryhag nutyyyy christurbate mizakhell ital3ny sodagod suttercane__ pikxw mxged marrubenfunero langgezockt jazzyviuxx gabrielkaa4 hlcky dlocky0n dasjoshy xhemyy toustik_ sunderred weilno roiandss enos2000live g4bben scb45 gaedo_ royalkitkat11 jnexpress legendydd cairoxo sunderred infinitiiyoo thejollyduck 2na_f2p", pewTimeS)
		self.send_message("/me TriHard prank855 jacedz zhandy38 bagassuo youseemchill gergo1015 epardes brodik88 kenrekt_ mattni_ peepotalk neutralics femithefeminist fijxuu mc_ride1 mysthd pepe_the_toad dddenyyyyy zenzre omegamk19 vile3j erniexiv pynput ricecookeerr zonianmidian cuxp angelfruits_vr itssssjoshh problematicchatter yukistarcraft thewaii_ idanielswi nourylul spurpshub shoto297 maldees schpetersen donas88o cowofdeath n0versal omrii__ mwjs  rnaom sausey__ jikope lordevid", pewTimeS)
		self.send_message("/me TriHard ccammunist erobb15 demotro_ midoriyokai pogi52 rxmdy jaareet fant1_ znixp toomucherry limamtopm stickihands kuoles pichu_345 carrul62 unitooth pelapa_ biwwwie sotiris_ael iceshard__ iwantummmmmmmm anthamin ajspyman alexisssu blwwwle racso_0 kroaat_ petthebot shihttzuu anthamin koalas28 lybei parallelfifthpolice metaljungle_ shitw unreleasedfromjailmate iatifi dagaugl tkamii ryanpotat dov_skal daamj devld__ jontemillian brockbuv acousticfrogg cristianr53 momi22 protear", pewTimeS)
		# Can add like one name to the line below
		self.send_message("/me TriHard iNF3CT0Rz jonzork dominar_u xqcow_waiting_room ronaldosen rob0___ icdb bander ottto_von_bismarck klaun85 forsenstares wekyyyc nishabtam redyoshi_ epicdonutdude_ archilllect dieziege danklipse banforsen spxney bryanfake845 asaltytoast suchperson guzzzzzzzy lllllllllllllllow etu_kekw_ never_doubt_the_god_gamer iniquitous_palygorskite elweones juicernat p4ul_3_ 100_ski hmoodybins diverslty mexicanguitarist_c55 Berba_Rooney_Tevez impaledChain filomaj kanyereeves Iuca1888", pewTimeS)
		self.send_message("/me TriHard BlackLivesMatter kkonaaaaaaaaaaa 0_________champ_________0 wwwwwwwwwwwwwwwwwwwwmmmww forsen________________baj QU0TE_IF_FORSEN_THREW", pewTimeS)

		print("executed")
		

class BotThread(threading.Thread) :
	def __init__(self, bot):
		self.bot = bot
		super(BotThread, self).__init__()

	def run(self):
		self.bot.start()
					

if __name__ == "__main__":
	sched_bot = None

	for channel in OWNERS:
		bot = Bot(channel)
		thread = BotThread(bot=bot)
		thread.start()
		print("Thread started for channel:" , channel)
		
		if "pewdiepie" in channel:
			sched_bot = bot
	if sched_bot is not None:	
		schedule.every().day.at("15:00").do(sched_bot.job)

		while True:
			schedule.run_pending()
			time.sleep(50)
