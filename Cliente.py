from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
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
def existe(telefono):
    query = "SELECT telefono FROM cliente WHERE telefono = %s"
    cursor.execute(query, (telefono,))
    return cursor.fetchone() is not None

def consultar():
    try:
        query = "SELECT telefono, nombre, correo, genero FROM cliente"
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        if not resultados:
            show_popup("Información", "No hay datos registrados")
            return
            
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        main_layout.height = Window.height * 0.8
        
        # Título
        titulo = Label(text="Listado de Clientes", 
                     size_hint_y=None,
                     height=50,
                     font_size='20sp',
                     bold=True,
                     color=(0, 0, 0, 1))
        
        # Grid de datos
        grid = GridLayout(cols=4, size_hint_y=None, spacing=2)
        grid.bind(minimum_height=grid.setter('height'))
        
        # Encabezados
        for text in ["Telefono", "Nombre", "Correo", "Genero"]:
            grid.add_widget(Label(text=text, bold=True, size_hint_y=None, height=40))
        
        # Datos
        for telefono, nombre,correo, genero in resultados:
            grid.add_widget(Label(text=str(telefono), size_hint_y=None, height=30))
            grid.add_widget(Label(text=nombre, size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(correo), size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(genero), size_hint_y=None, height=30))
            
        # ScrollView
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(grid)
        
        # Ensamblar
        main_layout.add_widget(titulo)
        main_layout.add_widget(scroll)
        
        # Popup
        popup = Popup(title="Clientes",
                    content=main_layout,
                    size_hint=(0.9, 0.9),
                    background_color=(1, 1, 1, 1))
        popup.open()
        
    except Exception as e:
        show_popup("Error", f"Error al consultar los datos: {str(e)}")

def insertar(telefono, nombre, genero, correo):
    query = "INSERT INTO cliente(telefono, nombre, genero, correo) VALUES (%s, %s, %s, %s)"
    valores = (telefono, nombre, genero, correo)
    cursor.execute(query, valores)
    conexion.commit()

def actualizar(telefono, nombre, genero, correo):
    query = "UPDATE cliente SET nombre = %s, genero = %s, correo = %s WHERE telefono = %s"
    valores = (nombre, genero, correo, telefono)
    cursor.execute(query, valores)
    conexion.commit()

def eliminar(telefono):
    query = "DELETE FROM cliente WHERE telefono = %s"
    valores = (telefono,)
    cursor.execute(query, valores)
    conexion.commit()

class ClienteScreen(Screen):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Interfaz
        Window.clearcolor = (0.12, 0.12, 0.12, 1)
        layout = FloatLayout()

        # Título
        layout.add_widget(Label(text='Catálogo de Cliente',
                                pos_hint={'x': 0.27, 'y': 0.87},
                                size_hint=(0.5, 0.1),
                                color=(1, 1, 1, 1),
                                font_size='24sp'))

        # Campos de entrada
        # Teléfono
        layout.add_widget(Label(text='Teléfono',
                                pos_hint={'x': 0.05, 'y': 0.75},
                                size_hint=(0.3, 0.1),
                                color=(1, 1, 1, 1),
                                font_size='18sp'))
        telefono = TextInput(
                                background_color=(1, 1, 1, 1),
                                pos_hint={'x': 0.3, 'y': 0.77},
                                size_hint=(0.4, 0.05),
                                input_filter='int',
                                multiline=False)
        layout.add_widget(telefono)

        # Nombre
        layout.add_widget(Label(text='Nombre',
                                pos_hint={'x': 0.05, 'y': 0.65},
                                size_hint=(0.3, 0.1),
                                color=(1, 1, 1, 1),
                                font_size='18sp'))
        nombre = TextInput(
                                background_color=(1, 1, 1, 1),
                                pos_hint={'x': 0.3, 'y': 0.67},
                                size_hint=(0.4, 0.05),
                                multiline=False)
        layout.add_widget(nombre)

        # Género
        layout.add_widget(Label(text='Género',
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
                            size_hint=(0.2, 0.05))
        layout.add_widget(genero)

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
                                )
        layout.add_widget(correo)

        # Funciones de los botones
        def crear_cliente(instance):
            tel = telefono.text
            nom = nombre.text
            gen = genero.text
            cor = correo.text
            
            if tel and nom and gen != 'Seleccionar' and cor:
                if existe(tel):
                    show_popup("Error", f"El cliente con teléfono {tel} ya existe")
                else:
                    insertar(tel, nom, gen, cor)
                    show_popup("Éxito", "Cliente creado correctamente")
                    # Limpiar campos
                    telefono.text = ""
                    nombre.text = ""
                    genero.text = 'Seleccionar'
                    correo.text = ""
            else:
                show_popup("Error", "Por favor llena todos los campos correctamente")

        def actualizar_cliente(instance):
            tel = telefono.text
            nom = nombre.text
            gen = genero.text
            cor = correo.text
            
            if tel and nom and gen != 'Seleccionar' and cor:
                if existe(tel):
                    actualizar(tel, nom, gen, cor)
                    show_popup("Éxito", "Cliente actualizado correctamente")
                else:
                    show_popup("Error", f"El cliente con teléfono {tel} no existe")
            else:
                show_popup("Error", "Por favor completa todos los campos")

        def eliminar_cliente(instance):
            tel = telefono.text
            if tel:
                eliminar(tel)
                show_popup("Éxito", "Cliente eliminado correctamente")
                # Limpiar campos
                telefono.text = ""
                nombre.text = ""
                genero.text = 'Seleccionar'
                correo.text = ""
            else:
                show_popup("Error", "Ingresa el teléfono del cliente a eliminar")

        # Botones
        boton_crear = Button(text='Crear',
                            background_color=(0, 0.5, 1, 1),
                            color=(1, 1, 1, 1),
                            pos_hint={'x': 0.1, 'y': 0.2},
                            size_hint=(0.2, 0.08))
        boton_crear.bind(on_press=crear_cliente)
        layout.add_widget(boton_crear)

        boton_actualizar = Button(text='Actualizar',
                                background_color=(0, 0.5, 1, 1),
                                color=(1, 1, 1, 1),
                                pos_hint={'x': 0.4, 'y': 0.2},
                                size_hint=(0.2, 0.08))
        boton_actualizar.bind(on_press=actualizar_cliente)
        layout.add_widget(boton_actualizar)

        boton_eliminar = Button(text='Eliminar',
                            background_color=(0, 0.5, 1, 1),
                            color=(1, 1, 1, 1),
                            pos_hint={'x': 0.7, 'y': 0.2},
                            size_hint=(0.2, 0.08))
        boton_eliminar.bind(on_press=eliminar_cliente)
        layout.add_widget(boton_eliminar)

        boton_consultar = Button(text='Consultar',
                                background_color=(0, 0.5, 1, 1),
                                color=(1, 1, 1, 1),
                                pos_hint={'x': 0.3, 'y': 0.08},  
                                size_hint=(0.4, 0.08))  
        boton_consultar.bind(on_press=lambda x: consultar())
        layout.add_widget(boton_consultar)
        
        boton_volver = Button(
            text='Volver al menú',
            background_color=(1, 0, 0, 1),
            color=(1, 1, 1, 1),
            pos_hint={'x': 0.8, 'y': 0.87},
            size_hint=(0.15, 0.08)
        )
        boton_volver.bind(on_press=self.volver_menu)
        layout.add_widget(boton_volver)

        # Validaciones
        def limitar_id(instance, value):
            if len(value) > 10:
                instance.text = value[:10]
        telefono.bind(text=limitar_id)

        def sin_espacios(instance, value):
            if ' ' in value:
                instance.text = value.replace(' ', '')
        correo.bind(text=sin_espacios)
        
        self.add_widget(layout)
        
    def volver_menu(self, instance):
        self.manager.current = 'menu'