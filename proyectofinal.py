import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

# ==========================================
# REGISTRO DE PRODUCTOS
# ==========================================
def abrir_registro_productos():
    ven = tk.Toplevel()
    ven.title("Registro de Productos")
    ven.geometry("400x300")

    lbl_nombre = ttk.Label(ven, text="Nombre del Producto:", font=("Arial", 12))
    lbl_nombre.pack(pady=5)
    txt_nombre = ttk.Entry(ven, font=("Arial", 12))
    txt_nombre.pack(pady=5)

    lbl_precio = ttk.Label(ven, text="Precio:", font=("Arial", 12))
    lbl_precio.pack(pady=5)
    txt_precio = ttk.Entry(ven, font=("Arial", 12))
    txt_precio.pack(pady=5)

    def guardar_producto():
        nombre = txt_nombre.get()
        precio = txt_precio.get()

        if nombre == "" or precio == "":
            messagebox.showwarning("Campos Vacíos", "Todos los campos deben estar completos.")
            return

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivop = os.path.join(BASE_DIR, "productos.txt")

        with open(archivop, "a", encoding="utf-8") as archivo:
            archivo.write(f"{nombre}|{precio}\n")

        txt_nombre.delete(0, tk.END)
        txt_precio.delete(0, tk.END)

    btn_guardar = ttk.Button(ven, text="Guardar Producto", command=guardar_producto)
    btn_guardar.pack(pady=25)


# ==========================================
# REGISTRO DE VENTAS
# ==========================================
def abrir_registro_ventas():
    ven = tk.Toplevel()
    ven.title("Registrar Venta")
    ven.geometry("400x500")

    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivo = os.path.join(BASE_DIR, "productos.txt")
        with open(archivo, "r", encoding="utf-8") as archivo:
            productos = {}
            for linea in archivo:
                if linea.strip():
                    nombre, precio = linea.strip().split("|")
                    productos[nombre] = float(precio)
        lista_productos = list(productos.keys())
    except FileNotFoundError:
        messagebox.showerror("Error", "No existen productos registrados.")
        ven.destroy()
        return

    lbl_prod = ttk.Label(ven, text="Producto:", font=("Arial", 12))
    lbl_prod.pack(pady=5)
    cb_producto = ttk.Combobox(ven, values=lista_productos, font=("Arial", 12), state="readonly")
    cb_producto.pack(pady=5)

    lbl_precio = ttk.Label(ven, text="Precio:", font=("Arial", 12))
    lbl_precio.pack(pady=5)
    txt_precio = ttk.Entry(ven, font=("Arial", 12), state="readonly")
    txt_precio.pack(pady=5)

    lbl_cantidad = tk.Label(ven, text="Cantidad:", font=("Arial", 12))
    lbl_cantidad.pack(pady=5)
    cantidad_var = tk.StringVar(ven)
    txt_cantidad = ttk.Entry(ven, font=("Arial", 12), textvariable=cantidad_var)
    txt_cantidad.pack(pady=5)

    lbl_total = ttk.Label(ven, text="Total:", font=("Arial", 12))
    lbl_total.pack(pady=5)
    txt_total = ttk.Entry(ven, font=("Arial", 12), state="readonly")
    txt_total.pack(pady=5)

    def actualizar_precio(event):
        prod = cb_producto.get()
        if prod in productos:
            txt_precio.config(state="normal")
            txt_precio.delete(0, tk.END)
            txt_precio.insert(0, productos[prod])
            txt_precio.config(state="readonly")
            calcular_total()

    def calcular_total(*args):
        try:
            cant = int(txt_cantidad.get())
            precio = float(txt_precio.get())
            total = cant * precio
            txt_total.config(state="normal")
            txt_total.delete(0, tk.END)
            txt_total.insert(0, total)
            txt_total.config(state="readonly")
        except:
            txt_total.config(state="normal")
            txt_total.delete(0, tk.END)
            txt_total.config(state="readonly")

    cantidad_var.trace_add("write", lambda *args: calcular_total())

    def registrar_venta():
        prod = cb_producto.get()
        precio = txt_precio.get()
        cant = txt_cantidad.get()
        total = txt_total.get()

        if prod == "" or precio == "" or cant == "" or total == "":
            messagebox.showwarning("Campos Vacíos", "Todos los campos deben estar completos.")
            return

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivov = os.path.join(BASE_DIR, "ventas.txt")

        with open(archivov, "a", encoding="utf-8") as archivo:
            archivo.write(f"{prod}|{precio}|{cant}|{total}\n")

        cb_producto.set("")
        txt_precio.config(state="normal"); txt_precio.delete(0, tk.END); txt_precio.config(state="readonly")
        txt_cantidad.delete(0, tk.END)
        txt_total.config(state="normal"); txt_total.delete(0, tk.END); txt_total.config(state="readonly")

    cb_producto.bind("<<ComboboxSelected>>", actualizar_precio)

    btn_guardar = ttk.Button(ven, text="Registrar Venta", command=registrar_venta)
    btn_guardar.pack(pady=25)


# ==========================================
# REPORTES
# ==========================================
def abrir_reportes():
    ventana = tk.Toplevel()
    ventana.title("Reporte de Ventas")
    ventana.geometry("700x400")
    ventana.configure(bg="#f2f2f2")

    titulo = tk.Label(
        ventana,
        text="Reporte de Ventas Realizadas",
        font=("Arial", 16, "bold"),
        bg="#f2f2f2"
    )
    titulo.pack(pady=10)

    frame_tabla = ttk.Frame(ventana)
    frame_tabla.pack(pady=10)

    columnas = ("producto", "precio", "cantidad", "total")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)

    tabla.heading("producto", text="Producto")
    tabla.heading("precio", text="Precio")
    tabla.heading("cantidad", text="Cantidad")
    tabla.heading("total", text="Total")

    tabla.column("producto", width=250, anchor="center")
    tabla.column("precio", width=100, anchor="center")
    tabla.column("cantidad", width=100, anchor="center")
    tabla.column("total", width=120, anchor="center")
    tabla.pack()

    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivo = os.path.join(BASE_DIR, "ventas.txt")
        with open(archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                if linea.strip():
                    datos = linea.strip().split("|")
                    if len(datos) == 4:
                        tabla.insert("", tk.END, values=datos)
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo ventas.txt no existe.")
        ventana.destroy()


# ==========================================
# ACERCA DE
# ==========================================
def abrir_acerca_de():
    acerca = tk.Toplevel()
    acerca.title("Acerca de")
    acerca.geometry("250x200")
    acerca.resizable(False, False)

    lbl_id = tk.Label(acerca, text="Software Ventas 2025", font=("Arial", 14))
    lbl_id.pack(pady=5)

    lbl_creado = tk.Label(acerca, text="Creado por: Gera Aguilar", font=("Arial", 12))
    lbl_creado.pack(pady=5)

    lbl_grupo = tk.Label(acerca, text="Grupo: 3A Prog Vesp", font=("Arial", 12))
    lbl_grupo.pack(pady=5)


# ==========================================
# VENTANA PRINCIPAL
# ==========================================
ventana = tk.Tk()
ventana.title("Dulceria Tomy")
ventana.geometry("500x600")
ventana.resizable(False, False)
ventana.configure(bg="#FFD8A8")

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


def crear_boton(texto, comando):
    return tk.Button(
        ventana,
        text=texto,
        command=comando,
        font=("Arial", 12),
        width=22,
        height=2
    )

crear_boton("Registro de Productos", abrir_registro_productos).pack(pady=10)
crear_boton("Registro de Ventas", abrir_registro_ventas).pack(pady=10)
crear_boton("Reportes", abrir_reportes).pack(pady=10)
crear_boton("Acerca de", abrir_acerca_de).pack(pady=10)

ventana.mainloop()