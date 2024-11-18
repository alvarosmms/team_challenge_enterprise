# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 23:47:00 2024

@author: juanmoreno
"""

# funciones.py
import random
from clases import Tablero
import tkinter as tk
from variables import *

def generar_coordenada_aleatoria():
    return random.randint(0, 9), random.randint(0, 9)

def mostrar_mensaje_bienvenida():
    print("¡Bienvenido al juego de Hundir la Flota! Intenta hundir todos los barcos enemigos.")

def verificar_fin_juego(jugador, maquina):
    if jugador.barcos_restantes == 0:
        print("¡Te acaba de ganar una máquina XD! Vuelve cuando quieras a intentarlo de nuevo ;-3")
        return True
    elif maquina.barcos_restantes == 0:
        print("Enhorabuena, ¡Has ganado! Esperamos que hayas disfrutado de nuestro juego, ¡vuelve pronto!")
        return True
    return False

def convertir_tablero_a_texto(tablero, visible=False):
    ###Convierte el tablero en texto para mostrarlo en la ventana.
    texto = []
    for fila in tablero.tablero:
        fila_texto = []
        for casilla in fila:
            if casilla == BARCO and not visible:
                fila_texto.append(" ")  # Ocultar barcos si no es visible
            elif casilla == IMPACTO:
                fila_texto.append("X")  # Impacto
            elif casilla == FALLO:
                fila_texto.append("O")  # Fallo
            else:
                fila_texto.append(casilla)
        texto.append(" | ".join(fila_texto))
    return "\n".join(texto)

### Modo facil
def juego_facil():
    ventana_juego = tk.Tk()
    ventana_juego.title("Hundir la flota - Fácil")
    ventana_juego.geometry("600x800")

    tablero_jugador = Tablero(id_jugador=1)
    tablero_maquina = Tablero(id_jugador=2)

    # Manejador de disparos
    def manejar_disparo():
        try:
            # Obtener las coordenadas ingresadas por el jugador
            x = int(entry_x.get())
            y = int(entry_y.get())

            # Verificar si las coordenadas son válidas
            if x < 0 or x >= DIMENSIONES_TABLERO or y < 0 or y >= DIMENSIONES_TABLERO:
                resultado["text"] = "Coordenadas fuera de rango. Inténtalo de nuevo."
                return  # Salir de la función sin disparar

            # Verificar si ya se disparó en esa coordenada
            if tablero_maquina.tablero[x, y] in [IMPACTO, FALLO]:
                resultado["text"] = f"Ya disparaste en ({x}, {y}). Intenta en otro lugar."
                return  # Salir de la función sin disparar

            # Realizar el disparo
            impacto, hundido = tablero_maquina.disparo(x, y)

            if impacto:
                resultado["text"] = f"¡Tocado en ({x}, {y})!"
                if hundido:
                    resultado["text"] += " ¡Barco hundido!"
            else:
                resultado["text"] = f"¡Agua en ({x}, {y})!"

            # Actualizar el tablero de la máquina tras el disparo del jugador
            mapa_maquina.config(text=convertir_tablero_a_texto(tablero_maquina, visible=False))

            # Verificar si el jugador ha ganado
            if tablero_maquina.barcos_restantes == 0:
                resultado["text"] = "¡Ganaste! Has hundido todos los barcos de la máquina."
                ventana_juego.after(2000, ventana_juego.quit)
                return  # Terminar el juego

            # Disparo de la máquina
            x_m, y_m, estado_maquina = tablero_jugador.disparo_maquina()
            if estado_maquina == "Tocado":
                resultado_maquina["text"] = f"La máquina disparó a ({x_m}, {y_m}) -> ¡Tocado!"
            elif estado_maquina == "Hundido":
                resultado_maquina["text"] = f"La máquina disparó a ({x_m}, {y_m}) -> ¡Barco hundido!"
            else:
                resultado_maquina["text"] = f"La máquina disparó a ({x_m}, {y_m}) -> ¡Agua!"

            # Actualizar el tablero del jugador tras el disparo de la máquina
            mapa_jugador.config(text=convertir_tablero_a_texto(tablero_jugador, visible=True))

            # Verificar si la máquina ha ganado
            if tablero_jugador.barcos_restantes == 0:
                resultado["text"] = "¡Perdiste! La máquina ha ganado."
                ventana_juego.after(2000, ventana_juego.quit)

        except ValueError:
            resultado["text"] = "Por favor, ingresa coordenadas válidas."

    # Interfaz de la ventana del juego
    etiqueta = tk.Label(ventana_juego, text="Introduce las coordenadas para disparar (x, y):")
    etiqueta.pack(pady=10)

    entry_x = tk.Entry(ventana_juego, width=5)
    entry_y = tk.Entry(ventana_juego, width=5)
    entry_x.pack(pady=5)
    entry_y.pack(pady=5)

    disparar_btn = tk.Button(ventana_juego, text="Disparar", command=manejar_disparo)
    disparar_btn.pack(pady=10)

    resultado = tk.Label(ventana_juego, text="")
    resultado.pack(pady=5)

    resultado_maquina = tk.Label(ventana_juego, text="")
    resultado_maquina.pack(pady=5)

    # Etiquetas para mostrar los tableros de los jugadores
    mapa_jugador = tk.Label(ventana_juego, text=convertir_tablero_a_texto(tablero_jugador, visible=True),
                            font=("Courier", 12))
    mapa_jugador.pack(pady=10)

    mapa_maquina = tk.Label(ventana_juego, text=convertir_tablero_a_texto(tablero_maquina, visible=False),
                            font=("Courier", 12))
    mapa_maquina.pack(pady=10)

    ventana_juego.mainloop()