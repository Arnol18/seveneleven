from kivy.app import App
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
def existe(id_categorias):
    query = "SELECT id_categorias FROM categoria WHERE telefono = %s"
    cursor.execute(query, (id_categorias,))
    return cursor.fetchone() is not None

def consultar():
    try:
        query = "SELECT codigo, nombre, precio, costo, existencias, reorden, id_categoria FROM articulo"
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
        grid = GridLayout(cols=7, size_hint_y=None, spacing=2)
        grid.bind(minimum_height=grid.setter('height'))
        
        # Encabezados
        for text in ["codigo", "nombre", "precio", "costo", "existencias", "reorden", "id_categoria"]:
            grid.add_widget(Label(text=text, bold=True, size_hint_y=None, height=40))
        
        # Datos
        for codigo, nombre, precio, costo, existencias, reorden, id_categoria in resultados:
            grid.add_widget(Label(text=str(codigo), size_hint_y=None, height=30))
            grid.add_widget(Label(text=nombre, size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(precio), size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(costo), size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(existencias), size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(reorden), size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(id_categoria), size_hint_y=None, height=30))
        
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
        
def insertar(id_categoria, nombre):
    query = "INSERT INTO categoria(id_categoria, nombre) VALUES (%s, %s)"
    valores = (id_categoria, nombre)
    cursor.execute(query, valores)
    conexion.commit()

def artibuto(id_categoria, articulo):
    query = "UPDATE articulo  SET id_categoria = (%s) WHERE codigo = '(%s)'"
    valores = (id_categoria, articulo)
    cursor.execute(query, valores)
    conexion.commit()
    
def atribuir(id_categoria, codigo):
    query = "UPDATE articulo SET id_categoria = %s WHERE codigo = %s"
    valores = (id_categoria, codigo)
    cursor.execute(query, valores)
    conexion.commit()

def eliminar(id_categorias):
    query = "DELETE FROM categoria WHERE id_categoria= %s"
    valores = (id_categorias)
    cursor.execute(query, valores)
    conexion.commit()

def leer():
    query = "SELECT codigo, nombre FROM articulo"
    cursor.execute(query)
    resultados = cursor.fetchall()
    return {nombre: codigo for codigo, nombre in resultados}
articulo_seleccionado = None

def articulo_select(spinner, text):
    global articulo_seleccionado
    articulo_seleccionado = articulos_dict.get(text)
    print(f'Seleccionaste: {text} (Código: {articulo_seleccionado})')

def cerrar():
    cursor.close()
    conexion.close()

# Interfaz
Window.clearcolor = (0.12, 0.12, 0.12, 1)
layout = FloatLayout()

# Título
layout.add_widget(Label(text='Catálogo de Categoria',
                        pos_hint={'x': 0.27, 'y': 0.87},
                        size_hint=(0.5, 0.1),
                        color=(1, 1, 1, 1),
                        font_size='24sp'))

# Campos de entrada
# ID
layout.add_widget(Label(text='ID categoria',
                        pos_hint={'x': 0.05, 'y': 0.75},
                        size_hint=(0.3, 0.1),
                        color=(1, 1, 1, 1),
                        font_size='18sp'))
id_categoria = TextInput(
                          background_color=(1, 1, 1, 1),
                          pos_hint={'x': 0.3, 'y': 0.77},
                          size_hint=(0.4, 0.05),
                          multiline=False)
layout.add_widget(id_categoria)

# Categoria
layout.add_widget(Label(text='Categoria',
                        pos_hint={'x': 0.05, 'y': 0.65},
                        size_hint=(0.3, 0.1),
                        color=(1, 1, 1, 1),
                        font_size='18sp'))
categoria = TextInput(
                        background_color=(1, 1, 1, 1),
                        pos_hint={'x': 0.3, 'y': 0.67},
                        size_hint=(0.4, 0.05),
                        multiline=False)
layout.add_widget(categoria)

# Articulo
articulos_dict = leer()

articulo_spinner = Spinner(text='Seleccionar',
                           values=list(articulos_dict.keys()), 
                           background_color=(0.8, 0.8, 0.8, 1),
                           color=(1, 1, 1, 1),
                           pos_hint={'x': 0.3, 'y': 0.57},
                           size_hint=(0.2, 0.05))

layout.add_widget(Label(text='Artículo',
                        pos_hint={'x': 0.05, 'y': 0.55},
                        size_hint=(0.3, 0.1),
                        color=(1, 1, 1, 1),
                        font_size='18sp'))
layout.add_widget(articulo_spinner)
articulo_spinner.bind(text=articulo_select)

# Funciones de los botones
def crear_categoria(instance):
    id = id_categoria.text
    nom = categoria.text
    if id and nom:
        insertar(id, nom)
        show_popup("Éxito", "Categoria creada correctamente")
    else:
        show_popup("Error", "Ingresa todos los campos correctamente")

def agregar_categoria(instance):
    id = id_categoria.text
    codigo = articulo_seleccionado
    if id and codigo:
        atribuir(id, codigo)
        show_popup("Éxito", "Categoria agregada correctamente")
    else:
        show_popup("Error", "Ingresa todos los campos correctamente")
    
def eliminar_categoria(instance):
    id = id_categoria.text
    if id:
        eliminar(id)
        show_popup("Éxito", "Categoria eliminado correctamente")
        # Limpiar campos
        id_categoria.text = ""
        categoria.text = ""
    else:
        show_popup("Error", "Ingresa el id de la categoria a eliminar")        

# Botones
boton_crear = Button(text='Crear',
                    background_color=(0, 0.5, 1, 1),
                    color=(1, 1, 1, 1),
                    pos_hint={'x': 0.1, 'y': 0.2},
                    size_hint=(0.2, 0.08))
boton_crear.bind(on_press=crear_categoria)
layout.add_widget(boton_crear)

boton_agregar = Button(text='Agregar',
                         background_color=(0, 0.5, 1, 1),
                         color=(1, 1, 1, 1),
                         pos_hint={'x': 0.4, 'y': 0.2},
                         size_hint=(0.2, 0.08))
boton_agregar.bind(on_press=agregar_categoria)
layout.add_widget(boton_agregar)

boton_eliminar = Button(text='Eliminar',
                       background_color=(0, 0.5, 1, 1),
                       color=(1, 1, 1, 1),
                       pos_hint={'x': 0.7, 'y': 0.2},
                       size_hint=(0.2, 0.08))
boton_eliminar.bind(on_press=eliminar_categoria)
layout.add_widget(boton_eliminar)

boton_consultar = Button(text='Consultar',
                        background_color=(0, 0.5, 1, 1),
                        color=(1, 1, 1, 1),
                        pos_hint={'x': 0.3, 'y': 0.08},  # Mismo x que boton_crear
                        size_hint=(0.4, 0.08))  # 0.6 = 0.7 (x de Eliminar) - 0.1 (x de Crear)
boton_consultar.bind(on_press=lambda x: consultar())
layout.add_widget(boton_consultar)


# App
class CatalogoArticuloApp(App):
    def build(self):
        return layout
CatalogoArticuloApp().run()