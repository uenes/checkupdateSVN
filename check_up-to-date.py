# encoding: utf-8
from Tkinter import *
import sys
import ctypes  
import time
from subprocess import Popen, PIPE
from outOfDateInterface import OutOfDateInterface

# C:\\inetpub\\wwwroot\\Integracao_SIF_SEI_Sprint5

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
	app = OutOfDateInterface(root, pathServerChanges)
	root.iconbitmap('sync.ico')
	root.mainloop()
	root.destroy()

def statusCommand ():
	process = Popen(['svn', 'status', '-u', sys.argv[1]], stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	return stdout
	
# **************** END FUNCTIONS ****************


timeOfDelay = 300
reload(sys)  
sys.setdefaultencoding('UTF8')

while True:
	lista = statusCommand().splitlines()

	listOfServerChanges = getListOfServerChanges(lista)
	
	if len(listOfServerChanges) > 0:
		openOutOfDateWindow(listOfServerChanges)
	time.sleep(timeOfDelay)
	
