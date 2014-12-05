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
        
        self.code = Listbox(self, yscrollcommand=self.Vsb.set, selectbackground = 'PaleGreen1')
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

    def noop(self, *args):
        return "break"

    def moveLinePtr(self, pos):
 #       self.code.config(state = NORMAL)
        self.code.selection_clear(self.prev_pos, None)
        self.code.selection_set(pos - 1, None)
        self.prev_pos = pos - 1
  #      self.code.config(state = DISABLED)

    def insertLine(self, line):
#        self.code.config(state = NORMAL) 
        self.code.insert(END, line)
        self.brPtr.insert(END, "  ")
#        self.code.config(state = DISABLED)
  
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

if __name__ == "__main__":
    tk = Tk()
    codeBox = SourceCodeBox(tk)
    tk.mainloop()



