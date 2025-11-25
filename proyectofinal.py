import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime

# ============================
# FUNCIONES
# ============================
def abrir_registro_productos():
    reg = ttk.Toplevel()
    reg.title("Registro de Productos")
    reg.geometry("400x400")
    reg.resizable(False, False)

    lbl_id = ttk.Label(reg, text="ID del Producto:", font=("Arial", 12))
    lbl_id.pack(pady=5)
    txt_id = ttk.Entry(reg, font=("Arial", 12))
    txt_id.pack(pady=5)

    lbl_desc = ttk.Label(reg, text="Descripción:", font=("Arial", 12))
    lbl_desc.pack(pady=5)
    txt_desc = ttk.Entry(reg, font=("Arial", 12))
    txt_desc.pack(pady=5)

    lbl_precio = ttk.Label(reg, text="Precio:", font=("Arial", 12))
    lbl_precio.pack(pady=5)
    txt_precio = ttk.Entry(reg, font=("Arial", 12))
    txt_precio.pack(pady=5)

    lbl_categoria = ttk.Label(reg, text="Categoría:", font=("Arial", 12))
    lbl_categoria.pack(pady=5)
    txt_categoria = ttk.Entry(reg, font=("Arial", 12))
    txt_categoria.pack(pady=5)

    def guardar_producto():
        id_prod = txt_id.get().strip()
        descripcion = txt_desc.get().strip()
        precio = txt_precio.get().strip()
        categoria = txt_categoria.get().strip()

        if id_prod == "" or descripcion == "" or precio == "" or categoria == "":
            messagebox.showwarning("Campos Vacíos", "Por favor complete todos los campos.")
            return
        
        try:
            float(precio)
        except:
            messagebox.showerror("Error", "El precio debe ser un número.")
            return

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivo = os.path.join(BASE_DIR, "productos.txt")

        with open(archivo, "a", encoding="utf-8") as archivo:
            archivo.write(f"{id_prod}|{descripcion}|{precio}|{categoria}\n")
            messagebox.showinfo("Guardado", "Producto registrado correctamente.")

            txt_id.delete(0, ttk.END)
            txt_desc.delete(0, ttk.END)
            txt_precio.delete(0, ttk.END)
            txt_categoria.delete(0, ttk.END)

    btn_guardar = ttk.Button(reg, text="Guardar Producto", command=guardar_producto)
    btn_guardar.pack(pady=20)


# ==========================================
# MOSTRAR TICKET
# ==========================================
def mostrar_ticket(producto, precio, cantidad, total):

    ticket = ttk.Toplevel()
    ticket.title("Ticket de Venta")
    ticket.geometry("300x450")
    ticket.resizable(False, False)

    fecha_hora = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")

    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        img = Image.open(os.path.join(BASE_DIR, "ventas2025.png"))
        img = img.resize((120, 120))
        logo_tk = ImageTk.PhotoImage(img)

        ticket.logo_tk = logo_tk
        lbl_logo = ttk.Label(ticket, image=logo_tk)
        lbl_logo.pack(pady=10)

    except:
        ttk.Label(ticket, text="(Sin logo)", font=("Arial", 10)).pack(pady=10)

    texto = (
        " * DULCERIA TOMY *\n"
        "--------------------------------------\n"
        f"Fecha: {fecha_hora}\n"
        "--------------------------------------\n"
        f"Producto: {producto}\n"
        f"Precio: ${precio}\n"
        f"Cantidad: {cantidad}\n"
        "--------------------------------------\n"
        f"TOTAL: ${total}\n"
        "--------------------------------------\n"
        " ¡GRACIAS POR SU COMPRA!\n"
    )

    lbl_ticket = ttk.Label(ticket, text=texto, justify="left", font=("Arial", 11))
    lbl_ticket.pack(pady=10)

    btn_cerrar = ttk.Button(ticket, text="Cerrar", command=ticket.destroy)
    btn_cerrar.pack(pady=10)


# ==========================================
# REGISTRO DE VENTAS
# ==========================================
def abrir_registro_ventas():
    ven = ttk.Toplevel()
    ven.title("Registro de Ventas")
    ven.geometry("420x430")
    ven.resizable(False, False)

    productos = {}

    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivof = os.path.join(BASE_DIR, "productos.txt")
        with open(archivof, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                partes = linea.strip().split("|")
                if len(partes) == 4:
                    idp, desc, precio, cat = partes
                    productos[desc] = float(precio)
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo productos.txt")
        ven.destroy()
        return

    lista_productos = list(productos.keys())

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
    cantidad_var = ttk.StringVar(ven)
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
            txt_precio.delete(0, ttk.END)
            txt_precio.insert(0, productos[prod])
            txt_precio.config(state="readonly")
            calcular_total()

    def calcular_total(*args):
        try:
            cant = int(txt_cantidad.get())
            precio = float(txt_precio.get())
            total = cant * precio
            txt_total.config(state="normal")
            txt_total.delete(0, ttk.END)
            txt_total.insert(0, total)
            txt_total.config(state="readonly")
        except:
            txt_total.config(state="normal")
            txt_total.delete(0, ttk.END)
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
            mostrar_ticket(prod, precio, cant, total)

        cb_producto.set("")
        txt_precio.config(state="normal"); txt_precio.delete(0, ttk.END); txt_precio.config(state="readonly")
        txt_cantidad.delete(0, ttk.END)
        txt_total.config(state="normal"); txt_total.delete(0, ttk.END); txt_total.config(state="readonly")

    cb_producto.bind("<<ComboboxSelected>>", actualizar_precio)

    btn_guardar = ttk.Button(ven, text="Registrar Venta", command=registrar_venta)
    btn_guardar.pack(pady=25)


# ==========================================
# REPORTES
# ==========================================
def abrir_reportes():

    ventana = ttk.Toplevel()
    ventana.title("Reporte de Ventas")
    ventana.geometry("700x400")
    ventana.configure(bg="#f2f2f2")

    titulo = ttk.Label(
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
                        tabla.insert("", ttk.END, values=datos)
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo ventas.txt no existe.")
        ventana.destroy()


# ==========================================
# ACERCA DE
# ==========================================
def abrir_acerca_de():
    acerca = ttk.Toplevel()
    acerca.title("Acerca de")
    acerca.geometry("250x200")
    acerca.resizable(False, False)

    lbl = ttk.Label(acerca, text="Dulceria Tomy", font=("Arial", 14))
    lbl.pack(pady=20)


# ==========================================
# VENTANA PRINCIPAL
# ==========================================
ventana = ttk.Tk()
ventana.title("Dulceria Tomy")
ventana.geometry("500x600")
ventana.resizable(False, False)
ventana.configure(bg="#FFD8A8")

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    imagen = Image.open(os.path.join(BASE_DIR, "ventas2025.png"))
    imagen = imagen.resize((250, 250))
    img_logo = ImageTk.PhotoImage(imagen)

    lbl_logo = ttk.Label(ventana, image=img_logo, bg="#FFD8A8")
    lbl_logo.pack(pady=20)
except:
    lbl_sin_logo = ttk.Label(
        ventana,
        text="(Aquí va el logo del sistema)",
        font=("Arial", 14),
        bg="#FFD8A8"
    )
    lbl_sin_logo.pack(pady=40)


# BOTONES
def crear_boton(texto, comando):
    return ttk.Button(
        ventana,
        text=texto,
        command=comando,
        font=("Arial", 12),
        bg="black",
        fg="white",
        activebackground="#333333",
        activeforeground="white",
        width=22,
        height=2
    )

crear_boton("Registro de Productos", abrir_registro_productos).pack(pady=10)
crear_boton("Registro de Ventas", abrir_registro_ventas).pack(pady=10)
crear_boton("Reportes", abrir_reportes).pack(pady=10)
crear_boton("Acerca de", abrir_acerca_de).pack(pady=10)

ventana.mainloop()
