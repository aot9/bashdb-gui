#! /usr/bin/env python

import pexpect
import re
class BashDb():
    def __init__(self, scriptname):
    
        self.appOut = None
        self.curSourceFile = None
        self.curCodeLine = None
        self.prevCmd = None
        
        self.script = scriptname
        self.child = pexpect.spawn('bashdb -q ' + self.script)
        self.child.expect('bashdb<.*>')

        self.__parseOutput(self.__getOutput())

    def __getOutput(self):
        return (self.child.before + self.child.after).replace('\n', '').split('\r') 
    
    def __parseOutput(self, text):
        self.appOut = ''
        if self.prevCmd:
            text = text[1:]
        for line in text:
            matchObj = re.match(r'\s?\((.*\.sh):(\d)+\):', line)
            if matchObj:
                self.curSourceFile = matchObj.group(1)
                self.curCodeLine = int(matchObj.group(2))
                break
            else:
                self.appOut += line + '\n'
    
    def __cmd(self, command):
        self.prevCmd = command
        self.child.send(command + '\n')
        self.child.expect('bashdb<.*>')
        self.__parseOutput(self.__getOutput())
    
    def readSourceCode(self):
        return [line.replace('\r', '') for line in open(self.script).readlines()]
    
    def getCurCodeLine(self):
        return self.curCodeLine

    def getAppOutput(self):
        return self.appOut

    def getCurSrcFile(self):
        return self.curSourceFile

    def step(self):
        self.__cmd('step')

    def run(self):
        self.__cmd('cont')

    def quit(self):
        self.__cmd('q')
    
    def restart(self):
        self.__cmd('R')
    
if __name__ == '__main__':
    db = BashDb('./test.sh')
    db.step()
    db.step()
    db.step()
    db.restart()
    db.step()
    db.step()
    #db.quit()


