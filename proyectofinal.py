import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# -------------------------
# FUNCIONES
# -------------------------
def abrir_registro_productos():
    messagebox.showinfo("Registro de Productos", "Aquí irá el módulo de registro de productos.")

def abrir_registro_ventas():
    messagebox.showinfo("Registro de Ventas", "Aquí irá el módulo de registro de ventas.")

def abrir_reportes():
    messagebox.showinfo("Reportes", "Aquí irá el módulo de reportes.")

def abrir_acerca_de():
    messagebox.showinfo("Acerca de", "Punto de Venta de Ropa\nProyecto Escolar\nVersión 1.0")


# -------------------------
# VENTANA PRINCIPAL
# -------------------------
ventana = tk.Tk()
ventana.title("Dulceria Tomy")
ventana.geometry("500x600")
ventana.resizable(False, False)

# Fondo naranja pastel
ventana.configure(bg="#FFD8A8")


# -------------------------
# LOGO
# -------------------------
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    imagen = Image.open(os.path.join(BASE_DIR, "ventas2025.png"))
    imagen = imagen.resize((250, 250))
    img_logo = ImageTk.PhotoImage(imagen)

    lbl_logo = tk.Label(ventana, image=img_logo, bg="#FFD8A8")
    lbl_logo.pack(pady=20)
except:
    lbl_sin_logo = tk.Label(
        ventana, 
        text="(Aquí va el logo del sistema)", 
        font=("Arial", 14),
        bg="#FFD8A8"
    )
    lbl_sin_logo.pack(pady=40)


# -------------------------
# FUNCIÓN PARA CREAR BOTONES
# -------------------------
def crear_boton(texto, comando):
    return tk.Button(
        ventana,
        text=texto,
        command=comando,
        font=("Arial", 12),
        bg="black",        # fondo negro
        fg="white",        # texto blanco
        activebackground="#333333",
        activeforeground="white",
        width=22,          # TODOS los botones del mismo ancho
        height=2,          # TODOS de la misma altura
    )


# -------------------------
# BOTONES (TODOS MISMO TAMAÑO)
# -------------------------
crear_boton("Registro de Productos", abrir_registro_productos).pack(pady=10)
crear_boton("Registro de Ventas", abrir_registro_ventas).pack(pady=10)
crear_boton("Reportes", abrir_reportes).pack(pady=10)
crear_boton("Acerca de", abrir_acerca_de).pack(pady=10)


ventana.mainloop()
