# encoding: utf-8

import sys
import ctypes  
import time
from subprocess import Popen, PIPE


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
	message = u'Novos commits realizados no branch \n \n' + stringOfPathServerChanges + '\n \n Atualizar a cópia local? \n \n Não : Próxima verificação em 8 horas'
	return ctypes.windll.user32.MessageBoxW(0, message , u'ALERTA', 0x3|0x20|0x10000|0x40000)	

def messageUpdateResult (updateResult, stderr):
	#if updateResult is not None:
	message = u'Update realizado com sucesso! ' 
	#else:
	#	message = u' Resultado do Update : \n \n ' + type(updateResult)
	ctypes.windll.user32.MessageBoxW(0, message , u'ALERTA', 0x0|0x40|0x10000|0x40000)

# **************** END FUNCTIONS ****************
	
timeOfDelay = 300
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

while True:
	# C:\\inetpub\\wwwroot\\Integracao_SIF_SEI_Sprint5
	process = Popen(['svn', 'status', '-u', sys.argv[1]], stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	lista = stdout.splitlines()

	listOfServerChanges = getListOfServerChanges(lista)
			
	stringOfPathServerChanges = getStrOfPathServerChanges(listOfServerChanges)			

	if len(listOfServerChanges) > 0:
		result = messageOfNonUpToDate(stringOfPathServerChanges)
		if result == 7:
			timeOfDelay = 28800
		if result == 6:
			process = Popen(['svn', 'update', sys.argv[1]], stdout=PIPE, stderr=PIPE)
			stdout, stderr = process.communicate()
			messageUpdateResult(stdout, stderr)
		
	time.sleep(timeOfDelay)
	timeOfDelay = 300

