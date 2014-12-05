#! /usr/bin/env python

from Tkinter import *
import tkFont

class SourceCodeBox(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.pack(expand = 1, fill = BOTH)
        
        self.prev_pos = 0
        self.Vsb = Scrollbar(self, orient="vertical", command=self.onVsb)
        self.Vsb.pack(side = RIGHT, fill = Y)       
        
        self.code = Listbox(self, disabledforeground='black', yscrollcommand=self.Vsb.set)
        self.linePtr = Listbox(self, width = 2, disabledforeground = 'black', yscrollcommand=self.Vsb.set )
        self.brPtr = Listbox(self, width = 2, relief = RAISED, bg = 'gray', selectbackground = 'red', 
                             selectmode = MULTIPLE, yscrollcommand = self.Vsb.set)
        
        self.brPtr.pack(side = LEFT, fill = Y)
        self.linePtr.pack(side = LEFT, fill = Y)
        self.code.pack(side = LEFT, fill = BOTH, expand = 1)
        
        self.code.bind("<Button-4>", self.onMouseWheel)
        self.linePtr.bind("<Button-4>", self.onMouseWheel)
        self.brPtr.bind("<Button-4>", self.onMouseWheel)
        
        self.code.bind("<Button-5>", self.onMouseWheel)
        self.linePtr.bind("<Button-5>", self.onMouseWheel)
        self.brPtr.bind("<Button-5>", self.onMouseWheel)

    def moveLinePtr(self, pos):
        self.linePtr.config(state = NORMAL)
        self.linePtr.delete(self.prev_pos)
        self.linePtr.insert(pos - 1, "=>")
        self.prev_pos = pos - 1
        self.linePtr.config(state = DISABLED)

    def insertLine(self, line):
        self.code.config(state = NORMAL) 
        self.code.insert(END, line)
        self.brPtr.insert(END, "  ")
        self.linePtr.insert(END, "  ")
        self.code.config(state = DISABLED)
  
    def onMouseWheel(self, event):
        if event.num == 4:
            d = -1
        elif event.num == 5:
            d = 1 
        
        self.linePtr.yview("scroll", d, "units")
        self.code.yview("scroll", d, "units")
        self.brPtr.yview("scroll", d, "units")
        return "break" 

    def onVsb(self, *args):
        self.code.yview(*args)
        self.linePtr.yview(*args)
        self.brPtr.yview(*args)

if __name__ == "__main__":
    tk = Tk()
    codeBox = SourceCodeBox(tk)
    tk.mainloop()



