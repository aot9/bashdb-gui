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

        self.Font = tkFont.Font(family="Monospace", size=11)        

        self.ButtonFrame = Frame(self)
        self.ButtonFrame.pack(side = TOP, fill = X, expand = 0)

        Button(self.ButtonFrame, text = "Step Into",    command = self.step_cb   ).pack(side = LEFT, fill = X, expand = 1)
        Button(self.ButtonFrame, text = "Step Over",    command = self.next_cb   ).pack(side = LEFT, fill = X, expand = 1)
        Button(self.ButtonFrame, text = "Go",     command = self.run_cb    ).pack(side = LEFT, fill = X, expand = 1)
        Button(self.ButtonFrame, text = "Restart", command = self.restart_cb).pack(side = LEFT, fill = X, expand = 1)

        self.pw = PanedWindow(self, orient = VERTICAL)
        self.pw.pack(side = TOP, fill = BOTH, expand = 1)

        self.tabView = ttk.Notebook(self.pw) 
        self.pw.add(self.tabView)
        
        self.sourceCodeBox = SourceCodeBox(self.pw)
        self.tabView.add(self.sourceCodeBox, text = self.Bl.getCurSrcFile())

        self.fillSourceCodeBox()

        self.outputBox = Text(self.pw)
        self.pw.add(self.outputBox)
        self.__cmd_cb(None)
    
    def __cmd_cb(self, func):
        if func:
            func()
        
        self.outputBox.insert(END, self.Bl.getAppOutput())
        self.sourceCodeBox.moveLinePtr(self.Bl.getCurCodeLine())

    def step_cb(self):
        self.__cmd_cb(self.Bl.step)

    def run_cb(self):
        self.__cmd_cb(self.Bl.run)

    def restart_cb(self):
        self.__cmd_cb(self.Bl.restart)
    
    def next_cb(self):
        self.__cmd_cb(self.Bl.next)

    def quit_cb(self):
        self.__cmd_cb(self.Bl.quit)

    def fillSourceCodeBox(self):
        i = 1
        for line in self.Bl.readSourceCode():
            strnum = str(i)
            self.sourceCodeBox.insertLine(strnum + (" "*(5-len(strnum))) + line.strip())
            i = i + 1

if __name__ == '__main__':
    view = View(None)
    view.geometry('640x480')
    view.mainloop()
            
