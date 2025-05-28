from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout 
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from Venta import VentaScreen
from Articulo import ArticuloScreen
from Cliente import ClienteScreen
from Categorias import CategoriaScreen
from Proveedor import ProveedorScreen
from Unidad import UnidadScreen
from Empleado import EmpleadoScreen


class MenuScreen(Screen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Interfaz
        Window.clearcolor = (0.12, 0.12, 0.12, 1)
        layout = FloatLayout()

        # Título
        layout.add_widget(Label(
            text='Menu',
            pos_hint={'x': 0.26, 'y': 0.87},
            size_hint=(0.5, 0.1),
            color=(1, 1, 1, 1),
            font_size='24sp'
        ))
            
        boton_venta = Button(text='Venta',
                                background_color=(0, 0.5, 1, 1),
                                color=(1, 1, 1, 1),
                                pos_hint={'x': 0.36, 'y': 0.65},
                                size_hint=(0.3, 0.08),
        )
        boton_venta.bind(on_press=lambda instance: self.cambiar_pantalla('venta'))
        layout.add_widget(boton_venta)

       


        boton_articulo = Button(text='Articulo',
                                background_color=(0, 0.5, 1, 1),
                                color=(1, 1, 1, 1),
                                pos_hint={'x': 0.1, 'y': 0.5},
                                size_hint=(0.3, 0.08))
        boton_articulo.bind(on_press=lambda instance: self.cambiar_pantalla('articulo'))
        layout.add_widget(boton_articulo)

        boton_proveedor = Button(text='Proveedor',
                                background_color=(0, 0.5, 1, 1),
                                color=(1, 1, 1, 1),
                                pos_hint={'x': 0.6, 'y': 0.5},
                                size_hint=(0.3, 0.08))
        boton_proveedor.bind(on_press=lambda instance: self.cambiar_pantalla('proveedor'))
        layout.add_widget(boton_proveedor)

        boton_categoria = Button(text='Categoria',
                                background_color=(0, 0.5, 1, 1),
                                color=(1, 1, 1, 1),
                                pos_hint={'x': 0.1, 'y': 0.35},  # Mismo x que boton_crear
                                size_hint=(0.3, 0.08))  # 0.6 = 0.7 (x de Eliminar) - 0.1 (x de Crear)
        boton_categoria.bind(on_press=lambda instance: self.cambiar_pantalla('categoria'))
        layout.add_widget(boton_categoria)

        boton_unidad = Button(text='Unidad',
                                background_color=(0, 0.5, 1, 1),
                                color=(1, 1, 1, 1),
                                pos_hint={'x': 0.6, 'y': 0.35},
                                size_hint=(0.3, 0.08))
        boton_unidad.bind(on_press=lambda instance: self.cambiar_pantalla('unidad'))
        layout.add_widget(boton_unidad)

        boton_empleado = Button(text='Empleado',
                            background_color=(0, 0.5, 1, 1),
                            color=(1, 1, 1, 1),
                            pos_hint={'x': 0.1, 'y': 0.2},
                            size_hint=(0.3, 0.08))
        boton_empleado.bind(on_press=lambda instance: self.cambiar_pantalla('empleado'))
        layout.add_widget(boton_empleado)

        boton_cliente = Button(text='Cliente',
                            background_color=(0, 0.5, 1, 1),
                            color=(1, 1, 1, 1),
                            pos_hint={'x': 0.6, 'y': 0.2},
                            size_hint=(0.3, 0.08))
        boton_cliente.bind(on_press=lambda instance: self.cambiar_pantalla('cliente'))
        layout.add_widget(boton_cliente)
        self.add_widget(layout)
   
    def cambiar_pantalla(self, nombre):
        self.manager.current = nombre

class MenuApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(VentaScreen(name='venta'))
        sm.add_widget(ClienteScreen(name='compra'))
        sm.add_widget(ArticuloScreen(name='articulo'))
        sm.add_widget(ProveedorScreen(name='proveedor'))
        sm.add_widget(CategoriaScreen(name='categoria'))
        sm.add_widget(UnidadScreen(name='unidad'))
        sm.add_widget(EmpleadoScreen(name='empleado'))
        sm.add_widget(ClienteScreen(name='cliente'))
        return sm

MenuApp().run()