from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label as PopupLabel
import mysql.connector  # type: ignore

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
def existe_usuario(id_empleado):
    query = "SELECT id_empleado FROM empleado WHERE id_empleado = %s"
    cursor.execute(query, (id_empleado,))
    return cursor.fetchone() is not None

def inserta_usuario(id_empleado, nombre, genero, puesto, clave):
    query = "INSERT INTO empleado(id_empleado, nombre, genero, puesto, clave) VALUES (%s, %s, %s, %s, MD5(%s))"
    valores = (id_empleado, nombre, genero, puesto, clave)
    cursor.execute(query, valores)
    conexion.commit()

def actualiza_usuario(id_empleado, contra):
    query = "UPDATE empleado SET clave = MD5(%s) WHERE id_empleado = %s"
    valores = (contra, id_empleado)
    cursor.execute(query, valores)
    conexion.commit()

def elimina_usuario(id_empleado):
    query = "DELETE FROM empleado WHERE id_empleado = %s"
    valores = (id_empleado,)
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
    text='Catalogo de Empleado',
    pos_hint={'x': 0.27, 'y': 0.87},
    size_hint=(0.5, 0.1),
    color=(1, 1, 1, 1),
    font_size='24sp'
))

# ID Empleado
layout.add_widget(Label(text='ID Empleado',
                        pos_hint={'x': 0.05, 'y': 0.75},
                        size_hint=(0.3, 0.1),
                        color=(1, 1, 1, 1),
                        font_size='18sp'))
id_empleado = TextInput(
    background_color=(1, 1, 1, 1),
    pos_hint={'x': 0.3, 'y': 0.77},
    size_hint=(0.4, 0.05),
    input_filter='int'
)
layout.add_widget(id_empleado)

# Nombre
layout.add_widget(Label(text='Nombre',
                        pos_hint={'x': 0.05, 'y': 0.65},
                        size_hint=(0.3, 0.1),
                        color=(1, 1, 1, 1),
                        font_size='18sp'))
nombre = TextInput(background_color=(1, 1, 1, 1),
                         pos_hint={'x': 0.3, 'y': 0.67},
                         size_hint=(0.4, 0.05))
layout.add_widget(nombre)

# Género
layout.add_widget(Label(text='Genero',
                        pos_hint={'x': 0.05, 'y': 0.55},
                        size_hint=(0.3, 0.1),
                        color=(1, 1, 1, 1),
                        font_size='18sp'))
genero = Spinner(
    text='Seleccionar',
    values=('M', 'F'),
    background_color=(0.8, 0.8, 0.8, 1),
    color=(1, 1, 1, 1),
    pos_hint={'x': 0.3, 'y': 0.57},
    size_hint=(0.2, 0.05)
)
layout.add_widget(genero)

# Puesto
layout.add_widget(Label(text='Puesto',
                        pos_hint={'x': 0.05, 'y': 0.45},
                        size_hint=(0.3, 0.1),
                        color=(1, 1, 1, 1),
                        font_size='18sp'))
puesto = Spinner(
    text='Seleccionar',
    values=('Cajero', 'Encargado'),
    background_color=(0.8, 0.8, 0.8, 1),
    color=(1, 1, 1, 1),
    pos_hint={'x': 0.3, 'y': 0.47},
    size_hint=(0.2, 0.05)
)
layout.add_widget(puesto)

# Clave
layout.add_widget(Label(text='Clave',
                        pos_hint={'x': 0.05, 'y': 0.35},
                        size_hint=(0.3, 0.1),
                        color=(1, 1, 1, 1),
                        font_size='18sp'))
clave = TextInput(password=True,
                        password_mask='•',
                        background_color=(1, 1, 1, 1),
                        pos_hint={'x': 0.3, 'y': 0.37},
                        size_hint=(0.4, 0.05),
                        font_size='15sp')
layout.add_widget(clave)

# Funciones de los botones
def Crear(instance):
    id_emp = id_empleado.text
    nombre_usuario = nombre.text
    genero_usuario = genero.text
    puesto_usuario = puesto.text
    clave_usuario = clave.text
    if id_emp and nombre_usuario and genero_usuario != 'Seleccionar' and puesto_usuario != 'Seleccionar' and clave_usuario:
        if existe_usuario(id_emp):
            show_popup("Error", f"El usuario con ID {id_emp} ya existe")
        else:
            inserta_usuario(id_emp, nombre_usuario, genero_usuario, puesto_usuario, clave_usuario)
            show_popup("Éxito", "Usuario creado correctamente")
    else:
        show_popup("Error", "Por favor llena todos los campos correctamente")

def Actualizar(instance):
    id_usuario = id_empleado.text
    nueva_clave = clave.text
    if id_usuario and nueva_clave:
        if existe_usuario(id_usuario):
            actualiza_usuario(id_usuario, nueva_clave)
            show_popup("Éxito", "Contraseña actualizada correctamente")
        else:
            show_popup("Error", f"El usuario con ID {id_usuario} no existe")
    else:
        show_popup("Error", "Por favor ingresa el ID y la nueva clave")

def Eliminar(instance):
    try:
        id_usuario = id_empleado.text.strip()
        clave_usuario = clave.text.strip()

        if not id_usuario or not clave_usuario:
            show_popup("Error", "Debes ingresar tanto el ID como la contraseña")
            return

        # Verificar primero si el usuario existe
        cursor.execute("SELECT id_empleado FROM empleado WHERE id_empleado = %s", (id_usuario,))
        if not cursor.fetchone():
            show_popup("Error", f"El usuario con ID {id_usuario} no existe")
            return

        # Verificar contraseña con MD5
        cursor.execute("SELECT id_empleado FROM empleado WHERE id_empleado = %s AND clave = MD5(%s)", 
                      (id_usuario, clave_usuario))
        
        if cursor.fetchone():
            # Eliminar usuario
            cursor.execute("DELETE FROM empleado WHERE id_empleado = %s", (id_usuario,))
            conexion.commit()
            
            # Limpiar campos
            id_empleado.text = ""
            nombre.text = ""
            clave.text = ""
            
            show_popup("Éxito", "Usuario eliminado correctamente")
        else:
            show_popup("Error", "Contraseña incorrecta. Verifica tus datos.")

    except Exception as e:
        print(f"Error: {str(e)}")
        show_popup("Error", "Ocurrió un error al procesar la solicitud")
        
# Botones
boton_crear = Button(text='Crear',
                     background_color=(0, 0.5, 1, 1),
                     color=(1, 1, 1, 1),
                     pos_hint={'x': 0.1, 'y': 0.2},
                     size_hint=(0.2, 0.08))
boton_crear.bind(on_press=Crear)
layout.add_widget(boton_crear)

boton_actualizar = Button(text='Actualizar',
                          background_color=(0, 0.5, 1, 1),
                          color=(1, 1, 1, 1),
                          pos_hint={'x': 0.4, 'y': 0.2},
                          size_hint=(0.2, 0.08))
boton_actualizar.bind(on_press=Actualizar)
layout.add_widget(boton_actualizar)

boton_eliminar = Button(text='Eliminar',
                        background_color=(0, 0.5, 1, 1),
                        color=(1, 1, 1, 1),
                        pos_hint={'x': 0.7, 'y': 0.2},
                        size_hint=(0.2, 0.08))
boton_eliminar.bind(on_press=Eliminar)
layout.add_widget(boton_eliminar)

# App
class CatalogoEmpleadooApp(App):
    def build(self):
        return layout

CatalogoEmpleadooApp().run()