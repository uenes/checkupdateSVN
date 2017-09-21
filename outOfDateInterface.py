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

	def update(self): 
		process = Popen(['svn', 'merge', '--dry-run' ,'-r', 'BASE:HEAD', '.'], cwd=sys.argv[1], stdout=PIPE, stderr=PIPE) 
		stdout, stderr = process.communicate()
		
		if stderr == '':
			stdoutDryRun = stdout
			listConflictPath = self.getListConflictPaths(stdoutDryRun)
			process = Popen(['svn', 'update', '--accept', 'e', sys.argv[1]], stdout=PIPE, stderr=PIPE) 
			stdout, stderr = process.communicate()
			stdoutUpdate = stdout
			
			if stderr == '':
				if self.getListConflictPaths(stdoutDryRun):
					for path in listConflictPath:
						process = Popen(['WinMergeU', path], cwd=sys.argv[1], stdout=PIPE, stderr=PIPE) 
						stdout, stderr = process.communicate()
					self.__message.set('Resolva os conflitos: \n \n' + self.getStringFromList(listConflictPath))
				else:				
					self.__message.set('Update executado com sucesso! \n \n' + stdoutUpdate)
			else:
				self.__message.set('Houve um erro no update. \n \n' + stdoutUpdate)
		else:
			self.__message.set('Houve um erro no update. \n \n' + stdoutUpdate)
	
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