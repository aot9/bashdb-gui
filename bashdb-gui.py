#! /usr/bin/env python

from Debug import BashDb
from View import View

db   = BashDb('./test.sh')
view = View(db)
view.geometry('640x480')
view.mainloop()
