#! /usr/bin/env python

from Debug import BashDb
from View import View
import sys

db   = BashDb(" ".join(sys.argv[1:]))
view = View(db)
view.geometry('800x600')
view.mainloop()
