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
        self.curSrcFile = None
        
        self.Bl = Bl
         
        self.Font = tkFont.Font(family="Monospace", size=12)

        self.ButtonFrame = Frame(self)
        self.ButtonFrame.pack(side=TOP, fill=X)
        btnPackOpt = {'side': LEFT, 'fill': X}

        Button(self.ButtonFrame, text="Step Into",
               command=lambda: self.__cmd_cb(self.Bl.step)).pack(btnPackOpt)
        Button(self.ButtonFrame, text="Step Over",
               command=lambda: self.__cmd_cb(self.Bl.next)).pack(btnPackOpt)
        Button(self.ButtonFrame, text="Go",
               command=lambda: self.__cmd_cb(self.Bl.run)).pack(btnPackOpt)
        Button(self.ButtonFrame, text="Restart",
               command=lambda: self.__cmd_cb(self.Bl.restart)).pack(btnPackOpt)
        
        self.pw = PanedWindow(self, orient=VERTICAL)
        self.pw.pack(side=TOP, fill=BOTH, expand=1)

        self.tabFrame = LabelFrame(self.pw, text="Listing", padx=5, pady=5)
        self.tabView = ttk.Notebook(self.tabFrame)
        self.tabView.pack(fill=BOTH, expand=1)
        self.pw.add(self.tabFrame)
        
        self.hpw = PanedWindow(self.pw, orient=HORIZONTAL)
        self.pw.add(self.hpw)

        self.outputFrame = LabelFrame(self.hpw, text="Stdout", padx=5, pady=5)
        self.outputBox = Text(self.outputFrame)
        self.outputBox.pack(fill=BOTH, expand=1)
        
        self.dataFrame = LabelFrame(self.hpw, text="Watch List", padx=5, pady=5)
        self.dataBtnFrame = Frame(self.dataFrame)
        self.dataBtnFrame.pack(side=TOP, fill=X)
        self.addVarBtn = Button(self.dataBtnFrame, text="Add", command=lambda: self.__dataEntry_cb(self.Bl.addVarToWatch))
        self.addVarBtn.pack(side=LEFT, fill=X)
        self.remVarBtn = Button(self.dataBtnFrame, text="Del", command=lambda: self.__dataEntry_cb(self.Bl.remVarFromWatch))
        self.remVarBtn.pack(side=LEFT, fill=X)
        self.dataEntry = Entry (self.dataBtnFrame)
        self.dataEntry.pack(side=LEFT, fill=X, expand=1)
        self.dataBox = Text(self.dataFrame)
        self.dataBox.pack(side=BOTTOM, fill=BOTH, expand=1)
        
        self.hpw.add(self.outputFrame)
        self.hpw.add(self.dataFrame)
        
        self.__cmd_cb(None)
   
    def __dataEntry_cb(self, btnFunc):
        btnFunc(self.dataEntry.get())
        self.dataEntry.delete(0, END)
        self.updateDataBox()
        
    def __cmd_cb(self, func):
        if func:
            func()
        
        if self.curSrcFile != self.Bl.getCurSrcFile():
            if self.curSrcFile is not None:
                self.getActiveTab().selectionClear()
            self.curSrcFile = self.Bl.getCurSrcFile() 
            for tab_id in self.tabView.tabs():
                if self.tabView.tab(tab_id)["text"] == self.curSrcFile:
                    self.tabView.select(tab_id)
                    break
            else:    
                self.addNewTab()
       
        self.outputBox.insert(END, self.Bl.getAppOutput())
        self.getActiveTab().moveLinePtr(self.Bl.getCurCodeLine())
        self.updateDataBox()
    
    def getActiveTab(self):
        return self.tabView.__dict__['children'][self.tabView.select().rsplit('.', 1)[1]]

    def addNewTab(self):
        sourceCodeBox = SourceCodeBox(self.tabView)
        sourceCodeBox.setFont(self.Font)
        sourceCodeBox.setBrCb(self.Bl.br)
        
        self.tabView.add(sourceCodeBox, text=self.curSrcFile)
        self.tabView.select(self.tabView.tabs()[-1])
        self.fillSourceCodeBox(sourceCodeBox)

    def updateDataBox(self):
        self.dataBox.delete(1.0, END)
        for line in self.Bl.getWatchList():
            self.dataBox.insert(END, line + '\n')

    def fillSourceCodeBox(self, codeBox):
        srcCode = self.Bl.readSourceCode() 
        for n, line in zip(xrange(1, len(srcCode) + 1), srcCode):
            codeBox.insertLine(" " + str(n) + " "*(6-len(str(n))) + line.strip())

if __name__ == '__main__':
    view = View(None)
    view.geometry('640x480')
    view.mainloop()