from tkinter import *
from tkinter import ttk


class historial(ttk.Frame):
	def __init__(self, *arg):
		super(historial, self).__init__()
		self.etiqueta = ttk.Label(root, text = 'hola mundo')
		self.etiqueta.pack()


if __name__ == '__main__':
	root = Tk()
	
	frame = historial(root)
	frame.pack()
	
	root.mainloop()