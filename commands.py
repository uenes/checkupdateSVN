from subprocess import Popen, PIPE
import sys

class Commands:

    def __init__(self):
        reload(sys)  
        sys.setdefaultencoding('UTF8')
        
    def svnStatus(self):
        process = Popen(['svn', 'status', '-u', sys.argv[1]], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        if stderr != '':
            raise NameError(stderr)
        return stdout

    def tortoiseUpdate(self, path):
        process = Popen(['TortoiseProc.exe', '/command:update', '/path:'+path, '/closeonend:0'], stdout=PIPE, stderr=PIPE) 
        stdout, stderr = process.communicate()
        if stderr != '':
            raise NameError(stderr)
        return stdout

    def textEditor(self, path):
        process = Popen(['notepad++', path], stdout=PIPE, stderr=PIPE) 
        stdout, stderr = process.communicate()
        if stderr != '':
            raise NameError(stderr)
        return stdout