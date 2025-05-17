from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import hashlib
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label as PopupLabel
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
def existe_usuario(id_empleado):
    query = "SELECT id_empleado FROM empleado WHERE id_empleado = %s"
    cursor.execute(query, (id_empleado,))
    return cursor.fetchone() is not None

def consultar():
    try:
        query = "SELECT id_empleado, nombre, genero, puesto, sueldo FROM empleado"
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        if not resultados:
            show_popup("Información", "No hay datos registrados")
            return
            
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        main_layout.height = Window.height * 0.8
        
        # Título
        titulo = Label(text="Listado de Empleados", 
                     size_hint_y=None,
                     height=50,
                     font_size='20sp',
                     bold=True,
                     color=(0, 0, 0, 1))
        
        # Grid de datos
        grid = GridLayout(cols=5, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))
        
        # Encabezados
        for text in ["id_empleado", "Nombre", "Genero", "Puesto", "Sueldo"]:
            grid.add_widget(Label(text=text, bold=True, size_hint_y=None, height=40))
        
        # Datos
        for id_empleado, nombre, genero, puesto, sueldo in resultados:
            grid.add_widget(Label(text=str(id_empleado), size_hint_y=None, height=30))
            grid.add_widget(Label(text=nombre, size_hint_y=None, height=30))
            grid.add_widget(Label(text=genero, size_hint_y=None, height=30))
            grid.add_widget(Label(text=puesto, size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(sueldo), size_hint_y=None, height=30))
            
        # ScrollView
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(grid)
        
        # Ensamblar
        main_layout.add_widget(titulo)
        main_layout.add_widget(scroll)
        
        # Popup
        popup = Popup(title="Empleados",
                    content=main_layout,
                    size_hint=(0.9, 0.9),
                    background_color=(1, 1, 1, 1))
        popup.open()
        
    except Exception as e:
        show_popup("Error", f"Error al consultar los datos: {str(e)}")


def inserta_usuario(id_empleado, nombre, genero, puesto, sueldo, clave):
    query = "INSERT INTO empleado(id_empleado, nombre, genero, puesto, sueldo, clave) VALUES (%s, %s, %s, %s, %s, MD5(%s))"
    valores = (id_empleado, nombre, genero, puesto, sueldo, clave)
    cursor.execute(query, valores)
    conexion.commit()

def actualiza_usuario(id_empleado,nsueldo, nclave):
    query = "UPDATE empleado SET sueldo = %s, clave = MD5(%s) WHERE id_empleado = %s"
    valores = (nsueldo, nclave,id_empleado)
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
                        input_filter='int',
                        multiline=False)
layout.add_widget(id_empleado)

# Nombre
layout.add_widget(Label(text='Nombre',
                        pos_hint={'x': 0.05, 'y': 0.65},
                        size_hint=(0.3, 0.1),
                        color=(1, 1, 1, 1),
                        font_size='18sp'))
nombre = TextInput(background_color=(1, 1, 1, 1),
                        pos_hint={'x': 0.3, 'y': 0.67},
                        size_hint=(0.4, 0.05),
                        multiline=False)
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

# Sueldo
layout.add_widget(Label(text='Sueldo',
                        pos_hint={'x': 0.05, 'y': 0.35},
                        size_hint=(0.3, 0.1),
                        color=(1, 1, 1, 1),
                        font_size='18sp'))
sueldo = TextInput(background_color=(1, 1, 1, 1),
                         pos_hint={'x': 0.3, 'y': 0.37},
                         size_hint=(0.4, 0.05),
                         input_filter='float',
                         multiline=False)
layout.add_widget(sueldo)

# Clave
layout.add_widget(Label(text='Clave',
                        pos_hint={'x': 0.05, 'y': 0.25},
                        size_hint=(0.3, 0.1),
                        color=(1, 1, 1, 1),
                        font_size='18sp'))
clave = TextInput(password=True,
                        password_mask='•',
                        background_color=(1, 1, 1, 1),
                        pos_hint={'x': 0.3, 'y': 0.27},
                        size_hint=(0.4, 0.05),
                        multiline=False,
                        font_size='15sp')
layout.add_widget(clave)

mostrar = ToggleButton(text='Mostrar',
                       pos_hint={'x': 0.71, 'y': 0.27},
                       size_hint=(0.08, 0.05))
mostrar.bind(on_press=lambda instance: (
    setattr(clave, 'password', instance.state == 'normal')))
layout.add_widget(mostrar)

# Funciones de los botones
def Crear(instance):
    id_emp = id_empleado.text
    nombre_usuario = nombre.text
    genero_usuario = genero.text
    puesto_usuario = puesto.text
    sueldo_usuario = sueldo.text
    clave_usuario = clave.text
    if id_emp and nombre_usuario and genero_usuario != 'Seleccionar' and puesto_usuario != 'Seleccionar' and sueldo_usuario and clave_usuario:
        if existe_usuario(id_emp):
            show_popup("Error", f"El usuario con ID {id_emp} ya existe")
        else:
            inserta_usuario(id_emp, nombre_usuario, genero_usuario, puesto_usuario, sueldo_usuario, clave_usuario)
            show_popup("Éxito", "Usuario creado correctamente")
    else:
        show_popup("Error", "Por favor llena todos los campos correctamente")

def Actualizar(instance):
    id_usuario = id_empleado.text
    sueldo_usuario = sueldo.text
    nueva_clave = clave.text
    if id_usuario and sueldo_usuario and nueva_clave:
        if existe_usuario(id_usuario):
            actualiza_usuario(id_usuario, sueldo_usuario, nueva_clave)
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

        # Convertir clave ingresada a MD5 en Python
        clave_md5 = hashlib.md5(clave_usuario.encode()).hexdigest()
        print(hashlib.md5("password".encode()).hexdigest())
        # Verificar contraseña con la clave MD5
        cursor.execute("SELECT id_empleado FROM empleado WHERE id_empleado = %s AND clave = %s", 
                       (id_usuario, clave_md5))
        
        if cursor.fetchone():
            # Eliminar usuario
            cursor.execute("DELETE FROM empleado WHERE id_empleado = %s", (id_usuario,))
            conexion.commit()
            
            # Limpiar campos
            id_empleado.text = ""
            nombre.text = ""
            sueldo.text = ""
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
                     pos_hint={'x': 0.1, 'y': 0.15},
                     size_hint=(0.2, 0.08))
boton_crear.bind(on_press=Crear)
layout.add_widget(boton_crear)

boton_actualizar = Button(text='Actualizar',
                          background_color=(0, 0.5, 1, 1),
                          color=(1, 1, 1, 1),
                          pos_hint={'x': 0.4, 'y': 0.15},
                          size_hint=(0.2, 0.08))
boton_actualizar.bind(on_press=Actualizar)
layout.add_widget(boton_actualizar)

boton_eliminar = Button(text='Eliminar',
                        background_color=(0, 0.5, 1, 1),
                        color=(1, 1, 1, 1),
                        pos_hint={'x': 0.7, 'y': 0.15},
                        size_hint=(0.2, 0.08))
boton_eliminar.bind(on_press=Eliminar)
layout.add_widget(boton_eliminar)

boton_consultar = Button(text='Consultar',
                        background_color=(0, 0.5, 1, 1),
                        color=(1, 1, 1, 1),
                        pos_hint={'x': 0.3, 'y': 0.04}, 
                        size_hint=(0.4, 0.08))  
boton_consultar.bind(on_press=lambda x: consultar())
layout.add_widget(boton_consultar)

# Validaciones
def limitar_id(instance, value):
    if len(value) > 11:
        instance.text = value[:10]
id_empleado.bind(text=limitar_id)
# App
class CatalogoEmpleadooApp(App):
    def build(self):
        return layout

CatalogoEmpleadooApp().run()