import sys
import ctypes  
import time
from subprocess import Popen, PIPE

timeOfDelay = 300

while True:
	# C:\\inetpub\\wwwroot\\Integracao_SIF_SEI_Sprint5
	process = Popen(['svn', 'status', '-u', sys.argv[1]], stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	lista = stdout.splitlines()

	listOfServerChanges = []
	listOfLocalChanges = []

	for item in lista:
		isServerChange = item.find('*')
		if isServerChange != -1:
			listOfServerChanges.append(item)
		else:
			if item[0] == 'M':
				listOfLocalChanges.append(item)
			
	stringOfPathServerChanges = ''		
	for item in listOfServerChanges:
		indexOfPath = item.find('C:')
		path = item[indexOfPath:len(item)]
		lastOne = path.rfind('\\')
		previousLastOne = path[0:lastOne].rfind('\\')
		stringOfPathServerChanges = stringOfPathServerChanges + path[previousLastOne:len(path)] + '\n'
		 
		
	#listOfPathLocalChanges = []	
	#for item in listOfPathLocalChanges:
	#	indexOfPath = item.find('C:')
	#	path = item[indexOfPath:len(item)]		


	if len(listOfServerChanges) == 0:
		message = u'Novos commits realizados no branch \n \n' + stringOfPathServerChanges + '\n \n Atualizar a copia local? \n \n Cancel : Proxima verificacao em 8 horas'
		result = ctypes.windll.user32.MessageBoxW(0, message , u'ALERTA', 0x3|0x20|0x10000|0x40000)
		print result
		if result == 2:
			timeOfDelay = 28800
		if result == 6:
			process = Popen(['svn', 'update', sys.argv[1]], stdout=PIPE, stderr=PIPE)
			stdout, stderr = process.communicate()
			message = u' Resultado do Update : \n \n blablabla' + stdout
			ctypes.windll.user32.MessageBoxW(0, message , u'ALERTA', 0x0|0x40|0x10000|0x40000)
		
	time.sleep(timeOfDelay)
	timeOfDelay = 300