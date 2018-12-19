import tkinter as tk
from tkinter import *
import os
import socket
from tkinter import ttk, filedialog
import threading

if not os.path.exists('server2/'):
	    os.makedirs('server2')

def connecterThread():
	global serverStatu
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverRunning = True
	label_message.insert(END, '--> Running server on '+adresse.get()+' / '+port.get())
	s.bind((adresse.get(),int(port.get())))
	s.listen()
	label_message.insert(END, '--> server ready ')
	while serverRunning:
		client, adress = s.accept()
		serverStatu.configure(text="connecter")
		label_message.insert(END, '--> {} connected to the server'.format(adress))
		filename = ''
		first = 0
		while True:
			data = client.recv(1024)
			if 'filename**' in data.decode():
				filename = 'server2/'+data.decode().replace('filename**','')
				with open(filename, "wb") as fw:
					print("Receiving..")
					while True:
						data = client.recv(1024)
						if data == b'ENDED':
							print("END recv")
							label_message.insert(END, 'Received : '+filename)
							break
						fw.write(data)
					fw.close()					
			elif 'downloadfile**' in data.decode():
				filename = 'server2/'+data.decode().replace('downloadfile**','')
				if os.path.exists(filename):
					with open(filename, 'rb') as fs:
						while True:
							data = fs.read(1024)
							client.send(data)
							if not data:
								break
						client.send(b'ENDED')
						fs.close()
				else:
					label_message.insert(END, 'File not found')
		client.close()

def connecter():
	threading.Thread(target=connecterThread).start()


root = Tk()
root.title("Server 2")
root.geometry('300x400')

port = tk.StringVar()
adresse = tk.StringVar()

fram_connection = ttk.LabelFrame(root)
fram_connection.pack()
fram_connection.config(padding=20)

connection = tk.Button(fram_connection, text="Connecter", command=connecter)
connection.grid(row=4, column=1, pady=10)

serverAdd = tk.Label(fram_connection, text="Server Statu :").grid(row=0, column=0)
serverStatu = tk.Label(fram_connection, text="déconnecter")
serverStatu.grid(row=0, column=1, padx=10, pady=10)

labelAdress1 = tk.Label(fram_connection, text="Adresse :").grid(row=1, column=0)
adresseEntry = tk.Entry(fram_connection,textvariable=adresse).grid(row=1, column=1)

labelPort1 = tk.Label(fram_connection, text="Prot :").grid(row=2, column=0)
portEntry = tk.Entry(fram_connection,textvariable=port).grid(row=2, column=1)


frame_message = ttk.LabelFrame(root, text = "Log :")
frame_message.pack(fill=BOTH)
frame_message.config(padding=5)

label_message = tk.Listbox(frame_message,bg='black',fg='green')
label_message.pack(fill=BOTH)
label_message.configure()


root.mainloop()