# encoding: utf-8
from Tkinter import *
import sys
import ctypes  
import time
from subprocess import Popen, PIPE
from outOfDateInterface import OutOfDateInterface


# **************** BEGIN FUNCTIONS ****************
def getListOfServerChanges (lista):
	result = []
	for item in lista:
		isServerChange = item.find('*')
		if isServerChange != -1:
			result.append(item)
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

def messageOfNonUpToDate (stringOfPathServerChanges):
	message = u'Novos commits realizados no branch \n \n' + stringOfPathServerChanges + '\n \n Atualizar a cópia local? \n \n Não : Adiar por 8 horas'
	return ctypes.windll.user32.MessageBoxW(0, message , u'ALERTA', 0x3|0x20|0x10000|0x40000)	

def messageUpdateResult (updateResult, stderr):
	message = u'Update realizado com sucesso!' 
	ctypes.windll.user32.MessageBoxW(0, message , u'ALERTA', 0x0|0x40|0x10000|0x40000)

def checkForPotentialConflict (lista): # TERMINARRR
	result = []
	for item in lista:
		isServerChange = item.find('*')
		isLocalChange = item[0]
		if isServerChange != -1 and item[0] == "M":
			return True 
		else:
			return False
	
def openOutOfDateWindow(pathServerChanges):
	root = Tk()
	app = OutOfDateInterface(root, pathServerChanges)
	root.mainloop()
	root.destroy()

def statusCommand ():
	process = Popen(['svn', 'status', '-u', sys.argv[1]], stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	return stdout
	
# **************** END FUNCTIONS ****************


timeOfDelay = 300
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

while True:
	# C:\\inetpub\\wwwroot\\Integracao_SIF_SEI_Sprint5
	lista = statusCommand().splitlines()

	listOfServerChanges = getListOfServerChanges(lista)
	conflict = checkForPotentialConflict(lista)
	stringOfPathServerChanges = getStrOfPathServerChanges(listOfServerChanges)	
	if conflict:
		stringOfPathServerChanges = stringOfPathServerChanges + '\n Atenção! Podem haver conflitos.'

	if len(listOfServerChanges) > 0:
		openOutOfDateWindow(stringOfPathServerChanges)
		
	time.sleep(timeOfDelay)
	timeOfDelay = 300

