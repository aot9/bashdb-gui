#! /usr/bin/env python

from Debug import BashDb
from View import View
import sys

db   = BashDb(sys.argv[1])
view = View(db)
view.geometry('640x480')
view.mainloop()
