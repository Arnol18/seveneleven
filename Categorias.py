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
                          input_filter='int',
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
layout.add_widget(Label(text='Articulo',
                        pos_hint={'x': 0.05, 'y': 0.55},
                        size_hint=(0.3, 0.1),
                        color=(1, 1, 1, 1),
                        font_size='18sp'))
articulo = Spinner(
                      text='Seleccionar',
                      values=('1','2','3'),
                      background_color=(0.8, 0.8, 0.8, 1),
                      color=(1, 1, 1, 1),
                      pos_hint={'x': 0.3, 'y': 0.57},
                      size_hint=(0.2, 0.05))
layout.add_widget(articulo)

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
class CatalogoArticuloApp(App):
    def build(self):
        return layout
CatalogoArticuloApp().run()