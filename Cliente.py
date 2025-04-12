from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.core.window import Window

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

# Validaciones
def limitar_id(instance, value):
    if len(value) > 10:
        instance.text = value[:10]
telefono.bind(text=limitar_id)

def sin_espacios(instance, value):
    if ' ' in value:
        instance.text = value.replace(' ', '')
correo.bind(text=sin_espacios)

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

# App
class CatalogoClienteApp(App):
    def build(self):
        return layout
CatalogoClienteApp().run()