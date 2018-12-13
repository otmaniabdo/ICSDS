import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
import split
import Threads
import time
import os
import glob

password = 'masterbigdata218'
fsp = split.FileSplitter()
filesPart = []
directory = ['temp/','client/']


for f in glob.glob("temp/*.*"):
	os.remove(f)

for d in directory:
	if not os.path.exists(d):
	    os.makedirs(d)


    	
def dialogfile():
	global filename
	filename = filedialog.askopenfilename(initialdir="/", title="Select file :",
                                          filetype=(("jpeg", "*.jpg"), ("All Files", "*.*")))
	filename_label = ttk.Label(fram_file, text=filename).grid(row=1)
	label_message.insert(END,'File Added')

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

	time.sleep(1)

	os.remove(t0.filesPart[0]) 
	os.remove(t0.filesPart[1])

	progressbar.stop()



root = Tk()
root.title("Client")
root.geometry('440x600')

fram_connection = ttk.LabelFrame(root, text="Connection :")
fram_connection.pack()
fram_connection.config(padding=10)

connection = tk.Button(fram_connection, text="Connecter")
connection.grid(row=4, column=2, pady=10)

server1 = tk.Label(fram_connection, text="SERVER 1 :").grid(row=0, column=0)
serverStatu = tk.Label(fram_connection, text="en attente...").grid(row=0, column=1, padx=10, pady=10)

labelAdress1 = tk.Label(fram_connection, text="Adresse :").grid(row=1, column=0)
adresse1 = tk.Entry(fram_connection).grid(row=1, column=1)

labelPort1 = tk.Label(fram_connection, text="Prot :").grid(row=1, column=3)
port1 = tk.Entry(fram_connection).grid(row=1, column=4)

server2 = tk.Label(fram_connection, text="SERVER 2 :").grid(row=2, column=0)
serverStatu = tk.Label(fram_connection, text="en attente...").grid(row=2, column=1, padx=10, pady=10)

labelAdress2 = tk.Label(fram_connection, text="Adresse :").grid(row=3, column=0)
adresse2 = tk.Entry(fram_connection).grid(row=3, column=1)

labelPort2 = tk.Label(fram_connection, text="Port :").grid(row=3, column=3)
port2 = tk.Entry(fram_connection).grid(row=3, column=4)

fram_file = ttk.LabelFrame(root, text="File :")
fram_file.pack()
fram_file.config(padding=10)

filename = tk.StringVar()

openfile = tk.Button(fram_file, text="Select file", command=dialogfile, padx=10).grid(row=0, padx=160, pady=10)

frame_crypto = ttk.LabelFrame(root, text = "Chiffrement :")
frame_crypto.pack()
frame_crypto.config(padding=10)

crypt = tk.IntVar()

r1 = tk.Radiobutton(frame_crypto, text="AES", padx=40, variable=crypt,value=1).grid(row=0,column=0)
r2 = tk.Radiobutton(frame_crypto, text="RSA", padx=40, variable=crypt,value=2).grid(row=0,column=1)
r3 = tk.Radiobutton(frame_crypto, text="GPG", padx=40, variable=crypt,value=3).grid(row=0,column=2)


frame_send = ttk.LabelFrame(root, text = "Send :")
frame_send.pack()
frame_send.config(padding=20)

progressbar = ttk.Progressbar(frame_send, orient=tk.HORIZONTAL, length= 200)
progressbar.grid(row=0, column=0)
progressbar.config(mode= 'indeterminate')
progressbar.stop()


espace = tk.Label(frame_send, text="                      ").grid(row=0,column=1)
send = tk.Button(frame_send, text="Upload", padx=20, command=upload).grid(row=0, column=2)

frame_message = ttk.LabelFrame(root, text = "Log :")
frame_message.pack(fill=BOTH)
frame_message.config(padding=5)

label_message = tk.Listbox(frame_message,bg='black',fg='green')
label_message.pack(fill=BOTH)
label_message.configure()
root.mainloop()

