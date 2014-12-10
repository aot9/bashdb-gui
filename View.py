#! /usr/bin/env python

from Tkinter import *
import tkFont
import ttk
from SourceCodeBox import SourceCodeBox

class View(Tk):
    def __init__(self, Bl):
        Tk.__init__(self)
        
        self.title("bashdb-gui")
        self.cur_line = None
        self.Bl = Bl
        self.curSrcFile = self.Bl.getCurSrcFile()

        self.Font = tkFont.Font(family = "Monospace", size = 12)        

        self.ButtonFrame = Frame(self)
        self.ButtonFrame.pack(side = TOP, fill = X)
        btnPackOpt = {'side' : LEFT, 'fill' : X}

        Button(self.ButtonFrame, text = "Step Into", command = lambda : self.__cmd_cb(self.Bl.step)   ).pack(btnPackOpt)
        Button(self.ButtonFrame, text = "Step Over", command = lambda : self.__cmd_cb(self.Bl.next)   ).pack(btnPackOpt)
        Button(self.ButtonFrame, text = "Go",        command = lambda : self.__cmd_cb(self.Bl.run)    ).pack(btnPackOpt)
        Button(self.ButtonFrame, text = "Restart",   command = lambda : self.__cmd_cb(self.Bl.restart)).pack(btnPackOpt)

        self.pw = PanedWindow(self, orient = VERTICAL)
        self.pw.pack(side = TOP, fill = BOTH, expand = 1)

        self.tabView = ttk.Notebook(self.pw) 
        self.pw.add(self.tabView)
        
        self.sourceCodeBox = SourceCodeBox(self.tabView)
        self.sourceCodeBox.setFont(self.Font)
        self.sourceCodeBox.setBrCb(self.Bl.br)

        self.tabView.add(self.sourceCodeBox, text = self.curSrcFile)
    
        self.fillSourceCodeBox()
        
        self.hpw = PanedWindow(self, orient = HORIZONTAL)
        
        self.pw.add(self.hpw)

        self.outputBox = Text(self.hpw, font = self.Font)
        
        self.dataFrame = Frame(self.hpw)
        self.dataBtnFrame = Frame(self.dataFrame)
        self.dataBtnFrame.pack(side = TOP, fill = X)
        self.dataEntry = Entry (self.dataBtnFrame)
        self.dataEntry.pack(side = LEFT, fill = X, expand = 1)
        self.addVarBtn = Button(self.dataBtnFrame,  text = "Add", command = lambda : self.__dataEntry_cb(self.Bl.addVarToWatch))
        self.addVarBtn.pack(side = LEFT, fill = X)
        self.remVarBtn = Button(self.dataBtnFrame,  text = "Remove", command = lambda : self.__dataEntry_cb(self.Bl.remVarFromWatch))
        self.remVarBtn.pack(side = LEFT, fill = X)
        self.dataBox = Text(self.dataFrame)
        self.dataBox.pack(side = BOTTOM, fill = BOTH, expand = 1)
        
        self.hpw.add(self.outputBox)
        self.hpw.add(self.dataFrame)
        
        self.__cmd_cb(None)
   
    def __dataEntry_cb(self, btnFunc):
        btnFunc(self.dataEntry.get())
        self.dataEntry.delete(0, END)
        self.updateDataBox()
        
    def __cmd_cb(self, func):
        if func:
            func()
        
        self.outputBox.insert(END, self.Bl.getAppOutput())
        self.sourceCodeBox.moveLinePtr(self.Bl.getCurCodeLine())
        self.updateDataBox()

        #self.updateCurSrcFile()

#    def updateCurSrcFile(self):
        

    def updateDataBox(self):
        self.dataBox.delete(1.0, END)
        for line in self.Bl.getWatchList():
            self.dataBox.insert(END, line + '\n')

    def fillSourceCodeBox(self):
        i = 1
        for line in  self.Bl.readSourceCode():
            self.sourceCodeBox.insertLine(" " + str(i) + " "*(6-len(str(i))) + line.strip())
            i = i + 1

if __name__ == '__main__':
    view = View(None)
    view.geometry('640x480')
    view.mainloop()
            
