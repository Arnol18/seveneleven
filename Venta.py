from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty, ListProperty
import mysql.connector
from mysql.connector import Error
import logging
from datetime import datetime

# Configuración de logging
logging.basicConfig(filename='errores_pos.log', level=logging.ERROR)

# Conexión a la base de datos
try:
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tienda"
    )
    cursor = conexion.cursor()
    print("Conexión exitosa a la base de datos")
except Error as e:
    print(f"Error al conectar a MySQL: {e}")
    conexion = None
    cursor = None

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
    id_empleado_actual = 1
    
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
        
        self.construir_ui()
        
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
        
        self.entrada_cliente = TextInput(text=self.cliente_var, multiline=False)
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
            query = "SELECT codigo, nombre, precio, existencias FROM articulo WHERE nombre LIKE %s OR codigo LIKE %s"
            cursor.execute(query, (f"%{termino_busqueda}%", f"%{termino_busqueda}%"))
            articulos = cursor.fetchall()
            
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
            cursor.execute("SELECT codigo, nombre, precio, existencias FROM articulo")
            articulos = cursor.fetchall()
            
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
        
        if len(articulo['codigo']) < 10:
            self.mostrar_mensaje("Error", f"Código inválido: {articulo['codigo']}")
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
                cursor.execute("SELECT existencias FROM articulo WHERE codigo = %s", (codigo,))
                existencias = cursor.fetchone()[0]
                
                if item['cantidad'] >= existencias:
                    self.mostrar_mensaje("Error", f"No hay suficientes existencias de {item['nombre']}")
                    return
                
                item['cantidad'] += 1
                break
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
    
    def _procesar_venta(self):
        if not self.articulos_carrito:
            self.mostrar_mensaje("Error", "No hay artículos en el carrito")
            return
        
        try:
            if conexion.in_transaction:
                conexion.rollback()

            for item in self.articulos_carrito:
                if len(item['codigo']) < 10:
                    self.mostrar_mensaje("Error", f"Código de producto inválido: {item['codigo']}")
                    return
                
                cursor.execute("SELECT existencias FROM articulo WHERE codigo = %s", (item['codigo'],))
                resultado = cursor.fetchone()
                if not resultado:
                    self.mostrar_mensaje("Error", f"Producto no encontrado: {item['codigo']}")
                    return
                
                if item['cantidad'] > resultado[0]:
                    self.mostrar_mensaje("Error", f"No hay suficientes existencias de {item['nombre']}")
                    return
            
            total = sum(item['precio'] * item['cantidad'] for item in self.articulos_carrito)
            
            telefono_cliente = self.entrada_cliente.text if self.entrada_cliente.text else None
            nombre_cliente = None
            
            if telefono_cliente:
                cursor.execute("SELECT nombre FROM cliente WHERE telefono = %s", (telefono_cliente,))
                cliente_result = cursor.fetchone()
                if cliente_result:
                    nombre_cliente = cliente_result[0]
            
            cursor.execute("SELECT id_empleado FROM empleado WHERE id_empleado = %s", (self.id_empleado_actual,))
            if not cursor.fetchone():
                self.mostrar_mensaje("Error", "Empleado no válido")
                return
            
            if not conexion.in_transaction:
                conexion.start_transaction()
            
            cursor.execute("""
                INSERT INTO venta (fecha, importe, telefono, id_empleado)
                VALUES (NOW(), %s, %s, %s)
            """, (total, telefono_cliente, self.id_empleado_actual))
            
            id_venta = cursor.lastrowid
            
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
                    INSERT INTO detalle_venta (id_venta, codigo, cantidad, subtotal)
                    VALUES (%s, %s, %s, %s)
                """, (id_venta, item['codigo'], item['cantidad'], subtotal))
                
                cursor.execute("""
                    UPDATE articulo
                    SET existencias = existencias - %s
                    WHERE codigo = %s
                """, (item['cantidad'], item['codigo']))
            
            conexion.commit()
            
            fecha_venta = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            ticket_data = {
                'id_venta': id_venta,
                'fecha': fecha_venta,
                'total': total,
                'id_empleado': self.id_empleado_actual,
                'articulos': articulos_venta,
                'cliente': nombre_cliente
            }
            
            self.mostrar_ticket(ticket_data)
            self.limpiar_carrito()
            self.cargar_productos()
            
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
            # Actualización de los datos
            conexion.commit()
            
            cursor.execute("SELECT nombre, telefono FROM cliente WHERE telefono = %s", (telefono,))
            resultado = cursor.fetchone()
            
            if resultado:
                nombre, telefono = resultado
                self.cliente_var = telefono  # Actualizar el campo de cliente
                self.entrada_cliente.text = telefono  # Asegurar que muestra el teléfono correcto
                self.mostrar_mensaje("Cliente encontrado", f"Nombre: {nombre}\nTeléfono: {telefono}")
            else:
                content = BoxLayout(orientation='vertical', spacing=10)
                content.add_widget(Label(text="Cliente no encontrado"))
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