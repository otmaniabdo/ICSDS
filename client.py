import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
import split
import Threads
import time
import os
import glob
import socket
import threading

password = 'masterbigdata218'
fsp = split.FileSplitter()
filesPart = []
directory = ['temp/','client/']
connecter = False

for f in glob.glob("temp/*.*"):
	os.remove(f)

for d in directory:
	if not os.path.exists(d):
	    os.makedirs(d)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	
def dialogfile():
	global filename
	filename = filedialog.askopenfilename(initialdir="/", title="Select file :",
                                          filetype=(("jpeg", "*.jpg"), ("All Files", "*.*")))
	filename_label = ttk.Label(fram_file, text=filename).grid(row=1)
	label_message.insert(END,'File Added')

def uploadThread():
	threading.Thread(target=upload).start()

def downloadThread():
	threading.Thread(target=download).start()

def upload():
	global filename
	global fsp
	global password


	progressbar.start()
	label_message.insert(END,'File Splited : '+filename)
	t0 = Threads.splitThread(fsp, filename)

	t0.start()
	time.sleep(2)

	label_message.insert(END,'Files Encrypting :')

	label_message.insert(END, '    -->' + t0.filesPart[0])
	t1 = Threads.encryptThread(password,t0.filesPart[0])

	label_message.insert(END, '    -->' + t0.filesPart[1])
	t2 = Threads.encryptThread(password,t0.filesPart[1])

	t1.start()
	t2.start()

	t1.join()
	t2.join()

	time.sleep(5)

	print (t0.filesPart)
	filename1 = str.encode('filename**'+t0.filesPart[0].replace('temp/','')+'.inc')
	filename2 = str.encode('filename**'+t0.filesPart[1].replace('temp/','')+'.inc')
	print(filename1)
	if connecter:
		i = 0
		for f in t0.filesPart:
			with open(f+'.inc', 'rb') as fs:
				if i == 0:
					label_message.insert(END, '-> Send File 1')
					s.send(filename1)
				else:
					label_message.insert(END, '-> Send File 2')
					s2.send(filename2)
				while True:
					data = fs.read(1024)
					if(i == 0):
						s.send(data)
					else:
						s2.send(data)
					if not data:
						break
				if i == 0:
					s.send(b'ENDED')
				else:
					s2.send(b'ENDED')
				fs.close()
				i = i + 1 
	progressbar.stop()


def download():
	if connecter:
		i = 0
		while(i < 2):
			if i == 0:
				filenamedownload = str.encode('downloadfile**'+filedownload.get()+'-1.inc')
				s.send(filenamedownload)
				with open('temp/'+filedownload.get()+'-1.inc', "wb") as fw:
					while True:
						data = s.recv(1024)
						if data == b'ENDED':
							print("END recv")
							break
						fw.write(data)
					fw.close()
					i = i + 1
			elif i == 1:
				filenamedownload = str.encode('downloadfile**'+filedownload.get()+'-2.inc')
				s2.send(filenamedownload)
				with open('temp/'+filedownload.get()+'-2.inc', "wb") as fw:
					while True:
						data = s2.recv(1024)
						if data == b'ENDED':
							print("END recv")
							break
						fw.write(data)
					fw.close()
					i = i +1
		t1 = Threads.decryptThread(password,'temp/'+filedownload.get()+'-1.inc')
		t2 = Threads.decryptThread(password,'temp/'+filedownload.get()+'-2.inc')
		t1.start()
		t2.start()
		time.sleep(2)
		t3 = Threads.combineThread(fsp,'temp/'+filedownload.get()+'-1','temp/'+filedownload.get()+'-2')
		t3.start()

def connecter():
	global serverStatu
	s.connect((adresse.get(),int(port.get())))
	label_message.insert(END, ' --> connected to server1')
	s2.connect((a2.get(),int(p2.get())))
	label_message.insert(END, ' --> connected to server2')
	connecter = True

root = Tk()
root.title("Client")
root.geometry('440x600')

adresse = StringVar()
port = StringVar()

a2 = StringVar()
p2 = StringVar()

fram_connection = ttk.LabelFrame(root, text="Connection :")
fram_connection.pack()
fram_connection.config(padding=10)

connection = tk.Button(fram_connection, text="Connecter",command=connecter)
connection.grid(row=4, column=2, pady=10)

server1 = tk.Label(fram_connection, text="SERVER 1 :")
server1.grid(row=0, column=0)

labelAdress1 = tk.Label(fram_connection, text="Adresse :").grid(row=1, column=0)
adresse1 = tk.Entry(fram_connection,textvariable=adresse).grid(row=1, column=1)

labelPort1 = tk.Label(fram_connection, text="Prot :").grid(row=1, column=3)
port1 = tk.Entry(fram_connection,textvariable=port).grid(row=1, column=4)

server2 = tk.Label(fram_connection, text="SERVER 2 :").grid(row=2, column=0)

labelAdress2 = tk.Label(fram_connection, text="Adresse :").grid(row=3, column=0)
adresse2 = tk.Entry(fram_connection, textvariable=a2).grid(row=3, column=1)

labelPort2 = tk.Label(fram_connection, text="Port :").grid(row=3, column=3)
port2 = tk.Entry(fram_connection, textvariable=p2).grid(row=3, column=4)

fram_file = ttk.LabelFrame(root, text="File :")
fram_file.pack()
fram_file.config(padding=10)

filename = tk.StringVar()

openfile = tk.Button(fram_file, text="Select file", command=dialogfile, padx=10).grid(row=0, padx=160, pady=10)

frame_crypto = ttk.LabelFrame(root, text = "Telechargement :")
frame_crypto.pack()
frame_crypto.config(padding=10)

filedownload = tk.StringVar()

downloadEntry = tk.Entry(frame_crypto,width=50,textvariable=filedownload).grid(row=0,column=0)
downloadButton = tk.Button(frame_crypto,text='Download',command=downloadThread).grid(row=0,column=1)


frame_send = ttk.LabelFrame(root, text = "Send :")
frame_send.pack()
frame_send.config(padding=20)

progressbar = ttk.Progressbar(frame_send, orient=tk.HORIZONTAL, length= 200)
progressbar.grid(row=0, column=0)
progressbar.config(mode= 'indeterminate')
progressbar.stop()


espace = tk.Label(frame_send, text="                      ").grid(row=0,column=1)
send = tk.Button(frame_send, text="Upload", padx=20, command=uploadThread).grid(row=0, column=2)

frame_message = ttk.LabelFrame(root, text = "Log :")
frame_message.pack(fill=BOTH)
frame_message.config(padding=5)

label_message = tk.Listbox(frame_message,bg='black',fg='green')
label_message.pack(fill=BOTH)
label_message.configure()
root.mainloop()

