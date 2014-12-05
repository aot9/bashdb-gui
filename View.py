#! /usr/bin/env python

from Tkinter import *
import tkFont
import ttk

class View(Tk):
    def __init__(self, Bl):
        Tk.__init__(self)
        
        self.cur_line = None
        
        self.Bl = Bl

        self.Font = tkFont.Font(family="Monospace", size=11)        

        self.ButtonFrame = Frame(self)
        self.ButtonFrame.pack(side = TOP, fill = X, expand = 0)

        Button(self.ButtonFrame, text = "Step Into",    command = self.step_cb   ).pack(side = LEFT, fill = X, expand = 1)
        Button(self.ButtonFrame, text = "Step Over",    command = self.step_cb   ).pack(side = LEFT, fill = X, expand = 1)
        Button(self.ButtonFrame, text = "Go",     command = self.run_cb    ).pack(side = LEFT, fill = X, expand = 1)
        Button(self.ButtonFrame, text = "Restart", command = self.restart_cb).pack(side = LEFT, fill = X, expand = 1)
        Button(self.ButtonFrame, text = "Quit",    command = self.quit_cb   ).pack(side = LEFT, fill = X, expand = 1)

        self.pw = PanedWindow(self, orient = VERTICAL)
        self.pw.pack(side = TOP, fill = BOTH, expand = 1)

        self.tabView = ttk.Notebook(self.pw) 
        self.pw.add(self.tabView)
        
        self.sourceCodeBox = Listbox(self.pw, font = self.Font, selectmode = BROWSE)
        self.tabView.add(self.sourceCodeBox, text = self.Bl.getCurSrcFile())

        self.fillSourceCodeBox()

        self.outputBox = Text(self.pw, font = self.Font)
        self.pw.add(self.outputBox)
        self.__cmd_cb(None)
    
    def __cmd_cb(self, func):
        if func:
            func()
        
        self.outputBox.insert(END, self.Bl.getAppOutput())

    def step_cb(self):
        self.__cmd_cb(self.Bl.step)

    def run_cb(self):
        self.__cmd_cb(self.Bl.run)

    def restart_cb(self):
        self.__cmd_cb(self.Bl.restart)

    def quit_cb(self):
        self.__cmd_cb(self.Bl.quit)

    def fillSourceCodeBox(self):
        for line in self.Bl.readSourceCode():
            self.sourceCodeBox.insert(END, "    " + line)

if __name__ == '__main__':
    view = View(None)
    view.geometry('640x480')
    view.mainloop()
            
