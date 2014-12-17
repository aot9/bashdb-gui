--------------------------------
bashdb-gui
================================
###Description###

This app is a bashdb(bash debugger) front end.

###Requirements###

- [bashdb](http://sourceforge.net/projects/bashdb/) 
- python 2.7 (not tested with other versions)
- tkinter (python graphic lib)
- ttk (Tkinter themed widgets)

###Usage###

$ bashdb-gui.py script.sh arg1 arg2 ..

###Bugs###

Breakpoints not always work correct. Script execution may not break.
This is bashdb bug, that should had been fixed with this [commit](http://sourceforge.net/p/bashdb/code/ci/21ba345b5ca1ad41244533170b9c3166c6e982fc/).
Bug affects all bashdb versions older than 4.3-0.91.
