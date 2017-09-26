from Tkinter import *
from subprocess import Popen, PIPE

class OutOfDateInterface:
	
	def __init__(self, master, pathServerChanges):
		# ******* Mensagem no topo da janela ******* 
		self.__messageTopo = StringVar()
		top = Label(master, textvariable=self.__messageTopo, font=("Helvetica", 14))
		top.pack()
		self.__messageTopo.set('Novos commits realizados no branch: \n ')
		
		# ******* Mensagem do corpo da janela ******* 
		self.__message = StringVar()
		w = Label(master, textvariable=self.__message, font=("Helvetica", 12), justify="left")
		w.pack()
		
		# ******* Lista para apresentar os arquivos alterados ******* 
		self.__pathServerChanges = pathServerChanges
		self.__listOfPaths = StringVar(value=pathServerChanges)
		print self.__listOfPaths
		self.__listBoxChanged = Listbox(master, listvariable=self.__listOfPaths, width = 10)
		self.__listBoxChanged.config(width=0)
		self.__listBoxChanged.bind('<Double-1>', self.openFile)
		self.__listBoxChanged.pack()
		
		frame = Frame(master)
		frame.pack(padx=200, pady=10)

		# ******* Buttons ******* 
		self.quitButton = Button(frame, text="Sair", fg="red", font=("Helvetica", 14) ,command=frame.quit)
		self.quitButton.pack(side=RIGHT)

		self.updateButton = Button(frame, text="Update", font=("Helvetica", 14), command=self.update)
		self.updateButton.pack(side=LEFT)
		
	def hasConflictInDryRun(self, stdout):
		list = stdout.splitlines()
		
		for line in list:
			if line[0] == 'C':
				return True
		return False

	def update(self): # tem qe inverter... update primeiro e dps verifica os arquivos com conflito
		# EXECUTAR UPDATE
		process = Popen(['TortoiseProc.exe', '/command:update', '/path:'+sys.argv[1], '/closeonend:0'], stdout=PIPE, stderr=PIPE) 
		stdout, stderr = process.communicate()
		if stderr == '':
			self.__messageTopo.set('Update realizado com sucess! \n ')
	
	def getListConflictPaths(self, stdoutDryRun):
		listOutput = stdoutDryRun.splitlines()
		result = []
		for line in listOutput:
			if line[0] == 'C':
				result.append(line[5:len(line)])
				print line[5:len(line)]
		return result
	
	def getStringFromList(list):
		result = ''
		for item in list:
			result = result + item + '\n'
		return result

	def openFile (self, *args):
		index = self.__listBoxChanged.curselection()
		if len(index) == 1:
			process = Popen(['notepad++', self.__pathServerChanges[0]], stdout=PIPE, stderr=PIPE) 
			stdout, stderr = process.communicate()