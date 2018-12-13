import crypto
import threading

class splitThread(threading.Thread):
	def __init__(self,fsp,file):
		threading.Thread.__init__(self)
		print('split ', file)
		self.file = file
		self.fsp = fsp
		self.filesPart = []
	def run(self):
		print('Start Spliting ', self.file)
		self.fsp.parseOptions(self.file,'s')
		self.filesPart = self.fsp.do_work()


class encryptThread(threading.Thread):
	def __init__(self,passwoed,file):
		threading.Thread.__init__(self)
		print('encrypting ', file)
		self.passwoed = passwoed
		self.file = file

	def run(self):
		print('Start encrypting ', self.file)
		crypto.encrypt(self.passwoed,self.file)

class decryptThread(threading.Thread):
	def __init__(self,passwoed,file):
		threading.Thread.__init__(self)
		self.passwoed = passwoed
		self.file = file

	def run(self):
		print('Start decrypting ', self.file)
		crypto.decrypt(self.passwoed,self.file)


class combineThread(threading.Thread):
	def __init__(self,fsp, file1, file2):
		threading.Thread.__init__(self)
		self.fsp = fsp
		self.file1 = file1
		self.file2 = file2

	def run(self):
		print('Join files')
		self.fsp.combine(self.file1,self.file2)
