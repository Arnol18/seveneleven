from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
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
    database="tienda"
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

def consultar():
    try:
        query = "SELECT id_proveedor, nombre, telefono, correo FROM proveedor"
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        if not resultados:
            show_popup("Información", "No hay datos registrados")
            return
            
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        main_layout.height = Window.height * 0.8
        
        # Título
        titulo = Label(text="Listado de Proveedores", 
                     size_hint_y=None,
                     height=50,
                     font_size='20sp',
                     bold=True,
                     color=(0, 0, 0, 1))
        
        # Grid de datos
        grid = GridLayout(cols=4, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))
        
        # Encabezados
        for text in ["id_proveedor", "Nombre", "Telefono", "Correo"]:
            grid.add_widget(Label(text=text, bold=True, size_hint_y=None, height=40))
        
        # Datos
        for id_proveedor, nombre, telefono, correo in resultados:
            grid.add_widget(Label(text=str(id_proveedor), size_hint_y=None, height=30))
            grid.add_widget(Label(text=nombre, size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(telefono), size_hint_y=None, height=30))
            grid.add_widget(Label(text=correo, size_hint_y=None, height=30))
            
        # ScrollView
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(grid)
        
        # Ensamblar
        main_layout.add_widget(titulo)
        main_layout.add_widget(scroll)
        
        # Popup
        popup = Popup(title="Proveedores",
                    content=main_layout,
                    size_hint=(0.9, 0.9),
                    background_color=(1, 1, 1, 1))
        popup.open()
    except Exception as e:
            show_popup("Error", f"Error al consultar los datos: {str(e)}")

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
    valores = (id_proveedor,)
    cursor.execute(query, valores)
    conexion.commit()

# Nueva función para leer artículos
def leer_articulos():
    query = "SELECT codigo, nombre FROM articulo"
    cursor.execute(query)
    resultados = cursor.fetchall()
    return {nombre: codigo for codigo, nombre in resultados}

def atribuir(id_proveedor, codigo_articulo):
    query = "UPDATE articulo SET id_proveedor = %s WHERE codigo = %s"
    valores = (id_proveedor, codigo_articulo)
    cursor.execute(query, valores)
    conexion.commit()

class ProveedorScreen(Screen):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

        # Spinner para artículos
        articulos_dict = leer_articulos()
        self.articulo_seleccionado = None
        
        def articulo_select(spinner, text):
            self.articulo_seleccionado = articulos_dict.get(text)
            print(f'Seleccionaste: {text} (Código: {self.articulo_seleccionado})')
    
        articulo_spinner = Spinner(text='Seleccionar',
                                values=list(articulos_dict.keys()), 
                                background_color=(0.8, 0.8, 0.8, 1),
                                color=(1, 1, 1, 1),
                                pos_hint={'x': 0.3, 'y': 0.37},
                                size_hint=(0.2, 0.05))

        layout.add_widget(Label(text='Artículo',
                                pos_hint={'x': 0.05, 'y': 0.35},
                                size_hint=(0.3, 0.1),
                                color=(1, 1, 1, 1),
                                font_size='18sp'))
        layout.add_widget(articulo_spinner)
        articulo_spinner.bind(text=articulo_select)

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
            else:
                show_popup("Error", "Por favor llena todos los campos correctamente")
                
        def actualizar_proveedor(instance):
            id = id_proveedor.text
            tel = telefono.text
            nom = nombre.text
            cor = correo.text
            
            if id and tel and nom and cor:
                if existe(id):
                    actualizar(id, nom, tel, cor)
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
                
        def agregar_proveedor_articulo(instance):
            id = id_proveedor.text
            codigo = self.articulo_seleccionado
            if id and codigo:
                atribuir(id, codigo)
                show_popup("Éxito", "Proveedor asignado al artículo correctamente")
            else:
                show_popup("Error", "Selecciona un artículo e ingresa el ID del proveedor")

        # Botones
        boton_crear = Button(text='Crear',
                            background_color=(0, 0.5, 1, 1),
                            color=(1, 1, 1, 1),
                            pos_hint={'x': 0.1, 'y': 0.2},
                            size_hint=(0.2, 0.08))
        boton_crear.bind(on_press=crear_proveedor)
        layout.add_widget(boton_crear)

        boton_actualizar = Button(text='Actualizar',
                                background_color=(0, 0.5, 1, 1),
                                color=(1, 1, 1, 1),
                                pos_hint={'x': 0.4, 'y': 0.2},
                                size_hint=(0.2, 0.08))
        boton_actualizar.bind(on_press=actualizar_proveedor)
        layout.add_widget(boton_actualizar)

        boton_eliminar = Button(text='Eliminar',
                            background_color=(0, 0.5, 1, 1),
                            color=(1, 1, 1, 1),
                            pos_hint={'x': 0.7, 'y': 0.2},
                            size_hint=(0.2, 0.08))
        boton_eliminar.bind(on_press=eliminar_proveedor)
        layout.add_widget(boton_eliminar)
        
        boton_agregar = Button(text='Agregar',
                            background_color=(0, 0.5, 1, 1),
                            color=(1, 1, 1, 1),
                            pos_hint={'x': 0.55, 'y': 0.3},
                            size_hint=(0.2, 0.08))
        boton_agregar.bind(on_press=agregar_proveedor_articulo)
        layout.add_widget(boton_agregar)

        boton_consultar = Button(text='Consultar',
                                background_color=(0, 0.5, 1, 1),
                                color=(1, 1, 1, 1),
                                pos_hint={'x': 0.3, 'y': 0.04}, 
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
        self.add_widget(layout)
        
    def volver_menu(self, instance):
        self.manager.current = 'menu'