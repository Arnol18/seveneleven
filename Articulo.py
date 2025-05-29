from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
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
def existe(codigo):
    query = "SELECT codigo FROM articulo WHERE codigo = %s"
    cursor.execute(query, (codigo,))
    return cursor.fetchone() is not None

def consultar():
    try:
        query = "SELECT codigo, nombre, precio, costo, existencias, id_categoria, id_unidad FROM articulo"
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        if not resultados:
            show_popup("Información", "No hay datos registrados")
            return
            
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        main_layout.height = Window.height * 0.8
        
        # Título
        titulo = Label(text="Listado de Articulos", 
                     size_hint_y=None,
                     height=50,
                     font_size='20sp',
                     bold=True,
                     color=(0, 0, 0, 1))
        
        # Grid de datos
        grid = GridLayout(cols=7, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))
        
        # Encabezados
        for text in ["codigo", "nombre", "precio", "costo", "existencias", "categoria","unidad"]:
            grid.add_widget(Label(text=text, bold=True, size_hint_y=None, height=40))
        
        # Datos
        for codigo, nombre, precio, costo, existencias, id_categoria, id_unidad in resultados:
            grid.add_widget(Label(text=str(codigo), size_hint_y=None, height=30))
            grid.add_widget(Label(text=nombre, size_hint_y=20, height=50))
            grid.add_widget(Label(text=str(precio), size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(costo), size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(existencias), size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(id_categoria), size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(id_unidad), size_hint_y=None, height=30))
            
        
        # ScrollView
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(grid)
        
        # Ensamblar
        main_layout.add_widget(titulo)
        main_layout.add_widget(scroll)
        
        # Popup
        popup = Popup(title="Articulos",
                    content=main_layout,
                    size_hint=(0.9, 0.9),
                    background_color=(1, 1, 1, 1))
        popup.open()
        
    except Exception as e:
        show_popup("Error", f"Error al consultar los datos: {str(e)}")

def insertar(codigo,nombre, precio, costo, existencias, reorden):
    query = "INSERT INTO articulo (codigo, nombre, precio, costo, existencias, reorden) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    valores = (codigo, nombre, precio, costo, existencias, reorden)
    cursor.execute(query, valores)
    conexion.commit()

def actualizar(codigo,nombre, precio, costo, existencias, reorden):
    query = "UPDATE articulo SET codigo = %s, nombre=%s, precio = %s, costo=%s, existencias = %s, reorden=%s WHERE codigo = %s"
    valores = (codigo,nombre, precio, costo, existencias, reorden)
    cursor.execute(query, valores)
    conexion.commit()

def eliminar(codigo):
    query = "DELETE FROM articulo WHERE codigo = %s"
    valores = (codigo,)
    cursor.execute(query, valores)
    conexion.commit()

def leer(id_columna, nombre_tabla):
    query = f"SELECT {id_columna} FROM {nombre_tabla}"
    cursor.execute(query)
    resultados = cursor.fetchall()
    return {id[0]: id[0] for id in resultados}


class ArticuloScreen(Screen):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Interfaz
        Window.clearcolor = (0.12, 0.12, 0.12, 1)
        layout = FloatLayout()

        # Codigo de barras
        layout.add_widget(Label(text='Codigo de Barras',
                            pos_hint={'x': 0.05, 'y': 0.85},
                            size_hint=(0.3, 0.1),
                            color=(1, 1, 1, 1),
                            font_size='18sp'))
        codigo_barras = TextInput(
            background_color=(1, 1, 1, 1),
            pos_hint={'x': 0.3, 'y': 0.87},
            size_hint=(0.4, 0.05),
            input_filter='int',
            multiline=False)
        layout.add_widget(codigo_barras)

        # Nombre
        layout.add_widget(Label(text='Nombre',
                            pos_hint={'x': 0.05, 'y': 0.75},
                            size_hint=(0.3, 0.1),
                            color=(1, 1, 1, 1),
                            font_size='18sp'))
        nombre = TextInput(
            background_color=(1, 1, 1, 1),
            pos_hint={'x': 0.3, 'y': 0.77},
            size_hint=(0.4, 0.05),
            multiline=False)
        layout.add_widget(nombre)

        # Precio
        layout.add_widget(Label(text='Precio',
                            pos_hint={'x': 0.05, 'y': 0.65},
                            size_hint=(0.3, 0.1),
                            color=(1, 1, 1, 1),
                            font_size='18sp'))
        precio = TextInput(
            background_color=(1, 1, 1, 1),
            pos_hint={'x': 0.3, 'y': 0.67},
            size_hint=(0.4, 0.05),
            input_filter='float',
            multiline=False)
        layout.add_widget(precio)

        # Costo
        layout.add_widget(Label(text='Costo',
                            pos_hint={'x': 0.05, 'y': 0.55},
                            size_hint=(0.3, 0.1),
                            color=(1, 1, 1, 1),
                            font_size='18sp'))
        costo = TextInput(
            background_color=(1, 1, 1, 1),
            pos_hint={'x': 0.3, 'y': 0.57},
            size_hint=(0.4, 0.05),
            multiline=False)
        layout.add_widget(costo)
        
         # Existencia
        layout.add_widget(Label(text='Existencia',
                            pos_hint={'x': 0.05, 'y': 0.45},
                            size_hint=(0.3, 0.1),
                            color=(1, 1, 1, 1),
                            font_size='18sp'))
        existencia = TextInput(
            background_color=(1, 1, 1, 1),
            pos_hint={'x': 0.3, 'y': 0.47},
            size_hint=(0.4, 0.05),
            multiline=False)
        layout.add_widget(existencia)
        
         # Reorden
        layout.add_widget(Label(text='Reorden',
                            pos_hint={'x': 0.05, 'y': 0.35},
                            size_hint=(0.3, 0.1),
                            color=(1, 1, 1, 1),
                            font_size='18sp'))
        reorden = TextInput(
            background_color=(1, 1, 1, 1),
            pos_hint={'x': 0.3, 'y': 0.37},
            size_hint=(0.4, 0.05),
            multiline=False)
        layout.add_widget(reorden)
        

        def seleccionado(spinner, text):
            global seleccionado_valor
            try:
                    seleccionado_valor = text
            except ValueError:
                seleccionado_valor = None
                
        # Funciones de los botones            
        def crear_articulo(instance):
            id = codigo_barras.text
            nom = nombre.text
            prc = precio.text
            cst= costo.text
            ext = existencia.text
            rod = reorden.text      
            if id and nom and prc and cst and ext and rod:
                if existe(id):
                    show_popup("Error", f"El articulo con codigo {id} ya existe")
                else:
                    insertar(id, nom, prc, cst, ext,rod)
                    show_popup("Éxito", "Articulo creado correctamente")
            else:
                show_popup("Error", "Por favor llena todos los campos correctamente")
            
        def actualizar_articulo(instance):
            id = codigo_barras.text
            nom = nombre.text
            prc = precio.text
            cst= costo.text
            ext = existencia.text
            rod = reorden.text 
            
            if id and nom and prc and cst and ext and rod:
                if existe(id):
                    actualizar(id, nom, prc, cst, ext, rod)
                    show_popup("Éxito", "Articulo actualizado correctamente")
                else:
                    show_popup("Error", f"El articulo con codigo {id} no existe")
            else:
                show_popup("Error", "Por favor completa todos los campos")

        def eliminar_articulo(instance):
            id = codigo_barras.text
            nom=nombre.text
            if id and nom:
                eliminar(id)
                show_popup("Éxito", "Articulo eliminado correctamente")
                # Limpiar campos
                codigo_barras.text = ""
                precio.text = ""
                precio.text = ""
                existencia.text = ""
            else:
                show_popup("Error", "Ingresa el ID y nombre del articulo a eliminar")

        # Botones
        boton_crear = Button(text='Crear',
                            background_color=(0, 0.5, 1, 1),
                            color=(1, 1, 1, 1),
                            pos_hint={'x': 0.1, 'y': 0.15},
                            size_hint=(0.2, 0.08))
        boton_crear.bind(on_press=crear_articulo)
        layout.add_widget(boton_crear)

        boton_actualizar = Button(text='Actualizar',
                                background_color=(0, 0.5, 1, 1),
                                color=(1, 1, 1, 1),
                                pos_hint={'x': 0.4, 'y': 0.15},
                                size_hint=(0.2, 0.08))
        boton_actualizar.bind(on_press=actualizar_articulo)
        layout.add_widget(boton_actualizar)

        boton_eliminar = Button(text='Eliminar',
                            background_color=(0, 0.5, 1, 1),
                            color=(1, 1, 1, 1),
                            pos_hint={'x': 0.7, 'y': 0.15},
                            size_hint=(0.2, 0.08))
        boton_eliminar.bind(on_press=eliminar_articulo)
        layout.add_widget(boton_eliminar)

        boton_consultar = Button(text='Consultar',
                                background_color=(0, 0.5, 1, 1),
                                color=(1, 1, 1, 1),
                                pos_hint={'x': 0.3, 'y': 0.03}, 
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
        precio.bind(text=limitar_telefono)

        def limitar_id(instance, value):
            if len(value) > 13:
                instance.text = value[:13]
        codigo_barras.bind(text=limitar_id)

        def sin_espacios(instance, value):
            if ' ' in value:
                instance.text = value.replace(' ', '')
        existencia.bind(text=sin_espacios)
        
        self.add_widget(layout)
        
    def volver_menu(self, instance):
        self.manager.current = 'menu'