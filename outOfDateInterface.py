from Tkinter import *
from subprocess import Popen, PIPE

class OutOfDateInterface:
	
	def __init__(self, master, pathServerChanges):
		self.__messageTopo = StringVar()
		top = Label(master, textvariable=self.__messageTopo, font=("Helvetica", 14))
		top.pack()
		self.__messageTopo.set('Novos commits realizados no branch \n ')
		
		self.__message = StringVar()
		w = Label(master, textvariable=self.__message, font=("Helvetica", 12), justify="left")
		w.pack()
		self.__message.set(pathServerChanges)
				
		frame = Frame(master)
		frame.pack(padx=200, pady=10)

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

	def update(self): # VERIFICAR o uso da opcao  --dry-run 
		process = Popen(['svn', 'merge', '--dry-run' ,'-r', 'BASE:HEAD', '.'], cwd=sys.argv[1], stdout=PIPE, stderr=PIPE) 
		stdout, stderr = process.communicate()
		print stdout
		print stderr
		
		if stderr == '':
			if not self.hasConflictInDryRun(stdout):
				process = Popen(['svn', 'update', sys.argv[1]], stdout=PIPE, stderr=PIPE) #'--accept e',
				stdout, stderr = process.communicate()
				
				if stderr == '':
					self.__message.set('Update executado com sucesso! \n \n' + stdout)
				else:
			else:
				self.__message.set('Update com conflito! \n Por favor, execute o update com o TortoiseSVN para resolver os conflitos \n \n' + stdout)
		else:
			self.__message.set('Houve um erro no update. \n \n' + stderr)
	