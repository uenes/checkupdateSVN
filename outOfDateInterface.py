from Tkinter import *
from subprocess import Popen, PIPE
from commands import Commands

class OutOfDateInterface:
	
	def __init__(self):
		print "Init"
	
	def openNewCommitsInterface(self, master, pathServerChanges):
		master.title('Atualizar Workspace')
		self.__master = master
		# ******* Mensagem no topo da janela ******* 
		self.__messageTopo = StringVar()
		top = Label(master, textvariable=self.__messageTopo, font=("Helvetica", 14))
		top.pack()
		self.__messageTopo.set('Novos commits realizados no branch: ')
		
		# ******* Mensagem do corpo da janela ******* 
		self.__message = StringVar()
		w = Label(master, textvariable=self.__message, font=("Helvetica", 12), justify="left")
		w.pack()
		
		# ******* Lista para apresentar os arquivos alterados ******* 
		self.__pathServerChanges = pathServerChanges
		self.__listOfPaths = StringVar(value=pathServerChanges)
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

	def update(self):
		try:
			commands = Commands()
			commands.tortoiseUpdate(sys.argv[1])
			self.__messageTopo.set('Update realizado com sucess! ')
		except NameError, e: # TRATAR O ERRO NO UPDATE
			self.errorMessage(e)
	
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
			commands = Commands()
			commands.textEditor(self.__pathServerChanges[0])
		
	def errorMessage (self, message):
		self.__master.title('Erro')
		self.__messageTopo.set('Ocorreu um erro')
		self.__message.set(message)

		# ******* Limpar tela *******
		self.__listBoxChanged.pack_forget()