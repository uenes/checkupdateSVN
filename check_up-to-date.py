import sys
import ctypes  
import time
from subprocess import Popen, PIPE



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
			print item
			listOfServerChanges.append(item)
		else:
			if item[0] == 'M':
				print item
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


	if len(listOfServerChanges) > 0:
		result = ctypes.windll.user32.MessageBoxW(0, u'Novos commits realizados no branch \n \n' + stringOfPathServerChanges, u'ALERTA', 1)
		#if result == 1:
		#	process = Popen(['svn', 'update', sys.argv[1]], stdout=PIPE, stderr=PIPE)
		#	stdout, stderr = process.communicate()
		#	resultUpdate = ctypes.windll.user32.MessageBoxW(0, u' Resultado do Update : ' + '\n \n' + stdout, u'UPDATE', 1)
		
	time.sleep(60)