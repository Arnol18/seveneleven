from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label as PopupLabel
from kivy.core.window import Window
import mysql.connector

# Popup de notificación
def show_popup(title, message):
    popup_label = PopupLabel(text=message, font_size='18sp')
    popup = Popup(title=title,
                content=popup_label,
                size_hint=(0.6, 0.3),
                auto_dismiss=True)
    popup.open()

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="seveneleven"
)
if conexion.is_connected():
    print("Conexión exitosa")
    cursor = conexion.cursor()
else:
    print("No se pudo conectar a la base de datos")

# Funciones SQL 
def existe(id_proveedor):
    query = "SELECT id_proveedor FROM proveedor WHERE id_proveedor = %s"
    cursor.execute(query, (id_proveedor,))
    return cursor.fetchone() is not None

def insertar(id_proveedor,telefono, nombre, correo):
    query = "INSERT INTO proveedor(id_proveedor, nombre,telefono, correo) VALUES (%s, %s, %s, %s)"
    valores = (id_proveedor, nombre,telefono, correo)
    cursor.execute(query, valores)
    conexion.commit()

def actualizar(id_proveedor, nombre, telefono, correo):
    query = "UPDATE proveedor SET nombre = %s, telefono=%s, correo = %s WHERE id_proveedor = %s"
    valores = (nombre, telefono, correo, id_proveedor,)
    cursor.execute(query, valores)
    conexion.commit()

def eliminar(id_proveedor):
    query = "DELETE FROM proveedor WHERE id_proveedor = %s"
    valores = (id_proveedor)
    cursor.execute(query, valores)
    conexion.commit()

def cerrar():
    cursor.close()
    conexion.close()

# Interfaz
Window.clearcolor = (0.12, 0.12, 0.12, 1)
layout = FloatLayout()

# Título
layout.add_widget(Label(
    text='Catálogo de Proveedor',
    pos_hint={'x': 0.27, 'y': 0.87},
    size_hint=(0.5, 0.1),
    color=(1, 1, 1, 1),
    font_size='24sp'
))

# ID proveedor
layout.add_widget(Label(text='ID proveedor',
                      pos_hint={'x': 0.05, 'y': 0.75},
                      size_hint=(0.3, 0.1),
                      color=(1, 1, 1, 1),
                      font_size='18sp'))
id_proveedor = TextInput(
    background_color=(1, 1, 1, 1),
    pos_hint={'x': 0.3, 'y': 0.77},
    size_hint=(0.4, 0.05),
    input_filter='int',
    multiline=False)
layout.add_widget(id_proveedor)

# Teléfono
layout.add_widget(Label(text='Teléfono',
                      pos_hint={'x': 0.05, 'y': 0.65},
                      size_hint=(0.3, 0.1),
                      color=(1, 1, 1, 1),
                      font_size='18sp'))
telefono = TextInput(
    background_color=(1, 1, 1, 1),
    pos_hint={'x': 0.3, 'y': 0.67},
    size_hint=(0.4, 0.05),
    input_filter='int',
    multiline=False)
layout.add_widget(telefono)

# Nombre
layout.add_widget(Label(text='Nombre',
                      pos_hint={'x': 0.05, 'y': 0.55},
                      size_hint=(0.3, 0.1),
                      color=(1, 1, 1, 1),
                      font_size='18sp'))
nombre = TextInput(
    background_color=(1, 1, 1, 1),
    pos_hint={'x': 0.3, 'y': 0.57},
    size_hint=(0.4, 0.05),
    multiline=False)
layout.add_widget(nombre)

# Correo
layout.add_widget(Label(text='Correo',
                      pos_hint={'x': 0.05, 'y': 0.45},
                      size_hint=(0.3, 0.1),
                      color=(1, 1, 1, 1),
                      font_size='18sp'))
correo = TextInput(
    background_color=(1, 1, 1, 1),
    pos_hint={'x': 0.3, 'y': 0.47},
    size_hint=(0.4, 0.05),
    multiline=False)
layout.add_widget(correo)

# Botones
boton_crear = Button(text='Crear',
                    background_color=(0, 0.5, 1, 1),
                    color=(1, 1, 1, 1),
                    pos_hint={'x': 0.1, 'y': 0.2},
                    size_hint=(0.2, 0.08))
layout.add_widget(boton_crear)

boton_actualizar = Button(text='Actualizar',
                         background_color=(0, 0.5, 1, 1),
                         color=(1, 1, 1, 1),
                         pos_hint={'x': 0.4, 'y': 0.2},
                         size_hint=(0.2, 0.08))
layout.add_widget(boton_actualizar)

boton_eliminar = Button(text='Eliminar',
                       background_color=(0, 0.5, 1, 1),
                       color=(1, 1, 1, 1),
                       pos_hint={'x': 0.7, 'y': 0.2},
                       size_hint=(0.2, 0.08))
layout.add_widget(boton_eliminar)

# Funciones de los botones
def crear_proveedor(instance):
    id = id_proveedor.text
    tel = telefono.text
    nom = nombre.text
    cor = correo.text
    
    if id and tel and nom and cor:
        if existe(id):
            show_popup("Error", f"El proveedor con ID {id} ya existe")
        else:
            insertar(id, tel, nom, cor)
            show_popup("Éxito", "Proveedor creado correctamente")
            # Limpiar campos
            id_proveedor.text = ""
            telefono.text = ""
            nombre.text = ""
            correo.text = ""
    else:
        show_popup("Error", "Por favor llena todos los campos correctamente")

def actualizar_proveedor(instance):
    id = id_proveedor.text
    tel = telefono.text
    nom = nombre.text
    cor = correo.text
    
    if id and tel and nom and cor:
        if existe(id):
            actualizar(id, nom, cor)
            show_popup("Éxito", "Proveedor actualizado correctamente")
        else:
            show_popup("Error", f"El proveedor con ID {id} no existe")
    else:
        show_popup("Error", "Por favor completa todos los campos")

def eliminar_proveedor(instance):
    id = id_proveedor.text
    if id:
        eliminar(id)
        show_popup("Éxito", "Proveedor eliminado correctamente")
        # Limpiar campos
        id_proveedor.text = ""
        telefono.text = ""
        nombre.text = ""
        correo.text = ""
    else:
        show_popup("Error", "Ingresa el ID del proveedor a eliminar")

# Validaciones
def limitar_telefono(instance, value):
    if len(value) > 10:
        instance.text = value[:10]
telefono.bind(text=limitar_telefono)

def limitar_id(instance, value):
    if len(value) > 13:
        instance.text = value[:13]
id_proveedor.bind(text=limitar_id)

def sin_espacios(instance, value):
    if ' ' in value:
        instance.text = value.replace(' ', '')
correo.bind(text=sin_espacios)

# App
class CatalogoProveedorApp(App):
    def build(self):
        return layout
CatalogoProveedorApp().run()