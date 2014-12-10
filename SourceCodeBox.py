#! /usr/bin/env python

from Tkinter import *
import tkFont

class SourceCodeBox(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        
        self.pack(expand = 1, fill = BOTH)
        
        self.prev_pos = 0
        
        self.brSelectCb = None

        self.Vsb = Scrollbar(self, orient="vertical", command=self.onVsb)
        self.Vsb.pack(side = RIGHT, fill = Y)       
        
        self.code = Listbox(self, yscrollcommand=self.Vsb.set, exportselection = False,selectbackground = 'PaleGreen1')
        self.brPtr = Listbox(self, width = 2, relief = RAISED, bg = 'gray', selectbackground = 'red', 
                             selectmode = MULTIPLE, yscrollcommand = self.Vsb.set)
        
        self.brPtr.pack(side = LEFT, fill = Y)
        self.code.pack(side = LEFT, fill = BOTH, expand = 1)
        
        self.code.bind("<Button-4>", self.onMouseWheel)
        self.brPtr.bind("<Button-4>", self.onMouseWheel)
        
        self.code.bind("<Button-5>", self.onMouseWheel)
        self.brPtr.bind("<Button-5>", self.onMouseWheel)

        self.code.bind("<Button-1>", self.noop)
        self.code.bind("<B1-Motion>", self.noop)
        
        self.brPtr.bind("<Button-1>", self.onItemClick)
    
    def setFont(self, userFont):
        self.code.config(font = userFont)
        self.brPtr.config(font = userFont)
    
    def setBrCb(self, func):
        self.brSelectCb = func

    def noop(self, *args):
        return "break"

    def moveLinePtr(self, pos):
        self.code.selection_clear(self.prev_pos, None)
        self.code.selection_set(pos - 1, None)
        self.prev_pos = pos - 1

    def insertLine(self, line):
        self.code.insert(END, line)
        self.brPtr.insert(END, " ")
  
    def onMouseWheel(self, event):
        if event.num == 4:
            d = -1
        elif event.num == 5:
            d = 1 
        
        self.code.yview("scroll", d, "units")
        self.brPtr.yview("scroll", d, "units")
        return "break" 

    def onVsb(self, *args):
        self.brPtr.yview(*args)
        self.code.yview(*args)

    def onItemClick(self, event):
        nearestItem = self.brPtr.nearest(event.y)
        if self.brPtr.select_includes(nearestItem):
            self.brPtr.select_set(nearestItem)
        else:
            self.brPtr.select_clear(nearestItem)
        self.brSelectCb(nearestItem)

if __name__ == "__main__":
    tk = Tk()
    codeBox = SourceCodeBox(tk)
    tk.mainloop()



