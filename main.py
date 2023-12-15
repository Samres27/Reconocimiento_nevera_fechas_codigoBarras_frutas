from deteccion_barras import scanner_barras
from reconocerFecha import fechasOCR
from ObjectDetect import *

from customtkinter  import CTk, CTkFrame, CTkEntry, CTkLabel,CTkButton,CTkCheckBox
from tkinter import PhotoImage

root = CTk() 
root.geometry("500x600+350+20")
root.minsize(480,500)
root.config(bg ='#010101')
root.title("Reconocimiento ")

frame = CTkFrame(root, fg_color='#010101')
frame.grid(column=0, row = 0, sticky='nsew',padx=50, pady =50)

frame.columnconfigure([0,1], weight=1)
frame.rowconfigure([0,1,2,3,4,5], weight=1)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


#logo = PhotoImage(file='images/logo.png') 

def llamada1():
    #print("me llamaste papi")
    scanner_barras()


def llamada2():
    #print("me llamaste mami")
    fechasOCR()

def llamada3():
    video()



bt_Barras= CTkButton(frame, font = ('sans serif',12), border_color='#2cb67d', fg_color='#010101',
	hover_color='#2cb67d',corner_radius=12,border_width=2,
    text='ESCANEAR COD. BARRAS', width=200, height=100,command=llamada1)
bt_Barras.grid(columnspan=2, row=1,padx=4, pady =4,)

bt_Fechas= CTkButton(frame, font = ('sans serif',12), border_color='#2cb67d', fg_color='#010101',
	hover_color='#2cb67d',corner_radius=12,border_width=2,
    text='ESCANEAR FECHA VEN.', width=200, height=100,command=llamada2)
bt_Fechas.grid(columnspan=2, row=2,padx=4, pady =4,)

bt_Fechas= CTkButton(frame, font = ('sans serif',12), border_color='#2cb67d', fg_color='#010101',
	hover_color='#2cb67d',corner_radius=12,border_width=2,
    text='ESCANEAR FRUTAS.', width=200, height=100,command=llamada3)
bt_Fechas.grid(columnspan=2, row=3,padx=4, pady =4,)


#root.call('wm', 'iconphoto', root._w, '-default')#, logo)
root.mainloop()
