# encoding: utf-8
from Tkinter import *
import sys
import ctypes  
import time
from subprocess import Popen, PIPE
from outOfDateInterface import OutOfDateInterface
from commands import Commands

# **************** BEGIN FUNCTIONS ****************
def getListOfServerChanges (lista):
	result = []
	for item in lista:
		isServerChange = item.find('*')
		if isServerChange != -1:
			beginIndexOfPath = item.find('C:\\')
			result.append(item[beginIndexOfPath:len(item)])
	return result

def getStrOfPathServerChanges (listOfServerChanges):
	result = ''
	for item in listOfServerChanges:
		indexOfPath = item.find('C:')
		path = item[indexOfPath:len(item)]
		lastOne = path.rfind('\\')
		previousLastOne = path[0:lastOne].rfind('\\')
		result = result + path[previousLastOne:len(path)] + '\n'
	return result

def checkForPotentialConflict (lista):
	result = []
	for item in lista:
		isServerChange = item.find('*')
		isLocalChange = item[0]
		if isServerChange != -1 and item[0] == "M":
			return True 
		
	return False
	
def openOutOfDateWindow(pathServerChanges):
	root = Tk()
	interface = OutOfDateInterface()
	interface.openNewCommitsInterface(root, pathServerChanges)
	root.iconbitmap('sync.ico')
	root.mainloop()
	root.destroy()

def openErrorMessage(message):
	root = Tk()
	interface = OutOfDateInterface()
	interface.errorMessage(root, message)
	root.iconbitmap('sync.ico')
	root.mainloop()
	root.destroy()
	
# **************** END FUNCTIONS ****************


timeOfDelay = 600
reload(sys)  
sys.setdefaultencoding('UTF8')

while True:
	commands = Commands()
	try:
		lista = commands.svnStatus().splitlines()
		listOfServerChanges = getListOfServerChanges(lista)
		if len(listOfServerChanges) > 0:
			openOutOfDateWindow(listOfServerChanges)
	except NameError, e:
		openErrorMessage(e)
	
	time.sleep(timeOfDelay)