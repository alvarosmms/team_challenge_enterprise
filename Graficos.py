import tkinter as tk
import random as ran

# Tamaño del tablero
TAMANIO_TABLERO = 10

# Crear el tablero vacío
def crear_tablero():
    return [[" " for _ in range(TAMANIO_TABLERO)] for _ in range(TAMANIO_TABLERO)]

# Función para colocar los barcos aleatoriamente en el tablero
def colocar_barcos(tablero):
    # Barcos: 1 barco de 4 casillas, 2 barcos de 3 casillas y 3 barcos de 2 casillas
    barcos = [(4, 1), (3, 2), (2, 3)]  # (tamaño del barco, cantidad)

    for tamano, cantidad in barcos:
        for _ in range(cantidad):
            colocado = False
            while not colocado:
                # Elegir dirección aleatoria: horizontal o vertical
                direccion = ran.choice(["horizontal", "vertical"])
                if direccion == "horizontal":
                    fila = ran.randint(0, TAMANIO_TABLERO - 1)
                    columna = ran.randint(0, TAMANIO_TABLERO - tamano)
                    # Verificar si el espacio está libre
                    if all(tablero[fila][columna + i] == " " for i in range(tamano)):
                        # Colocar el barco
                        for i in range(tamano):
                            tablero[fila][columna + i] = "B"
                        colocado = True
                else:
                    fila = ran.randint(0, TAMANIO_TABLERO - tamano)
                    columna = ran.randint(0, TAMANIO_TABLERO - 1)
                    # Verificar si el espacio está libre
                    if all(tablero[fila + i][columna] == " " for i in range(tamano)):
                        # Colocar el barco
                        for i in range(tamano):
                            tablero[fila + i][columna] = "B"
                        colocado = True

# Verificar si el disparo es válido
def disparo_valido(tablero, x, y):
    return 0 <= x < TAMANIO_TABLERO and 0 <= y < TAMANIO_TABLERO and tablero[x][y] != "X" and tablero[x][y] != "O"

# Disparo del jugador
def disparar(tablero, x, y):
    if disparo_valido(tablero, x, y):
        if tablero[x][y] == "B":
            tablero[x][y] = "X"  # Marca de disparo del jugador
            return "Tocado"
        else:
            tablero[x][y] = "O"  # Marca de disparo fallido
            return "Agua"
    return "Disparo inválido"

# Disparo aleatorio de la máquina
def disparo_maquina(tablero):
    while True:
        x, y = ran.randint(0, TAMANIO_TABLERO - 1), ran.randint(0, TAMANIO_TABLERO - 1)
        if tablero[x][y] != "X" and tablero[x][y] != "O":  # Si la casilla no está marcada
            if tablero[x][y] == "B":
                tablero[x][y] = "O"  # Marca de disparo de la máquina
                return x, y, "Tocado"
            else:
                tablero[x][y] = "O"  # Marca de disparo fallido
                return x, y, "Agua"

# Verificar si un barco está hundido
def verificar_hundido(tablero, tamaño_barco):
    # Buscar barcos por tamaño
    for fila in range(TAMANIO_TABLERO):
        for columna in range(TAMANIO_TABLERO):
            if tablero[fila][columna] == "B":  # Barco
                # Comprobar horizontalmente
                if columna + tamaño_barco <= TAMANIO_TABLERO and all(tablero[fila][columna + i] == "X" for i in range(tamaño_barco)):
                    return True
                # Comprobar verticalmente
                if fila + tamaño_barco <= TAMANIO_TABLERO and all(tablero[fila + i][columna] == "X" for i in range(tamaño_barco)):
                    return True
    return False

# Verificar si quedan barcos
def quedan_barcos(tablero):
    for fila in range(TAMANIO_TABLERO):
        for columna in range(TAMANIO_TABLERO):
            if tablero[fila][columna] == "B":
                return True
    return False

# Convertir el tablero a texto para mostrarlo en el Label
def convertir_tablero_a_texto(tablero, es_maquina=False):
    """Convierte el tablero en texto para mostrarlo en la ventana.
    Si es la máquina, no muestra los barcos (B), solo los disparos (X y O)."""
    tablero_texto = []
    for fila in tablero:
        fila_texto = []
        for casilla in fila:
            if es_maquina and casilla == "B":
                fila_texto.append(" ")  # No mostrar los barcos de la máquina
            else:
                fila_texto.append(casilla)
        tablero_texto.append(" | ".join(fila_texto))
    return "\n".join(tablero_texto)

# Función principal del juego.
def juego_facil():
    ventana_juego = tk.Tk()
    ventana_juego.title("Hundir la flota - Fácil")
    ventana_juego.geometry("600x800")

    tablero_jugador = crear_tablero()
    tablero_maquina = crear_tablero()

    # Colocar barcos aleatorios
    colocar_barcos(tablero_jugador)
    colocar_barcos(tablero_maquina)

    # Manejador de disparos
    def manejar_disparo():
        try:
            x = int(entry_x.get())
            y = int(entry_y.get())
            if disparar(tablero_maquina, x, y) == "Tocado":
                resultado["text"] = f"¡Tocado en ({x}, {y})!"
            elif disparar(tablero_maquina, x, y) == "Agua":
                resultado["text"] = f"¡Agua en ({x}, {y})!"
            else:
                resultado["text"] = "Disparo inválido. Inténtalo de nuevo."

            # Verificar si la máquina ha hundido algún barco
            if verificar_hundido(tablero_maquina, 4):
                resultado_maquina["text"] = "¡Hundido! La máquina ha hundido un barco de 4."
            elif verificar_hundido(tablero_maquina, 3):
                resultado_maquina["text"] = "¡Hundido! La máquina ha hundido un barco de 3."
            elif verificar_hundido(tablero_maquina, 2):
                resultado_maquina["text"] = "¡Hundido! La máquina ha hundido un barco de 2."
            else:
                # Disparo de la máquina
                x_m, y_m, estado_maquina = disparo_maquina(tablero_jugador)
                resultado_maquina["text"] = f"La máquina disparó a ({x_m}, {y_m}) y {estado_maquina}"
                mapa_jugador.config(text=convertir_tablero_a_texto(tablero_jugador))

            # Actualizar tableros
            mapa_maquina.config(text=convertir_tablero_a_texto(tablero_maquina, es_maquina=True))
            mapa_jugador.config(text=convertir_tablero_a_texto(tablero_jugador))

            # Verificar si el juego ha terminado
            if not quedan_barcos(tablero_jugador):
                resultado["text"] = "¡Perdiste! La máquina ha ganado."
                ventana_juego.after(2000, ventana_juego.quit)
            elif not quedan_barcos(tablero_maquina):
                resultado["text"] = "¡Ganaste! Has hundido todos los barcos de la máquina."
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
    mapa_jugador = tk.Label(ventana_juego, text=convertir_tablero_a_texto(tablero_jugador), font=("Courier", 12))
    mapa_jugador.pack(pady=10)

    mapa_maquina = tk.Label(ventana_juego, text=convertir_tablero_a_texto(tablero_maquina, es_maquina=True),
                            font=("Courier", 12))
    mapa_maquina.pack(pady=10)

    ventana_juego.mainloop()

# Menú principal
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

#### Crear la ventana del menú inicial
ventana_inicio = tk.Tk()
ventana_inicio.title("Menú de inicio")
ventana_inicio.geometry("300x200")

texto_inicio = tk.Label(ventana_inicio, text="Hundir la flota", font=("Arial", 14), fg="red")
texto_inicio.pack(pady=20)

jugar = tk.Button(ventana_inicio, text="Jugar", command=abrir_nueva_ventana)
jugar.pack(pady=20)

ventana_inicio.mainloop()












