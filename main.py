from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
# from itinerario import Itinerario

from PIL import Image, ImageTk
from pprint import pprint
import json
import sqlite3

from tkcalendar import DateEntry
from datetime import date
from datetime import datetime
from operator import itemgetter

import tkintermapview

class Detalles_evento(Toplevel):
	def __init__(self, id, lista):
		super(Detalles_evento, self).__init__()
		self.resizable(False,False)
		self.title("Detalles del evento")
		main_frame = ttk.Frame(self)
		self.id = id
		print(self.id)
		self.lista = lista
		
		# print(self.id)
		# pprint(self.lista)
		for i in lista:
			if i[0] == int(self.id[0]):
				self.nombre = i[1]
				self.artista = i[2]
				self.ubicacion = i[4]
				self.fecha = i[5]
				
		texto = [
				 'Nombre del evento : ', self.nombre, '\n'
				 'Nombre del artista: ', self.artista, '\n'
				 'Ubicacion del evento: ', str(self.ubicacion), '\n'
				 'Fecha del evento: ', self.fecha, '\n'
				 ]
		texto = ' '.join(texto)
		
		presentacion = ttk.Label(main_frame, text = texto)
		presentacion.grid(row = 0, column = 0, sticky = 'w',**padding)
		
		label_comentario = ttk.Label(main_frame, text = '¡Escribe tu comentario!')
		label_comentario.grid(row = 1, column = 0, sticky = 'w', **padding)
		
		self.comentario = scrolledtext.ScrolledText(main_frame, 
													font = 'segoeUI',
													width=20, 
													height=5,
													)
		self.comentario.grid(row = 2, column = 0,**padding, sticky = 'ew')
		
		min_frame = ttk.Frame(main_frame)
		btn_publicar = ttk.Button(min_frame, text = 'Publicar', command = self.publicar)
		btn_publicar.grid(row = 0, column = 0, **padding)
		
		self.var_star = StringVar()
		cbox_star = ttk.Combobox(min_frame,
								 textvariable = self.var_star,
								 state = 'readonly',
								 values = ('♥','♥♥','♥♥♥','♥♥♥♥','♥♥♥♥♥'))
		cbox_star.grid(row = 0, column = 1, **padding)
		
		min_frame.grid(row = 3, column = 0, **padding)
		
		chk_spoilers = ttk.Checkbutton(main_frame, text = 'Contiene spoilers')
		chk_spoilers.grid(row = 4, column = 0, sticky = 'w', **padding)
		main_frame.pack()
		self.mainloop()
	
	def publicar(self):
		global usuario
		global id_usuario
		
		if usuario == 'indefinido':
			messagebox.showwarning('Advertencia', 'Inicie sesion para comentar')
			return
		else:
			id_ = int(self.id[0])
			# print(self.comentario.get('1.0','end'))
			cursor.execute('INSERT INTO review(id_evento, id_usuario, calificacion, comentario) VALUES (?,?,?,?)',
						   (id_, id_usuario,str(self.comentario.get('1.0','end')) ,self.var_star.get()))
			connection.commit()

class Ver_itinerario(Toplevel):
	def __init__(self):
		global usuario
		global id_usuario
		super(Ver_itinerario, self).__init__()
		if usuario == 'indefinido':
			self.destroy()
			messagebox.showwarning('Advertencia', 'Inicie sesion para ver su itinerario')
			return
		else:
			self.mostrar_itinerario()
	
	def mostrar_itinerario(self):
		self.resizable(False, False)
		self.itinerario = cursor.execute('SELECT id_evento FROM ruta WHERE id_usuario = ?', (id_usuario,)).fetchall()
		# print(self.itinerario)
		
		self.tabla_itinerario = ttk.Treeview(self)
		self.tabla_itinerario['columns'] = ('evento','artista', 'genero')
		self.tabla_itinerario.column('#0', width = 0, stretch = NO)
		self.tabla_itinerario.column('evento' )
		self.tabla_itinerario.column('artista' )
		self.tabla_itinerario.column('genero' )
		
		self.tabla_itinerario.heading('evento', text = 'Eventos')
		self.tabla_itinerario.heading('artista', text = 'artista')
		self.tabla_itinerario.heading('genero', text = 'género')
		
		for i in self.itinerario:
			evento = cursor.execute('SELECT nombre, artista, genero FROM evento WHERE id = ?', i).fetchone()
			self.tabla_itinerario.insert('', END, values = (
															evento[0],
															evento[1],
															evento[2]
															))
			
			# print(evento)
		self.tabla_itinerario.pack()
		
		
			

connection = sqlite3.Connection('database.db') #conexion con la base de datos
cursor = connection.cursor()

usuario = "indefinido"
id_usuario = int(12)

root = Tk()
root.minsize( width = 850, height = 450,)
style = ttk.Style(root)
# print(style.theme_names())
style.theme_use("clam")

# style.configure('TButton',background = 'grey', foreground = 'black', font = '10',focuscolor = 'none', border = 'none')
# style.configure('title.TLabel', font = 'segoeUI 15')
# font1 = font.Font(family ='segoeUI', size = 10)
# style.configure('.', 
				# focuscolor = 'none', 
				# background = '#33393b',
				# foreground = '#ffffff')
# style.configure('TNotebook.Tab', foreground = 'black')
# style.map('TNotebook.Tab',
		   # background = [('selected', 'red'),
						 # ('active', 'blue'),
						 # ('!disabled', 'yellow'),
						 # ],)

# style.map('TButton', 
		  # background = [('active', 'red')])

def foo():
	print(root.winfo_geometry())

# -------- barra de menú --------
root.option_add('*tearOff', FALSE)

menubar = Menu(root)
root['menu'] = menubar

# menu opciones 
# menu_opciones = Menu(menubar)
menubar.add_command(label = 'Iniciar sesión', command = lambda : inicio_sesion())
# menubar.add_command(label = 'Ajustes', command = lambda : Ajustes())
menubar.add_command(label = 'Ver itinerario', command = lambda : Ver_itinerario())

# menubar.add_cascade(menu = menu_opciones, label = 'Opciones')
# --------------------------------


# Esto es para agregarle padding a los widgets, 
# se lo agregamos usando el desempaquetado de
# diccionarios
padding = {'padx' : 5, 'pady' : 5}

###############################
# declaramos el frame principal
###############################
main_frame = ttk.Frame(root)

main_frame.columnconfigure(1, weight = 1)
main_frame.rowconfigure(1, weight = 1)

main_frame.grid(row = 0, column = 0, sticky = 'nsew')



################################
# declaramos el frame del titulo
################################

Hoy = date.today()

titulo_1 = ttk.Label(main_frame, 
					 text = 'MELODYHUB \nPowered by EvilGeniuses',
					 justify = 'left',
					 style = 'title.TLabel')
titulo_1.grid(row = 0,column = 0, sticky = 'w',columnspan = 2, **padding)


diasDeLaSemana = {0 : 'Lunes',
				  1 : 'Martes',
				  2 : 'Miercoles',
				  3 : 'Jueves',
				  4 : 'Viernes',
				  5 : 'Sábado',
				  6 : 'Domingo'}

mesDelAnio = {1 : 'Enero',
			  2 : 'Febrero',
			  3 : 'Marzo',
			  4 : 'Abril',
			  5 : 'Mayo',
			  6 : 'Junio',
			  7 : 'Julio',
			  8 : 'Agosto',
			  9 : 'Septiembre',
			  10 : 'Octubre',
			  11 : 'Noviembre',
			  12 : 'Diciembre'}

titulo_2 = ttk.Label(main_frame, 
					 text = "{}, {} de {} del {} \n Tartagal, Salta".format(diasDeLaSemana.get(Hoy.weekday()), 
																			Hoy.day, 
																			mesDelAnio.get(Hoy.month), 
																			Hoy.year),
					 justify = 'right',
					 style = 'title.TLabel')
					 

titulo_2.grid(row = 0, column = 1, sticky = 'e', **padding)

class Ajustes(Toplevel):
	def __init__(self):
		super(Ajustes, self).__init__()
		
		self.btn_modo_oscuro = ttk.Button(self, text = 'modo oscuro', command = self.darkmode)
		self.btn_modo_oscuro.pack()
		self.mainloop()
	
	def darkmode(self):
		style.configure('.', background = 'black', foreground = 'white')

class registrar_usuario(Toplevel):
	def __init__(self):
		super(registrar_usuario, self).__init__()
		self.resizable(False, False)
		main_frame = ttk.Frame(self)
		label_nombre = ttk.Label(main_frame, text = 'Nombre')
		label_nombre.grid(row = 0, column = 0, sticky = 'e',**padding)
		
		self.var_nombre = StringVar()
		entry_nombre = ttk.Entry(main_frame, textvariable = self.var_nombre)
		entry_nombre.grid(row = 0, column = 1,**padding)
		
		label_apellido = ttk.Label(main_frame, text = 'Contraseña')
		label_apellido.grid(row = 1, column = 0, sticky = 'e', **padding)
		
		self.var_contraseña = StringVar()
		entry_apellido = ttk.Entry(main_frame, textvariable = self.var_contraseña, show = '♫')
		entry_apellido.grid(row = 1, column = 1, **padding)
		
		btn_registratse = ttk.Button(main_frame, text = 'Registrarse', command = lambda: self.registro_usuario())
		btn_registratse.grid(row = 2, column = 0, columnspan = 2, sticky = 'ew', **padding)
		main_frame.pack()
	
	def registro_usuario(self):
		
		
		cursor.execute("INSERT INTO usuario(nombre, contraseña) VALUES (?,?)", (self.var_nombre.get(),self.var_contraseña.get()))
		connection.commit()
		messagebox.showinfo('Registro exitoso', 'El registro se completo con éxito ')
		self.destroy()
		return

class inicio_sesion(Toplevel):
	def __init__(self):
		super(inicio_sesion, self).__init__()
		self.resizable(False,False)
		main_frame = ttk.Frame(self)
		label_usuario = ttk.Label(main_frame, text = 'Usuario: ')
		label_usuario.grid(row = 0, column = 0, sticky = 'e', **padding)
		
		self.var_usuario = StringVar()
		entry_usuario = ttk.Entry(main_frame, textvariable= self.var_usuario)
		entry_usuario.grid(row = 0, column = 1, **padding)
		
		label_contraseña = ttk.Label(main_frame, text = 'Contraseña:  ')
		label_contraseña.grid(row = 1, column = 0,sticky = 'e', **padding)
		
		self.var_contraseña = StringVar()
		entry_contraseña = ttk.Entry(main_frame, textvariable = self.var_contraseña, show = '♫')
		entry_contraseña.grid(row = 1, column = 1, **padding)
		
		btn_iniciar_sesion = ttk.Button(main_frame, text = 'Iniciar sesión', command = lambda : self.iniciar_sesion())
		btn_iniciar_sesion.grid(row = 2, column = 0, columnspan = 2, sticky = 'ew', **padding)
		
		label_nuevo_usuario = ttk.Label(main_frame, text = '¿Nuevo usuario?')
		label_nuevo_usuario.grid(row = 3, column = 0, columnspan = 2, sticky = 'w', **padding)
		
		btn_registrar = ttk.Button(main_frame, text = 'Registrarse', command = lambda : registrar_usuario())
		btn_registrar.grid(row = 4, column = 0, columnspan = 2, sticky = 'ew', **padding)
		main_frame.pack()
		
		self.mainloop()
	
	def iniciar_sesion(self):
		global usuario
		global id_usuario
		cons_usuario = cursor.execute("SELECT * FROM usuario WHERE contraseña = ? AND nombre = ?",(self.var_contraseña.get(),self.var_usuario.get())).fetchone()
		if cons_usuario == None:
			messagebox.showwarning('Advertencia', 'Usuario y/o contraseña invalidos')
			return
		else:
			print(cons_usuario)
			id_usuario = cons_usuario[0]
			usuario = cons_usuario[1]
			messagebox.showinfo('Bienvenido', 'Inicio de sesión exitoso')
		
		self.destroy()


class Frame_busqueda(ttk.Frame):
	def __init__(self):
		super(Frame_busqueda, self).__init__()
		self.lista_eventos = []
		self.reversa = [False, False, False, False, False]
		self.var_entry_busqueda = StringVar()
		entry_busqueda = ttk.Entry(self, textvariable = self.var_entry_busqueda)
		entry_busqueda.grid(row = 0,
							column = 0,
							sticky = 'nsew',
							
							columnspan = 2,
							**padding
							)
		
		self.image_busqueda = Image.open('imagenes\\basic_magnifier.png')
		self.resize = (self.image_busqueda.size[0]//3, self.image_busqueda.size[1]//3)
		self.image_busqueda.thumbnail(self.resize)
		self.img = ImageTk.PhotoImage(self.image_busqueda)
		
		btn_busqueda = ttk.Button(self,image = self.img,compound = 'left', text = 'Buscar', command = self.buscar)
		btn_busqueda.grid(row = 1, column = 0,sticky = 'w' ,**padding)
		

		# miniframe para poner la botonera y 
		# mantener el comportamiento 
		frame_rb = ttk.Frame(self)

		self.var_tipo_busqueda = StringVar()
		self.var_tipo_busqueda.set('nombre')
		rb_nombre = ttk.Radiobutton(frame_rb,
									text = 'Buscar por evento',
									variable = self.var_tipo_busqueda,
									value = 'nombre')
		rb_nombre.grid(row = 1, column = 0, **padding)
		
		rb_artista = ttk.Radiobutton(frame_rb, 
									text = 'Buscar por artista',
									variable = self.var_tipo_busqueda,
									value = 'artista')
		rb_artista.grid(row = 1, column = 1, **padding)
		
		# rb_album = ttk.Radiobutton(frame_rb,
								# text = 'Buscar por álbum',
								# variable = self.var_tipo_busqueda,
								# value = 'album')
		# rb_album.grid(row = 1, column = 2, **padding)
		
		rb_genero = ttk.Radiobutton(frame_rb,
									text = 'Buscar por género',
									variable = self.var_tipo_busqueda,
									value = 'genero')
		rb_genero.grid(row = 1, column = 3, **padding)
		
		frame_rb.grid(row = 2, column = 0, columnspan = 2, sticky = 'w')
		# -------- fin de la declaracion del frame --------
		# l_buscar_desde = ttk.Label(self, text = 'Buscar desde: ')
		# l_buscar_desde.grid(row = 1, column = 2, sticky = 'e')

		# self.date_buscar_desde = DateEntry(self,
									# state = 'readonly',
									# locale = 'es_ES',
									# date_pattern = 'dd/mm/yyyy')
		# self.date_buscar_desde.grid(row = 1, column = 3, sticky = 'w')

		# self.date_buscar_hasta = DateEntry(self, 
							  # state = 'readonly',
							  # locale = 'es_ES',
							  # date_pattern = 'dd/mm/yyyy')

		# self.date_buscar_hasta.grid(row = 2, column = 3, sticky = 'w')

		# l_buscar_hasta = ttk.Label(self, text = 'Buscar hasta: ')
		# l_buscar_hasta.grid(row = 2, column = 2, sticky = 'e')

		self.table_res = ttk.Treeview(self)
		self.table_res['columns'] = ('Nombre del evento',
								'Artista', 
								'Género',
								# 'Ubicación',
								'Fecha')

		self.table_res.column('#0', width=0, stretch=NO)
		self.table_res.column('Nombre del evento')
		self.table_res.column('Artista')
		self.table_res.column('Género')
		# self.table_res.column('Ubicación')
		self.table_res.column('Fecha')

		self.table_res.heading('Nombre del evento', text = 'Nombre del evento', command = lambda: self.ordenar_tabla('evento'))
		self.table_res.heading('Artista', text = 'Artista', command = lambda: self.ordenar_tabla('artista'))
		self.table_res.heading('Género', text = 'Género', command = lambda: self.ordenar_tabla('genero'))
		# self.table_res.heading('Ubicación', text = 'Ubicación', command = lambda: self.ordenar_tabla('ubicacion'))
		self.table_res.heading('Fecha', text = 'Fecha', command = lambda: self.ordenar_tabla('fecha'))

		self.table_res.grid(row = 3, 
					   column = 0,
					   columnspan = 4,
					   # rowspan = 2,
					   sticky = 'nsew',
					   padx = (5,0),
					   pady = (0,10))

		scroll = ttk.Scrollbar(self, orient = VERTICAL, command = self.table_res.yview)
		scroll.grid(row = 3,
					column = 4,
					# rowspan = 2,
					sticky = 'nsw',
					pady = (0,10))
		self.table_res['yscrollcommand'] = scroll.set

		btn_detalles = ttk.Button(self, text = 'detalles',command = lambda : Detalles_evento(self.table_res.selection(), self.lista_eventos))
		btn_detalles.grid(row = 4, column = 0, sticky = 'w', **padding)
		
		self.escribir_tabla()
		
		self.columnconfigure(3, weight = 1)
		self.rowconfigure(3, weight = 1)


	def buscar(self):
		
		criterio_de_busqueda = self.var_tipo_busqueda.get()
		
		
		
		if self.var_entry_busqueda.get() == '':
			self.escribir_tabla()
			# return
		else:
			self.table_res.delete(*self.table_res.get_children())
			self.lista_eventos = cursor.execute("SELECT * FROM evento;").fetchall()
			
			# breakpoint()
			if criterio_de_busqueda == 'nombre':
				for i in self.lista_eventos:
					# breakpoint()
					if self.var_entry_busqueda.get() in i[1]:
						self.table_res.insert('',END, i[0], values =(
																	 i[1],
																	 i[2],
																	 i[3],
																	 i[4],
																	 i[5],
																	 ))
			
			elif criterio_de_busqueda == 'artista':
				for i in self.lista_eventos:
					# breakpoint()
					if self.var_entry_busqueda.get() in i[2]:
						self.table_res.insert('',END, i[0], values =(
																	 i[1],
																	 i[2],
																	 i[3],
																	 i[4],
																	 i[5],
																	 ))
				
			elif criterio_de_busqueda == 'genero':
				for i in self.lista_eventos:
					# breakpoint()
					if self.var_entry_busqueda.get() in i[3]:
						self.table_res.insert('',END, i[0], values =(
																	 i[1],
																	 i[2],
																	 i[3],
																	 i[4],
																	 i[5],
																	 ))
		
		# print(self.date_buscar_desde.get())
		# print(self.date_buscar_hasta.get())
	
	
	def limpiar_tabla(self):
		self.table_res.delete(*self.table_res.get_children())
	
	def escribir_tabla(self):
		self.limpiar_tabla()
		
		self.lista_eventos = cursor.execute("SELECT * FROM evento;").fetchall()
		
		lista_transitoria = []
		
		# for evento in self.lista_eventos:
			
			
			# lista_transitoria.append()
		
		
		# breakpoint()
		for evento in self.lista_eventos:
			self.table_res.insert('',END, int(evento[0]), values = (evento[1],
															   evento[2],
															   evento[3],
															   # evento[4],
															   evento[5]))
		# pprint(self.lista_eventos)
		
		# print('hola')
		
	
	def ordenar_tabla(self,criterio):
		# print(usuario)
		lista_transitoria = []
		# print(usuario)
		# print(id_usuario)
		for i in self.table_res.get_children():
			# fecha = 
			lista_transitoria.append([i, *self.table_res.item(i)['values']])
	
		# breakpoint()
		# pprint(lista_transitoria)
		
		if criterio == 'evento':
			lista_transitoria.sort(key = itemgetter(1), reverse = self.reversa[0])
			if self.reversa[0] == False :
				self.reversa[0] = True
			else:
				self.reversa[0] = False
			
		elif criterio == 'artista':
			lista_transitoria.sort(key = itemgetter(2), reverse = self.reversa[1] )
			if self.reversa[1] == False :
				self.reversa[1] = True
			else:
				self.reversa[1] = False
			
		elif criterio == 'genero':
			lista_transitoria.sort(key = itemgetter(3), reverse = self.reversa[2])
			if self.reversa[2] == False :
				self.reversa[2] = True
			else:
				self.reversa[2] = False
				
		
		elif criterio == 'fecha':
			lista_transitoria2 = []
			for i in lista_transitoria:
				# print(i[0:4])
				# print(i[5])
				lista_transitoria2.append([*i[0:4], date(int(i[-1].split('/')[2]),
														int(i[-1].split('/')[1]),
														int(i[-1].split('/')[0]))])
				lista_transitoria2.sort(key = itemgetter(4), reverse = self.reversa[4])
			# pprint(lista_transitoria)
			lista_transitoria.clear()
			# pprint(lista_transitoria2)
			for i in lista_transitoria2:
				# print(lista_transitoria)
				lista_transitoria.append([*i[0:4], '/'.join([str(i[-1].day),
															 str(i[-1].month),
															 str(i[-1].year),])])
			

			
			# pprint(lista_transitoria2)
			# lista_transitoria.sort(key = itemgetter(4), reverse = self.reversa[4])
			if self.reversa[4] == False :
				self.reversa[4] = True
			else:
				self.reversa[4] = False
		
		self.limpiar_tabla()
		
		for i in lista_transitoria:
			self.table_res.insert('', END, i[0], values = (i[1],
														   i[2],
														   i[3],
														   i[4],
														   # i[5])
														   ))
		# pprint(lista_transitorias)
		
	
class Itinerario(ttk.Frame):
		
	def __init__(self):
		super(Itinerario, self).__init__()
		self.mapa = tkintermapview.TkinterMapView(self, corner_radius = 10)
		self.mapa.set_position(-24.198611, -65.290833)
		self.mapa.set_zoom(8)
		self.mapa.grid(row = 0,
		column = 2,
		rowspan = 4,
		sticky = 'nsew',
		**padding)
		self.itinerario = set()
		self.var_evento = StringVar()
		self.entry_evento = ttk.Entry(self, textvariable = self.var_evento)
		self.entry_evento.grid(row = 0, column = 0, sticky = 'new', **padding )		
		self.btn_buscar = ttk.Button(self, text = 'Buscar evento', command = self.buscar_evento)
		self.btn_buscar.grid(row = 1, column = 0, **padding, sticky = 'ew')
		
		
		self.lista_eventos = ttk.Treeview(self)
		self.lista_eventos['columns'] = ('Eventos')
		
		self.lista_eventos.column('#0', width = 0, stretch = NO)
		self.lista_eventos.column('Eventos')
		self.lista_eventos.heading('Eventos', text = 'Eventos')
		self.lista_eventos.grid(row = 2, column = 0, sticky = 'ns')
		self.lista_eventos.bind('<<TreeviewSelect>>',lambda x : self.item_seleccionado())
		
		scroll = ttk.Scrollbar(self, orient = VERTICAL, command = self.lista_eventos.yview)
		scroll.grid(row = 2,
					column = 1,
					# rowspan = 2,
					sticky = 'nsw',
					pady = (0,0))
		self.lista_eventos['yscrollcommand'] = scroll.set
		
		self.btn_agregar_evento = ttk.Button(self, text = 'Agregar evento', command = self.agregar_evento)
		self.btn_agregar_evento.grid(row = 3, column = 0, **padding)
		
		self.escribir_evento()
		
		self.lista_confirmados = ttk.Treeview(self)
		self.lista_confirmados.grid(row = 0,
									column = 3,
									columnspan = 2,
									rowspan = 3, 
									sticky = 'ns',
									**padding)
		self.lista_confirmados['columns'] = ('Itinerario')
		
		self.lista_confirmados.column('#0', width = 0, stretch = NO)
		self.lista_confirmados.column('Itinerario')
		self.lista_confirmados.heading('Itinerario', text = 'Itinerario')
		
		
		
		
		
		self.btn_borrar = ttk.Button(self, text = 'Borrar de la lista', command = self.borrar)
		self.btn_borrar.grid(row = 3, column = 3, **padding)
		
		self.btn_confirmar = ttk.Button(self, text = 'Confirmar', command = self.confirmar)
		self.btn_confirmar.grid(row = 3, column = 4, **padding)
		
		self.rowconfigure(2, weight = 1)
		self.columnconfigure(2, weight = 1)
	
	def confirmar(self):
		# cursor.execute("INSERT INTO usuario(nombre, contraseña) VALUES (?,?)", ())
		# print(self.lista_confirmados.get_children())
		
		global id_usuario
		for i in self.lista_confirmados.get_children():
			cursor.execute("INSERT INTO ruta (id_evento, id_usuario) VALUES (?,?)",
						   (i, id_usuario))
			connection.commit()
		
		self.lista_confirmados.delete(*self.lista_confirmados.get_children())
		messagebox.showinfo('Registro exitoso', 'El itinerario se cargo en la base de datos')
	
	def borrar(self):
		self.lista_confirmados.delete(*self.lista_confirmados.selection())
	
	def agregar_evento(self):
		global id_usuario
		evento = self.lista_eventos.selection()[0]
		if usuario == "indefinido":
			messagebox.showwarning('Advertencia', 'Debes iniciar sesion para guardar el itinerario')
		else:
			try:
				self.lista_confirmados.insert('', 
											END, 
											self.lista_eventos.selection()[0],
											values = self.lista_eventos.item(self.lista_eventos.selection())['values'])
			
				print(self.lista_eventos.item(self.lista_eventos.selection()))
			
			except:
				messagebox.showwarning('Advertencia', 'El evento ya esta en el itinerario')
			
			# cursor.execute("INSERT INTO ruta(id_evento, id_usuario) VALUES (?,?)", (evento, id_usuario))
			# connection.commit()
			# messagebox.showinfo('Registro completado', 'El registro de su evento fue exitoso')
	
	def item_seleccionado(self):
		# print(self.lista_eventos.selection()[0])
		selection = self.lista_eventos.selection()[0]
		# print(selection)
		Id_ubicacion = cursor.execute('SELECT id_ubicacion FROM evento WHERE id = ?', (int(selection),)).fetchone()
		str_ubicacion = cursor.execute('SELECT direccion FROM ubicacion WHERE id = ?', Id_ubicacion).fetchone()
		
		
		self.mapa.set_address(str_ubicacion[0])
		# print(Id_ubicacion)
		
		
	
	def limpiar_tabla(self):
		self.lista_eventos.delete(*self.lista_eventos.get_children())
	
	def escribir_evento(self):
		self.limpiar_tabla()
		a = cursor.execute("SELECT id, nombre FROM evento;").fetchall()
		# pprint(a)
		for i in a:
			self.lista_eventos.insert('', END, int(i[0]), values = ([i[1]]))
		
	def buscar_evento(self):
		evento = self.var_evento.get()
		
		lista = cursor.execute(("SELECT ID, nombre FROM evento WHERE nombre LIKE ?"),('%{}%'.format(evento),)).fetchall()
		# pprint(lista)
		if len(lista) == 0:
			messagebox.showwarning('Advertencia', 'No se encontro el evento')
			return
		else:
			self.limpiar_tabla()
			for evento in lista:
				self.lista_eventos.insert('', END, int(evento[0]), values = ([evento[1]]))
	
	def imprimir(self):
		print(self.var_lista_eventos.get())
		# print(id_usuario)

##################################
# declaramos el notebook principal
##################################

main_notebook = ttk.Notebook(main_frame)

main_notebook.grid(row = 1, column = 1,sticky = 'nsew', **padding)

# ---- Agregamos los frames al calendario ----
main_notebook.add(Frame_busqueda(), text = 'Buscar')
main_notebook.add(Itinerario(),text = 'Crear itinerario')
# --------------------------------------------

# definimos el sizegrip

size = ttk.Sizegrip(main_frame)
size.grid(row=2, column=1, padx=0, pady=0, sticky='se')

# ---------------------


# --------- configuramos los pesos relativos ---------
root.rowconfigure(0, weight = 1)
root.columnconfigure(0, weight = 1)
# ----------------------------------------------------
root.mainloop()