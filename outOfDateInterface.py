from Tkinter import *
from subprocess import Popen, PIPE

class OutOfDateInterface:
	
	def __init__(self, master, pathServerChanges):
		self.__messageTopo = StringVar()
		top = Label(master, textvariable=self.__messageTopo, font=("Helvetica", 14))
		top.pack()
		self.__messageTopo.set('Novos commits realizados no branch \n \n')
		
		self.__message = StringVar()
		w = Label(master, textvariable=self.__message, font=("Helvetica", 12), justify="left")
		w.pack()
		self.__message.set(pathServerChanges)
				
		frame = Frame(master)
		frame.pack(padx=200, pady=20)

		self.button = Button(
			frame, text="Sair", fg="red", font=("Helvetica", 14) ,command=frame.quit
		)
		self.button.pack(side=RIGHT)

		self.hi_there = Button(frame, text="Update", font=("Helvetica", 14), command=self.update)
		self.hi_there.pack(side=LEFT)
		#self.Border = Tkinter.Frame(self, relief='flat', borderwidth=4)

	def update(self):
		process = Popen(['svn', 'update', sys.argv[1]], stdout=PIPE, stderr=PIPE) #'--accept e',
		stdout, stderr = process.communicate()
		
		self.__message.set('Update executado com sucesso! \n \n' + stdout)
		
		if stdout.find('conflict') != -1:
			process = Popen(['e'], stdout=PIPE, stderr=PIPE)
			stdout, stderr = process.communicate()
		