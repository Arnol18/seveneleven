from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.clock import Clock
import mysql.connector
from mysql.connector import Error
import logging
from datetime import datetime

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="seveneleven"
)
if conexion.is_connected():
    cursor = conexion.cursor()
else:
    print("No se pudo conectar a la base de datos")
    
class BotonProducto(Button):
    datos_producto = ObjectProperty(None)

class TicketView(ModalView):
    def __init__(self, venta_data, **kwargs):
        super(TicketView, self).__init__(**kwargs)
        self.size_hint = (0.7, 0.8)
        self.title = f"Ticket #{venta_data['id_venta']}"
        
        scroll = ScrollView()
        layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5, padding=10)
        layout.bind(minimum_height=layout.setter('height'))
        
        # Fecha y número de ticket
        fecha = Label(text=f"Fecha: {venta_data['fecha']}\nTicket: {venta_data['id_venta']}", 
                    font_size='14sp', size_hint_y=None, height=60)
        layout.add_widget(fecha)
        
        # Línea divisoria
        linea = Label(text="-"*50, size_hint_y=None, height=20)
        layout.add_widget(linea)
        
        # Artículos
        for item in venta_data['articulos']:
            articulo_layout = BoxLayout(size_hint_y=None, height=30)
            articulo_layout.add_widget(Label(text=f"{item['cantidad']} x {item['nombre']}", 
                                          size_hint_x=0.7, halign='left', font_size='12sp'))
            articulo_layout.add_widget(Label(text=f"${item['subtotal']:.2f}", 
                                          size_hint_x=0.3, halign='right', font_size='12sp'))
            layout.add_widget(articulo_layout)
        
        # Línea divisoria
        linea = Label(text="-"*50, size_hint_y=None, height=20)
        layout.add_widget(linea)
        
        # Total
        total_layout = BoxLayout(size_hint_y=None, height=40)
        total_layout.add_widget(Label(text="TOTAL:", size_hint_x=0.7, font_size='16sp'))
        total_layout.add_widget(Label(text=f"${venta_data['total']:.2f}", 
                                   size_hint_x=0.3, font_size='16sp'))
        layout.add_widget(total_layout)
        
        # Método de pago
        metodo_layout = BoxLayout(size_hint_y=None, height=30)
        metodo_layout.add_widget(Label(text="Método:", size_hint_x=0.7, font_size='14sp'))
        metodo_layout.add_widget(Label(text=venta_data['metodo_pago'], 
                                    size_hint_x=0.3, font_size='14sp'))
        layout.add_widget(metodo_layout)
        
        # Mostrar pago y cambio solo si es efectivo
        if venta_data['metodo_pago'] == "Efectivo":
            pago_layout = BoxLayout(size_hint_y=None, height=30)
            pago_layout.add_widget(Label(text="Pago:", size_hint_x=0.6, font_size='12sp'))
            pago_layout.add_widget(Label(text=f"${venta_data['pago']:.2f}", 
                                  size_hint_x=0.3, font_size='12sp'))
            layout.add_widget(pago_layout)
            
            cambio_layout = BoxLayout(size_hint_y=None, height=30)
            cambio_layout.add_widget(Label(text="Cambio:", size_hint_x=0.6, font_size='12sp'))
            cambio_layout.add_widget(Label(text=f"${venta_data['cambio']:.2f}", 
                                       size_hint_x=0.3, font_size='12sp'))
            layout.add_widget(cambio_layout)
        
        # Cliente si existe
        if venta_data.get('cliente'):
            cliente_layout = BoxLayout(size_hint_y=None, height=40)
            cliente_layout.add_widget(Label(text="Cliente:", size_hint_x=0.7, font_size='14sp'))
            cliente_layout.add_widget(Label(text=venta_data['cliente'], 
                                        size_hint_x=0.3, font_size='14sp'))
            layout.add_widget(cliente_layout)
        
        # Botón para cerrar
        btn_cerrar = Button(text="Cerrar", size_hint_y=None, height=50)
        btn_cerrar.bind(on_press=self.dismiss)
        layout.add_widget(btn_cerrar)
        
        scroll.add_widget(layout)
        self.add_widget(scroll)

class VentaScreen(Screen):
    total_var = StringProperty("$0.00")
    cliente_var = StringProperty("")
    articulos_carrito = ListProperty([])
    id_empleado_actual = 1  # ID del admin por defecto porque no hay loging
    metodo_pago = StringProperty("Efectivo")
    pago_var = StringProperty("0.00")
    cambio_var = StringProperty("0.00")
    
    def __init__(self, **kwargs):
        super(VentaScreen, self).__init__(**kwargs)
        self.buscar_productos = self._buscar_productos
        self.cargar_productos = self._cargar_productos
        self.agregar_al_carrito = self._agregar_al_carrito
        self.actualizar_carrito = self._actualizar_carrito
        self.aumentar_cantidad = self._aumentar_cantidad
        self.disminuir_cantidad = self._disminuir_cantidad
        self.limpiar_carrito = self._limpiar_carrito
        self.procesar_venta = self._procesar_venta
        self.buscar_cliente = self._buscar_cliente
        self.volver = self.volver_menu
        self.mostrar_mensaje = self._mostrar_mensaje
        self.mostrar_ticket = self._mostrar_ticket
        
        # Variables para manejo de código de barras
        self.barcode_buffer = ""
        self.barcode_timeout = 0
        self.barcode_reading = False
        self.last_key_time = 0
        
        self.construir_ui()
        self._setup_barcode_listener()

    def _setup_barcode_listener(self):
        """Configura el listener para códigos de barras."""
        Window.bind(on_key_down=self._on_keyboard_down)
        Clock.schedule_interval(self._check_barcode_timeout, 0.1)

    def _on_keyboard_down(self, window, keycode, scancode, codepoint, modifiers):
        """Captura la entrada del teclado para detectar códigos de barras."""
        current_time = Clock.get_time()
        time_since_last_key = current_time - self.last_key_time
        self.last_key_time = current_time
        
        # Ignorar teclas modificadoras
        if modifiers:
            return
            
        # Determinar el caracter basado en keycode o codepoint
        char = codepoint if codepoint else chr(keycode) if keycode < 256 else ''
        
        # Si es un caracter imprimible y no es ENTER
        if char and char.isprintable() and char not in ('\r', '\n'):
            # Si ha pasado mucho tiempo desde la última tecla, reiniciar buffer
            if time_since_last_key > 0.5:  # Más de 500ms desde la última tecla
                self.barcode_buffer = ""
                self.barcode_reading = True
                
            self.barcode_buffer += char
            self.barcode_timeout = 0.3
        elif (keycode == 13 or scancode == 40) and self.barcode_reading:
            self._process_barcode()

    def _check_barcode_timeout(self, dt):
        """Verifica si ha pasado el tiempo máximo para completar un código de barras."""
        if self.barcode_reading and self.barcode_timeout > 0:
            self.barcode_timeout -= dt
            if self.barcode_timeout <= 0:
                self._process_barcode()

    def _process_barcode(self):
        """Procesa el código de barras capturado."""
        if not self.barcode_buffer:
            self.barcode_reading = False
            return
            
        codigo = self.barcode_buffer.strip()
        
        # Limpiar buffer y estado
        self.barcode_buffer = ""
        self.barcode_reading = False
        
        # Buscar el producto por código de barras
        self._buscar_producto_por_codigo(codigo)

    def _buscar_producto_por_codigo(self, codigo):
        """Busca un producto en la base de datos por su código de barras."""
        if not codigo:
            self.mostrar_mensaje("Error", "Código de barras vacío")
            return
            
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT codigo, nombre, precio, existencias FROM articulo WHERE codigo = %s", (codigo,))
            producto = cursor.fetchone()
            cursor.close()
            
            if producto:
                codigo, nombre, precio, existencias = producto
        
                # Crear el objeto producto como lo hace el botón
                datos_producto = {
                    'codigo': str(codigo),  # Asegurar que es string
                    'nombre': nombre,
                    'precio': float(precio),
                    'existencias': existencias
                }
                
                # Simular el click en el botón del producto
                fake_button = BotonProducto()
                fake_button.datos_producto = datos_producto
                self.agregar_al_carrito(fake_button)
                
            else:
                self.mostrar_mensaje("Código no encontrado", f"No existe producto con código: {codigo}")
                
        except Error as e:
            self.mostrar_mensaje("Error DB", f"No se pudo buscar producto: {e.msg}")

    def construir_ui(self):
        layout_principal = BoxLayout(orientation='horizontal', spacing=10, padding=10)
        
        # Frame izquierdo (productos)
        layout_izquierdo = BoxLayout(orientation='vertical', size_hint=(0.7, 1))
        
        # Búsqueda de productos
        layout_busqueda = BoxLayout(size_hint_y=None, height=40, spacing=5)
        layout_busqueda.add_widget(Label(text="Buscar:"))
        
        self.entrada_busqueda = TextInput(multiline=False)
        self.entrada_busqueda.bind(on_text_validate=self.buscar_productos)
        layout_busqueda.add_widget(self.entrada_busqueda)
        
        boton_buscar = Button(text="Buscar", size_hint_x=None, width=100)
        boton_buscar.bind(on_press=lambda x: self.buscar_productos())
        layout_busqueda.add_widget(boton_buscar)
        
        layout_izquierdo.add_widget(layout_busqueda)
        
        # Lista de productos con ScrollView
        scroll_productos = ScrollView()
        self.grid_productos = GridLayout(cols=4, size_hint_y=None, spacing=5, padding=5)
        self.grid_productos.bind(minimum_height=self.grid_productos.setter('height'))
        
        # Encabezados
        self.grid_productos.add_widget(Label(text="Producto", size_hint_y=None, height=30, bold=True))
        self.grid_productos.add_widget(Label(text="Código", size_hint_y=None, height=30, bold=True))
        self.grid_productos.add_widget(Label(text="Precio", size_hint_y=None, height=30, bold=True))
        self.grid_productos.add_widget(Label(text="Existencias", size_hint_y=None, height=30, bold=True))
        
        scroll_productos.add_widget(self.grid_productos)
        layout_izquierdo.add_widget(scroll_productos)
        
        # Frame derecho (carrito y total)
        layout_derecho = BoxLayout(orientation='vertical', size_hint=(0.3, 1))
        
        # Carrito de compras
        etiqueta_carrito = Label(text="Venta Actual", size_hint_y=None, height=30, font_size='14sp', bold=True)
        layout_derecho.add_widget(etiqueta_carrito)
        
        scroll_carrito = ScrollView()
        self.grid_carrito = GridLayout(cols=4, size_hint_y=None, spacing=5, padding=5)
        self.grid_carrito.bind(minimum_height=self.grid_carrito.setter('height'))
        
        # Encabezados del carrito
        self.grid_carrito.add_widget(Label(text="Producto", size_hint_y=None, height=30, bold=True))
        self.grid_carrito.add_widget(Label(text="Cant.", size_hint_y=None, height=30, bold=True))
        self.grid_carrito.add_widget(Label(text="Precio", size_hint_y=None, height=30, bold=True))
        self.grid_carrito.add_widget(Label(text="Subtotal", size_hint_y=None, height=30, bold=True))
        
        scroll_carrito.add_widget(self.grid_carrito)
        layout_derecho.add_widget(scroll_carrito)
        
        # Total
        layout_total = BoxLayout(size_hint_y=None, height=40)
        layout_total.add_widget(Label(text="Total:", font_size='14sp', bold=True))
        self.etiqueta_total = Label(text=self.total_var, font_size='14sp', bold=True)
        layout_total.add_widget(self.etiqueta_total)
        layout_derecho.add_widget(layout_total)
        
        # Método de pago
        layout_metodo_pago = BoxLayout(size_hint_y=None, height=40, spacing=5)
        layout_metodo_pago.add_widget(Label(text="Método:", size_hint_x=0.3))
        
        self.spinner_pago = Spinner(
            text=self.metodo_pago,
            values=('Efectivo', 'Tarjeta'),
            size_hint_x=0.7
        )
        self.spinner_pago.bind(text=self._on_metodo_pago_change)
        layout_metodo_pago.add_widget(self.spinner_pago)
        layout_derecho.add_widget(layout_metodo_pago)
        
        # Pago y cambio (solo visible para efectivo)
        self.layout_pago_cambio = BoxLayout(size_hint_y=None, height=30, spacing=20)
        self.layout_pago_cambio.add_widget(Label(text="Paga con:", size_hint_x=0.25))
        
        self.entrada_pago = TextInput(
            text=self.pago_var,
            multiline=False,
            input_filter='float',
            hint_text="0.00"
        )
        self.entrada_pago.bind(text=self._calcular_cambio)
        self.layout_pago_cambio.add_widget(self.entrada_pago)
        
        self.layout_pago_cambio.add_widget(Label(text="Cambio:", size_hint_x=0.3))
        self.etiqueta_cambio = Label(text=self.cambio_var, size_hint_x=0.4)
        self.layout_pago_cambio.add_widget(self.etiqueta_cambio)
        layout_derecho.add_widget(self.layout_pago_cambio)
        
        # Botones de acción
        layout_botones = BoxLayout(size_hint_y=None, height=50, spacing=5)
        boton_cancelar = Button(text="Cancelar Venta", background_color=(0.96, 0.26, 0.21, 1))
        boton_cancelar.bind(on_press=lambda x: self.limpiar_carrito())
        layout_botones.add_widget(boton_cancelar)
        
        boton_procesar = Button(text="Procesar Venta", background_color=(0.3, 0.69, 0.31, 1))
        boton_procesar.bind(on_press=lambda x: self.procesar_venta())
        layout_botones.add_widget(boton_procesar)
        
        layout_derecho.add_widget(layout_botones)
        
        # Cliente
        layout_cliente = BoxLayout(orientation='vertical', size_hint_y=None, height=100)
        layout_cliente.add_widget(Label(text="Cliente:"))
        
        self.entrada_cliente = TextInput(text=self.cliente_var, multiline=False, hint_text="9619999999 para cliente general")
        layout_cliente.add_widget(self.entrada_cliente)
        
        layout_botones_cliente = BoxLayout(size_hint_y=None, height=40, spacing=5)
        boton_buscar_cliente = Button(text="Buscar")
        boton_buscar_cliente.bind(on_press=lambda x: self.buscar_cliente())
        layout_botones_cliente.add_widget(boton_buscar_cliente)
        
        boton_volver = Button(text="Volver", background_color=(1, 0, 0, 1))
        boton_volver.bind(on_press=lambda x: self.volver())
        layout_botones_cliente.add_widget(boton_volver)
        
        layout_cliente.add_widget(layout_botones_cliente)
        layout_derecho.add_widget(layout_cliente)
        
        # Ensamblar layout principal
        layout_principal.add_widget(layout_izquierdo)
        layout_principal.add_widget(layout_derecho)
        
        self.add_widget(layout_principal)
        self.cargar_productos()
        self._on_metodo_pago_change(self.spinner_pago, self.spinner_pago.text)
        
        # Asegurarse que ningún campo tiene el foco inicialmente
        self.entrada_busqueda.focus = False
        self.entrada_cliente.focus = False

    def _usar_cliente_general(self):
        """Establece el cliente general como cliente actual."""
        self.entrada_cliente.text = "9619999999"
        self.entrada_cliente.background_color = (0.9, 0.9, 0.9, 1)  # Fondo gris claro
        self.mostrar_mensaje("Cliente General", "Se ha establecido el cliente general para esta venta")

    def _on_metodo_pago_change(self, spinner, text):
        """Maneja el cambio en el método de pago"""
        self.metodo_pago = text
        if text == "Efectivo":
            self.layout_pago_cambio.opacity = 1
            self.layout_pago_cambio.disabled = False
            self._calcular_cambio(self.entrada_pago, self.entrada_pago.text)
        else:
            self.layout_pago_cambio.opacity = 0
            self.layout_pago_cambio.disabled = True
            self.cambio_var = "0.00"
            self.etiqueta_cambio.text = self.cambio_var

    def _calcular_cambio(self, instance, text):
        """Calcula el cambio cuando el pago es en efectivo"""
        if self.metodo_pago != "Efectivo":
            return
            
        try:
            total = float(self.total_var.replace("$", "").strip())
            pago = float(text) if text else 0.0
            
            if pago >= total:
                cambio = pago - total
                self.cambio_var = f"{cambio:.2f}"
            else:
                self.cambio_var = "0.00"
                
            self.etiqueta_cambio.text = self.cambio_var
        except ValueError:
            self.cambio_var = "0.00"
            self.etiqueta_cambio.text = self.cambio_var

    def _buscar_productos(self, instance=None):
        termino_busqueda = self.entrada_busqueda.text
        if not termino_busqueda:
            self.cargar_productos()
            return
        
        self.grid_productos.clear_widgets()
        self.grid_productos.add_widget(Label(text="Producto", size_hint_y=None, height=30, bold=True))
        self.grid_productos.add_widget(Label(text="Código", size_hint_y=None, height=30, bold=True))
        self.grid_productos.add_widget(Label(text="Precio", size_hint_y=None, height=30, bold=True))
        self.grid_productos.add_widget(Label(text="Existencias", size_hint_y=None, height=30, bold=True))
        
        try:
            cursor = conexion.cursor()
            query = "SELECT codigo, nombre, precio, existencias FROM articulo WHERE nombre LIKE %s OR codigo LIKE %s"
            cursor.execute(query, (f"%{termino_busqueda}%", f"%{termino_busqueda}%"))
            articulos = cursor.fetchall()
            cursor.close()
            
            for articulo in articulos:
                codigo, nombre, precio, existencias = articulo
                
                boton_nombre = BotonProducto(text=nombre, size_hint_y=None, height=40)
                boton_nombre.datos_producto = {
                    'codigo': codigo,
                    'nombre': nombre,
                    'precio': float(precio),
                    'existencias': existencias
                }
                boton_nombre.bind(on_press=self.agregar_al_carrito)
                
                self.grid_productos.add_widget(boton_nombre)
                self.grid_productos.add_widget(Label(text=codigo, size_hint_y=None, height=40))
                self.grid_productos.add_widget(Label(text=f"${precio:.2f}", size_hint_y=None, height=40))
                self.grid_productos.add_widget(Label(text=str(existencias), size_hint_y=None, height=40))
                
        except Error as e:
            self.mostrar_mensaje("Error DB", f"Error en búsqueda: {e.msg}")

    def _cargar_productos(self):
        self.grid_productos.clear_widgets()
        
        self.grid_productos.add_widget(Label(text="Producto", size_hint_y=None, height=30, bold=True))
        self.grid_productos.add_widget(Label(text="Código", size_hint_y=None, height=30, bold=True))
        self.grid_productos.add_widget(Label(text="Precio", size_hint_y=None, height=30, bold=True))
        self.grid_productos.add_widget(Label(text="Existencias", size_hint_y=None, height=30, bold=True))
        
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT codigo, nombre, precio, existencias FROM articulo")
            articulos = cursor.fetchall()
            cursor.close()
            
            for articulo in articulos:
                codigo, nombre, precio, existencias = articulo
                
                boton_nombre = BotonProducto(text=nombre, size_hint_y=None, height=40)
                boton_nombre.datos_producto = {
                    'codigo': codigo,
                    'nombre': nombre,
                    'precio': float(precio),
                    'existencias': existencias
                }
                boton_nombre.bind(on_press=self.agregar_al_carrito)
                
                self.grid_productos.add_widget(boton_nombre)
                self.grid_productos.add_widget(Label(text=codigo, size_hint_y=None, height=40))
                self.grid_productos.add_widget(Label(text=f"${precio:.2f}", size_hint_y=None, height=40))
                self.grid_productos.add_widget(Label(text=str(existencias), size_hint_y=None, height=40))
                
        except Error as e:
            self.mostrar_mensaje("Error DB", f"No se pudieron cargar productos: {e.msg}")

    def _agregar_al_carrito(self, instance):
        articulo = instance.datos_producto
        
        # Validación modificada para códigos de barras
        if not articulo['codigo'] or not articulo['codigo'].strip():
            self.mostrar_mensaje("Error", "Código de producto vacío")
            return
        
        for item in self.articulos_carrito:
            if item['codigo'] == articulo['codigo']:
                if item['cantidad'] >= articulo['existencias']:
                    self.mostrar_mensaje("Error", f"No hay suficientes existencias de {articulo['nombre']}")
                    return
                
                item['cantidad'] += 1
                self.actualizar_carrito()
                return
        
        if articulo['existencias'] <= 0:
            self.mostrar_mensaje("Error", f"No hay existencias de {articulo['nombre']}")
            return
        
        articulo['cantidad'] = 1
        self.articulos_carrito.append(articulo)
        self.actualizar_carrito()

    def _actualizar_carrito(self):
        self.grid_carrito.clear_widgets()
        self.grid_carrito.add_widget(Label(text="Producto", size_hint_y=None, height=30, bold=True))
        self.grid_carrito.add_widget(Label(text="Cant.", size_hint_y=None, height=30, bold=True))
        self.grid_carrito.add_widget(Label(text="Precio", size_hint_y=None, height=30, bold=True))
        self.grid_carrito.add_widget(Label(text="Subtotal", size_hint_y=None, height=30, bold=True))
        
        total = 0
        
        for item in self.articulos_carrito:
            subtotal = item['precio'] * item['cantidad']
            total += subtotal
            
            self.grid_carrito.add_widget(Label(text=item['nombre'], size_hint_y=None, height=40))
            
            layout_cantidad = BoxLayout(size_hint_y=None, height=40)
            
            boton_decrementar = Button(text="-", size_hint_x=None, width=20, size_hint_y=None, height=35)
            boton_decrementar.codigo_item = item['codigo']
            boton_decrementar.bind(on_press=self.disminuir_cantidad)
            layout_cantidad.add_widget(boton_decrementar)
            
            layout_cantidad.add_widget(Label(text=str(item['cantidad']), size_hint_y=None, height=40))
            
            boton_incrementar = Button(text="+", size_hint_x=None, width=20, size_hint_y=None, height=35)
            boton_incrementar.codigo_item = item['codigo']
            boton_incrementar.bind(on_press=self.aumentar_cantidad)
            layout_cantidad.add_widget(boton_incrementar)
            
            self.grid_carrito.add_widget(layout_cantidad)
            self.grid_carrito.add_widget(Label(text=f"${item['precio']:.2f}", size_hint_y=None, height=40))
            self.grid_carrito.add_widget(Label(text=f"${subtotal:.2f}", size_hint_y=None, height=40))
        
        self.total_var = f"${total:.2f}"
        self.etiqueta_total.text = self.total_var

    def _aumentar_cantidad(self, instance):
        codigo = instance.codigo_item
        for item in self.articulos_carrito:
            if item['codigo'] == codigo:
                try:
                    cursor = conexion.cursor()
                    cursor.execute("SELECT existencias FROM articulo WHERE codigo = %s", (codigo,))
                    existencias = cursor.fetchone()[0]
                    cursor.close()
                    
                    if item['cantidad'] >= existencias:
                        self.mostrar_mensaje("Error", f"No hay suficientes existencias de {item['nombre']}")
                        return
                    
                    item['cantidad'] += 1
                    break
                except Error as e:
                    self.mostrar_mensaje("Error DB", f"No se pudo verificar existencias: {e.msg}")
                    return
        self.actualizar_carrito()

    def _disminuir_cantidad(self, instance):
        codigo = instance.codigo_item
        for item in self.articulos_carrito:
            if item['codigo'] == codigo:
                if item['cantidad'] > 1:
                    item['cantidad'] -= 1
                else:
                    self.articulos_carrito.remove(item)
                break
        self.actualizar_carrito()

    def _limpiar_carrito(self):
        self.articulos_carrito = []
        self.actualizar_carrito()
    
    def _limpiar_venta_completa(self):
        """Limpia todos los campos relacionados con la venta actual"""
        self.limpiar_carrito()
        self.cargar_productos()
        
        # Resetear campos de pago
        self.entrada_pago.text = "0.00"
        self.pago_var = "0.00"
        self.cambio_var = "0.00"
        self.etiqueta_cambio.text = "0.00"
        
        # Resetear cliente
        self.entrada_cliente.text = ""
        self.entrada_cliente.background_color = (1, 1, 1, 1)
        
        # Resetear método de pago a Efectivo
        self.spinner_pago.text = "Efectivo"
        self._on_metodo_pago_change(self.spinner_pago, "Efectivo")

    def _procesar_venta(self):
        if not self.articulos_carrito:
            self.mostrar_mensaje("Error", "No hay artículos en el carrito")
            return
        
        # Validar pago si es en efectivo
        if self.metodo_pago == "Efectivo":
            try:
                total = float(self.total_var.replace("$", "").strip())
                pago = float(self.entrada_pago.text) if self.entrada_pago.text else 0.0
                
                if pago < total:
                    self.mostrar_mensaje("Error", f"El pago (${pago:.2f}) es menor al total (${total:.2f})")
                    return
            except ValueError:
                self.mostrar_mensaje("Error", "Monto de pago inválido")
                return
        
        try:
            if conexion.in_transaction:
                conexion.rollback()

            # Validar existencias
            for item in self.articulos_carrito:
                if not item['codigo'] or not item['codigo'].strip():
                    self.mostrar_mensaje("Error", "Código de producto inválido")
                    return
                
                cursor = conexion.cursor()
                cursor.execute("SELECT existencias FROM articulo WHERE codigo = %s", (item['codigo'],))
                resultado = cursor.fetchone()
                cursor.close()
                
                if not resultado:
                    self.mostrar_mensaje("Error", f"Producto no encontrado: {item['codigo']}")
                    return
                
                if item['cantidad'] > resultado[0]:
                    self.mostrar_mensaje("Error", f"No hay suficientes existencias de {item['nombre']}")
                    return
            
            total = sum(item['precio'] * item['cantidad'] for item in self.articulos_carrito)
            
            # Obtener datos del cliente - si no se especifica, usar cliente general
            telefono_cliente = self.entrada_cliente.text.strip() if self.entrada_cliente.text else '9619999999'
            nombre_cliente = "Cliente General"  # Valor por defecto
            
            # Verificar si el cliente existe en la BD (excepto para el cliente general)
            if telefono_cliente != '9619999999':
                cursor = conexion.cursor()
                cursor.execute("SELECT nombre FROM cliente WHERE telefono = %s", (telefono_cliente,))
                cliente_result = cursor.fetchone()
                cursor.close()
                
                if cliente_result:
                    nombre_cliente = cliente_result[0]
                else:
                    self.mostrar_mensaje("Aviso", "Cliente no encontrado. Se usará cliente general.")
                    telefono_cliente = '9619999999'
                    nombre_cliente = "Cliente General"
                pago_var.txt = StringProperty("0.00")
            
            # Validar empleado
            cursor = conexion.cursor()
            cursor.execute("SELECT id_empleado FROM empleado WHERE id_empleado = %s", (self.id_empleado_actual,))
            if not cursor.fetchone():
                cursor.close()
                self.mostrar_mensaje("Error", "Empleado no válido")
                return
            cursor.close()
            
            # Iniciar transacción
            if not conexion.in_transaction:
                conexion.start_transaction()
            
            # Obtener el cambio si es pago en efectivo
            cambio = 0.0
            pago = total
            if self.metodo_pago == "Efectivo":
                pago = float(self.entrada_pago.text)
                cambio = pago - total
            
            # Insertar en tabla venta
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO venta (fecha, tipo, metodo_pago, pago, cambio, importe, nombre_cliente, telefono, id_empleado) VALUES (
                    NOW(), 'Ticket', %s, %s, %s, %s, %s, %s, %s)""", 
                    (self.metodo_pago,pago,cambio,total,nombre_cliente,telefono_cliente, self.id_empleado_actual))
            
            id_venta = cursor.lastrowid
            
            # Insertar detalles de venta
            articulos_venta = []
            for item in self.articulos_carrito:
                subtotal = item['precio'] * item['cantidad']
                articulos_venta.append({
                    'codigo': item['codigo'],
                    'nombre': item['nombre'],
                    'precio': item['precio'],
                    'cantidad': item['cantidad'],
                    'subtotal': subtotal
                })
                
                cursor.execute("""
                    INSERT INTO detalle_venta (id_venta, codigo, precio_unitario, cantidad, subtotal) VALUES (
                        %s, %s, %s, %s, %s)""", 
                        (id_venta,item['codigo'],item['precio'],item['cantidad'],subtotal))
                
                # Actualizar existencias
                cursor.execute("""
                    UPDATE articulo
                    SET existencias = existencias - %s
                    WHERE codigo = %s
                """, (item['cantidad'], item['codigo']))
            
            conexion.commit()
            cursor.close()
            
            # Preparar datos para el ticket
            fecha_venta = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            ticket_data = {
                'id_venta': id_venta,
                'fecha': fecha_venta,
                'total': total,
                'metodo_pago': self.metodo_pago,
                'pago': pago,
                'cambio': cambio,
                'id_empleado': self.id_empleado_actual,
                'articulos': articulos_venta,
                'cliente': nombre_cliente
            }
            
            self.mostrar_ticket(ticket_data)
            self.limpiar_carrito()
            self._limpiar_venta_completa()
            self.cargar_productos()
            
            # Resetear campo de cliente
            self.entrada_cliente.text = ""
            self.entrada_cliente.background_color = (1, 1, 1, 1)  # Fondo blanco
            
        except Error as e:
            if conexion.in_transaction:
                conexion.rollback()
            logging.error(f"Error SQL al procesar venta: {e}")
            self.mostrar_mensaje("Error DB", f"Código: {e.errno}\nMensaje: {e.msg}")
        except Exception as e:
            if conexion.in_transaction:
                conexion.rollback()
            logging.error(f"Error inesperado: {e}")
            self.mostrar_mensaje("Error", f"Error inesperado: {str(e)}")

    def _buscar_cliente(self):
        telefono = self.entrada_cliente.text.strip()
        if not telefono:
            self.mostrar_mensaje("Buscar cliente", "Ingrese un número de teléfono")
            return
        
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, telefono FROM cliente WHERE telefono = %s", (telefono,))
            resultado = cursor.fetchone()
            cursor.close()
            
            if resultado:
                nombre, telefono = resultado
                self.cliente_var = telefono
                self.entrada_cliente.text = telefono
                self.entrada_cliente.background_color = (0.8, 0.95, 0.8, 1)  # Fondo verde claro
                self.mostrar_mensaje("Cliente encontrado", f"Nombre: {nombre}\nTeléfono: {telefono}")
            else:
                self.mostrar_mensaje("Cliente no encontrado", "No existe cliente con este teléfono")
                self.entrada_cliente.background_color = (0.95, 0.8, 0.8, 1)  # Fondo rojo claro
                
        except Error as e:
            self.mostrar_mensaje("Error DB", f"No se pudo buscar cliente: {e.msg}") 
            
    def _mostrar_ticket(self, ticket_data):
        ticket_view = TicketView(ticket_data)
        ticket_view.open()
    
    def volver_menu(self):
        self.manager.current = 'menu'
    
    def _mostrar_mensaje(self, titulo, mensaje):
        popup = Popup(title=titulo,
                     content=Label(text=mensaje),
                     size_hint=(None, None), size=(400, 200))
        popup.open()

    def on_leave(self, *args):
        """Limpiar el carrito al salir de la pantalla"""
        self.limpiar_carrito()
        return super().on_leave(*args)