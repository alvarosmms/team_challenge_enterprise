import tkinter as tk
from funciones import *
from clases import *
from variables import *


def abrir_nueva_ventana():
    ventana_inicio.destroy()
    ventana_menu = tk.Tk()
    ventana_menu.title("Menú del juego")
    ventana_menu.geometry("300x200")

    etiqueta = tk.Label(ventana_menu, text="Selecciona un modo de juego:", fg="black")
    etiqueta.pack(pady=20)

    facil = tk.Button(ventana_menu, text="Fácil", fg="green", command=juego_facil)
    facil.pack(pady=10)

    ventana_menu.mainloop()

# Crear la ventana del menú inicial
ventana_inicio = tk.Tk()
ventana_inicio.title("Menú de inicio")
ventana_inicio.geometry("300x200")

texto_inicio = tk.Label(ventana_inicio, text="Hundir la flota", font=("Arial", 14), fg="red")
texto_inicio.pack(pady=20)

jugar = tk.Button(ventana_inicio, text="Jugar", command=abrir_nueva_ventana)
jugar.pack(pady=20)

ventana_inicio.mainloop()