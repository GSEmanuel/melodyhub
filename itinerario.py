from tkinter import StringVar
from tkinter import *
from tkinter import ttk
import sqlite3
from pprint import pprint

padding = {'padx' : 5, 'pady' : 5}

connection = sqlite3.Connection('database.db') #conexion con la base de datos
cursor = connection.cursor()

