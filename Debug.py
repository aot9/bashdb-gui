#! /usr/bin/env python

import pexpect
import re

class BashDb():
    def __init__(self, scriptname):
    
        self.appOut = None
        self.curCodeLine = None
        self.prevCmd = None
        
        self.breakList = {}
        self.watchList = {}
        
        self.curSourceFile = scriptname

        self.child = pexpect.spawn('bashdb -q ' + scriptname)
        self.child.expect('bashdb<.*>')

        self.__parseOutput(self.__getOutput())

    def __getOutput(self):
        return (self.child.before + self.child.after).replace('\n', '').split('\r') 
    
    def __parseOutput(self, text):
        self.appOut = ''
        if self.prevCmd:
            text = text[1:]
        for line in text:
            matchObj = re.match(r'\s?\((.*\.sh):(\d+)\):', line)
            if matchObj:
                self.curSourceFile = matchObj.group(1)
                self.curCodeLine = int(matchObj.group(2))
                break
            else:
                self.appOut += line + '\n'
    
    def __cmd(self, command, parseOutput = True):
        self.prevCmd = command
        self.child.send(command + '\n')
        self.child.expect('bashdb<.*>')
        if parseOutput:
            self.__parseOutput(self.__getOutput())
    
    def readSourceCode(self):
        return [line.replace('\r', '') for line in open(self.curSourceFile).readlines()]
    
    def getCurCodeLine(self):
        return self.curCodeLine

    def getAppOutput(self):
        return self.appOut

    def getCurSrcFile(self):
        return self.curSourceFile

    def getWatchList(self):
        self.__updateWatchList()
        return [var+' ='+val for var, val in self.watchList.iteritems()]
    
    def addVarToWatch(self, var):
        if var not in self.watchList.keys():
            self.watchList[var] = None
    
    def remVarFromWatch(self, var):
        try:
            del self.watchList[var]
        except KeyError:
            pass

    def __updateWatchList(self):
        cmd = 'print "'
        delim = '<var_delim>'
        for key in self.watchList:
            cmd +=  delim + ' ' + '$' + key
        cmd += '"'
        self.__cmd(cmd, parseOutput = False) 
        
        vals = self.__getOutput()[1].split("<var_delim>")[1:]
        
        for key, val in zip(self.watchList.keys(), vals):
            self.watchList[key] = val

    def br(self, lineNr):
        if lineNr not in self.breakList or self.breakList[lineNr] == False:
            self.breakList[lineNr] = True
            self.__cmd('br ' + str(lineNr + 1), parseOutput = False)
        else:
            self.breakList[lineNr] = False
            self.__cmd('clear ' + str(lineNr + 1), parseOutput = False)

    def step(self):
        self.__cmd('step')

    def next(self):
        self.__cmd('next')

    def run(self):
        self.__cmd('cont')

    def restart(self):
        self.__cmd('R')
    
if __name__ == '__main__':
    db = BashDb('./test.sh')
    db.step() 
    db.step() 
    db.step()
    db.step() 
    db.step() 
    db.step()
    db.step() 
    db.step() 
    db.step()

    #db.addVarToWatch("var1")
    #db.addVarToWatch("var2")
    #db.__updateWatchList()
    #print db.getWatchList()
  #  db.step()
  #  db.step()
  #  db.step()
  #  db.restart()
  #  db.step()
  #  db.step()
  #  db.step()
  #  db.step()
  #  db.quit()


