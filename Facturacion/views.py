from django.shortcuts import render
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from .models import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse	
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages
import json as simplejson
from Cliente.models import *
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import View
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from Demanda.models import *
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


#Demanda
def guardar_datos_demanda(dia, mes, ano, presentacion_id, cantidad):
    
    #Se procesa la fecha para sacar la referencia
    
    #Listado_Productos.objects.filter(referencia_periodo = "1-2016").delete()
    #Listado_Productos.objects.filter(referencia_periodo = "2-2016").delete()
    

    
    periodo = 0
    
    if int(mes) >= 1 and int(mes) <= 4:
        periodo = 1
    elif int(mes) > 4 and int(mes) <= 8:
        periodo = 2
    else:
        periodo = 3
        
    #referencia_actual = str(periodo) + "-" + str(ano)
    referencia_actual = "1-2017"
    
    if periodo <= 2:
        periodo = periodo + 1
    
    else:
        periodo = 1
        ano = int(ano) + 1
        
    #referencia_futura = str(periodo) + "-" + str(ano)
    referencia_futura = "2-2017"
    
    #Se traen los listados del periodo actual y el futuro, y se calcula los pronosticos
    
    listado_productos_actual = Listado_Productos.objects.get(referencia_periodo = referencia_actual)
    
    #Si el futuro existe vs No existe
    try: 
        #Si existe
        listado_productos_futuro = Listado_Productos.objects.get(referencia_periodo = referencia_futura)
        
    except:
        
        #Si no existe, se crea y se crean todos sus productos.
        listado_productos_futuro = Listado_Productos(referencia_periodo = referencia_futura)
        listado_productos_futuro.save()
        
        productos = Producto.objects.all()
        productos_actuales = listado_productos_actual.productos
        
        
        for producto in productos:
            
            if producto.tipo == "Lubricantes Industriales":
                tipo_contenido = "Litros"
            elif producto.tipo == "Grasa":
                tipo_contenido = "Libras"
            elif producto.tipo == "Aditivos":
                tipo_contenido = "Litros"
            elif producto.tipo == "Soldadura para Antorcha":
                tipo_contenido = "Libras"
            elif producto.tipo == "Soldadura para Arco":
                tipo_contenido = "Libras"
            else:
                tipo_contenido = "Litros"
                
            #Aqui habra un error cuando en el listado de productos nuevo exista un producto que no este en el listado viejo
            #Esto ayudaria con un producto nuevo, try except, para uno desactivado queda pendiente cuando se factura.
            try:
                #Si existe el producto en el periodo actual, se crea SOLO en el futuro
                producto_pasado = productos_actuales.get(producto = producto)
                        
                pronostico = float(producto_pasado.pronostico) + 0.5*(float(producto_pasado.cantidad) - float(producto_pasado.pronostico))
                
                producto_importacion = Producto_Importacion(tipo_contenido = tipo_contenido, producto = producto, pronostico = pronostico)
                producto_importacion.save()
                listado_productos_futuro.productos.add(producto_importacion)
                
            except:
                
                
                #Si no existe el producto en el periodo actual, se crea en el actual y en el futuro
                producto_importacion = Producto_Importacion(tipo_contenido = tipo_contenido, producto = producto, pronostico = producto.pronostico_inicial)
                producto_importacion.save()
                listado_productos_actual.productos.add(producto_importacion)
                listado_productos_actual.save()
                
                producto_importacion = Producto_Importacion(tipo_contenido = tipo_contenido, producto = producto, pronostico = producto.pronostico_inicial)
                producto_importacion.save()
                listado_productos_futuro.productos.add(producto_importacion)
            
        listado_productos_futuro.save()
        
    
    #Una vez los dos periodos necesarios para los calculos estan listos, procedemos a convertir todo a las mismas unidades ()
    
    for x in range (0, len(cantidad)):
        
        #Se consultan todos los datos necesarios
        presentacion = Presentacion.objects.get(id=presentacion_id[x])
        cantidad_producto = cantidad[x]
        producto = presentacion.producto
        cantidad_presentacion = presentacion.numero_elementos
        
        
        productos_actual = listado_productos_actual.productos
        productos_futuro = listado_productos_futuro.productos
        
        #Aqui se asume que los productos estan tanto en el presente como el futuro, algo que podria no pasar.
        try:
            producto_importacion_actual = productos_actual.get(producto = producto)
            producto_importacion_futuro = productos_futuro.get(producto = producto)
            
        except:
            
            if producto.tipo == "Lubricantes Industriales":
                tipo_contenido = "Litros"
            elif producto.tipo == "Grasa":
                tipo_contenido = "Libras"
            elif producto.tipo == "Aditivos":
                tipo_contenido = "Litros"
            elif producto.tipo == "Soldadura para Antorcha":
                tipo_contenido = "Libras"
            elif producto.tipo == "Soldadura para Arco":
                tipo_contenido = "Libras"
            else:
                tipo_contenido = "Litros"
                    
            producto_importacion = Producto_Importacion(tipo_contenido = tipo_contenido, producto = producto, pronostico = producto.pronostico_inicial)
            producto_importacion.save()
            listado_productos_actual.productos.add(producto_importacion)
            listado_productos_actual.save()
            producto_importacion_actual = producto_importacion
            
            producto_importacion_f = Producto_Importacion(tipo_contenido = tipo_contenido, producto = producto, pronostico = producto.pronostico_inicial)
            producto_importacion_f.save()
            listado_productos_futuro.productos.add(producto_importacion_f)
            listado_productos_futuro.save()
            producto_importacion_futuro = producto_importacion_f
         
        #Se transforma todo a las mismas unidades de cantidad
        cantidad_unidad_medida = presentacion.cantidad
        unidad_medida = presentacion.tipo_cantidad
        
        
        if unidad_medida == "mL":
            cantidad_unidad_medida = (int(cantidad_unidad_medida) * int(cantidad_presentacion) * int(cantidad_producto))/1000
        else:
            cantidad_unidad_medida = (int(cantidad_unidad_medida) * int(cantidad_presentacion) * int(cantidad_producto))
            
        
        producto_importacion_actual.cantidad = float(cantidad_unidad_medida) + float(producto_importacion_actual.cantidad)
        producto_importacion_actual.save()
        
        producto_importacion_futuro.pronostico = float(producto_importacion_actual.pronostico) + 0.5*(float(producto_importacion_actual.cantidad) - float(producto_importacion_actual.pronostico))
        
        producto_importacion_futuro.save()
        
        
# Facturacion

class generarCotizacion(TemplateView):
    
    def get(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
        
        usuario = request.user
        carrito = Carrito.objects.get(encargado=usuario)
        
        try:
            id_cliente = carrito.cliente
            cliente = Cliente.objects.get(nit=id_cliente)
            id_contacto = carrito.contacto
            contacto = Contacto.objects.get(id=id_contacto)
            
        except:
            clientes = Cliente.objects.all()
            pag = Paginate(request, clientes, 10)
            
            cxt = {
                'posts': pag['queryset'],
                'totPost': clientes,
                'paginator': pag
            }
            
            messages.add_message(request, messages.ERROR, "No tiene seleccionado un Cliente, agregue uno a facturacion")
    
            
            return render_to_response('listar_clientes.html',cxt,
                	context_instance=RequestContext(request))
            
        presentaciones = carrito.presentaciones
        
        subtotal = 0
        
        for presentacion in presentaciones.all():
            subtotal = subtotal + presentacion.precio
        
        iva = (subtotal*19)/100    
        total = subtotal + iva
    	return render_to_response('generar_cotizacion.html',{'carrito':carrito, 'contacto':contacto, 'cliente':cliente, 'subtotal':subtotal, 
    	    'iva':iva, 'total':total, 'tipo' : 'cotizacion'},
    			context_instance=RequestContext(request))
    			

    def post(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))

        
        cliente_id = request.POST['cliente_id']
        total_input = request.POST['total-input']
        iva = request.POST['iva']
        contacto_id = request.POST['contacto_id']
        subtotal = request.POST['sub']
        validez_oferta = request.POST['validez_oferta']
        condicion_pago = request.POST['condicion_pago']
        tiempo_entrega = request.POST['tiempo_entrega']
        
        #Traen los datos de la tabla 2
        cantidad = request.POST.getlist('cantidad')
        precio_unidad = request.POST.getlist('precio_unidad')
        presentacion_id = request.POST.getlist('presentacion_id')
        
        #Se crea el objeto Facturacion deseado
        contacto = Contacto.objects.get(id=contacto_id)
        cliente = Cliente.objects.get(nit = cliente_id)
        
        
        cotizacion = Cotizacion(validez_oferta = validez_oferta, tiempo_entrega = tiempo_entrega, condicion_pago=condicion_pago, contacto = contacto.nombre, cliente = cliente, encargado = (request.user.first_name + request.user.last_name), subtotal = subtotal, iva = iva, 
        total = total_input)
        
        cotizacion.save()
        
        for x in range (0, len(cantidad)):
            
            presentacion = Presentacion.objects.get(id=presentacion_id[x])
            cantidad_presentacion = cantidad[x]
            precio_unidad_presentacion = precio_unidad[x]
            precio_unidad_total = int(cantidad_presentacion) * int(precio_unidad_presentacion)
            
            presentacion_declarada = PresentacionDeclarada(presentacion = presentacion, cantidad = cantidad_presentacion, 
            precio_unidad = precio_unidad_presentacion, precio_total = precio_unidad_total)
            
            presentacion_declarada.save()
            
            
            cotizacion.presentaciones.add(presentacion_declarada)
            
        cotizacion.save()
        
        return redirect("facturacion:generarCotizacion_pdf", id_cotizacion=cotizacion.id)
        
class generarFactura(TemplateView):
    
    def get(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
        
        
        facturas = Factura.objects.all()
        cantidad_facturas = len(facturas)
        
        if cantidad_facturas != 0:
            ultima_factura = facturas[cantidad_facturas-1]
            consecutivo_ultima = ultima_factura.consecutivo
            consecutivo_ultima = int(consecutivo_ultima) + 1
            consecutivo = str(consecutivo_ultima)
        else:
            consecutivo = "1"
        
        usuario = request.user
        carrito = Carrito.objects.get(encargado=usuario)
        
        try:
            id_cliente = carrito.cliente
            cliente = Cliente.objects.get(nit=id_cliente)
            id_contacto = carrito.contacto
            contacto = Contacto.objects.get(id=id_contacto)
            
        except:
            clientes = Cliente.objects.all()
            pag = Paginate(request, clientes, 10)
            
            cxt = {
                'posts': pag['queryset'],
                'totPost': clientes,
                'paginator': pag
            }
            
            messages.add_message(request, messages.ERROR, "No tiene seleccionado un Cliente, agregue uno a facturacion")
    
            
            return render_to_response('listar_clientes.html',cxt,
                	context_instance=RequestContext(request))
        
        presentaciones = carrito.presentaciones
        
        subtotal = 0
        
        for presentacion in presentaciones.all():
            subtotal = subtotal + presentacion.precio
        
        iva = (subtotal*19)/100    
        total = subtotal + iva
    
        
    	return render_to_response('generar_factura.html',{'consecutivo': consecutivo, 'carrito':carrito, 'contacto':contacto, 'cliente':cliente, 'subtotal':subtotal, 
    	    'iva':iva, 'total':total, 'tipo':'factura'},
    			context_instance=RequestContext(request))
    			

    def post(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
        
        
        cliente_id = request.POST['cliente_id']
        total_input = request.POST['total-input']
        iva = request.POST['iva']
        contacto_id = request.POST['contacto_id']
        subtotal = request.POST['sub']
        validez_oferta = request.POST['validez_oferta']
        condicion_pago = request.POST['condicion_pago']
        tiempo_entrega = request.POST['tiempo_entrega']
        consecutivo = request.POST['consecutivo']
        #Se capta la fecha
        #fecha = request.POST['fecha']

        
        #Traen los datos de la tabla 2
        cantidad = request.POST.getlist('cantidad')
        precio_unidad = request.POST.getlist('precio_unidad')
        presentacion_id = request.POST.getlist('presentacion_id')
        
        #Se crea el objeto Facturacion deseado
        contacto = Contacto.objects.get(id=contacto_id)
        cliente = Cliente.objects.get(nit = cliente_id)
        
        try:
            Factura.objects.get(consecutivo = consecutivo)
            mensaje = "El consecutivo es invalido, ya que ha sido usado anteriormente" 
            messages.error(request,mensaje)
            
            facturas = Factura.objects.all()
            cantidad_facturas = len(facturas)
            
            if cantidad_facturas != 0:
                ultima_factura = facturas[cantidad_facturas-1]
                consecutivo_ultima = ultima_factura.consecutivo
                consecutivo_ultima = int(consecutivo_ultima) + 1
                consecutivo = str(consecutivo_ultima)
            else:
                consecutivo = "1"
            
            usuario = request.user
            carrito = Carrito.objects.get(encargado=usuario)
            
            try:
                id_cliente = carrito.cliente
                cliente = Cliente.objects.get(nit=id_cliente)
                id_contacto = carrito.contacto
                contacto = Contacto.objects.get(id=id_contacto)
                
            except:
                clientes = Cliente.objects.all()
                pag = Paginate(request, clientes, 10)
                
                cxt = {
                    'posts': pag['queryset'],
                    'totPost': clientes,
                    'paginator': pag
                }
                
                messages.add_message(request, messages.ERROR, "No tiene seleccionado un Cliente, agregue uno a facturacion")
        
                
                return render_to_response('listar_clientes.html',cxt,
                    	context_instance=RequestContext(request))
            
            presentaciones = carrito.presentaciones
            
            subtotal = 0
            
            for presentacion in presentaciones.all():
                subtotal = subtotal + presentacion.precio
            
            iva = (subtotal*19)/100    
            total = subtotal + iva
        
            
            return render_to_response('generar_factura.html',{'consecutivo': consecutivo, 'carrito':carrito, 'contacto':contacto, 'cliente':cliente, 'subtotal':subtotal, 
            'iva':iva, 'total':total, 'tipo':'factura'},
            	context_instance=RequestContext(request))
        
        except:
            
            print " Consecutivo valido"
            
        #Se valida si existen las unidades en Stock
        for x in range(0, len(cantidad)):
            
            presentacion = Presentacion.objects.get(id = str(presentacion_id[x]))
            
            if presentacion.unidades_en_stock < int(cantidad[x]):
                
                mensaje = "No hay en Stock la cantidad de " + str(presentacion.producto.marca) + " " + str(presentacion.producto.referencia) + " requerida" + " en presentacion de " + str(presentacion.cantidad) + " " +str(presentacion.tipo_cantidad)
                messages.error(request,mensaje)
                 
                presentaciones = Presentacion.objects.filter(producto = presentacion.producto)
                
            	return render_to_response('generar_factura_validacion.html',{'presentaciones':presentaciones},
            			context_instance=RequestContext(request))


        factura = Factura(consecutivo = consecutivo, validez_oferta = validez_oferta, tiempo_entrega = tiempo_entrega, condicion_pago=condicion_pago, contacto = contacto.nombre, cliente = cliente, encargado = (request.user.first_name + request.user.last_name), subtotal = subtotal, iva = iva, 
        total = total_input)
        
        factura.save()
        

        for x in range (0, len(cantidad)):
            
            presentacion = Presentacion.objects.get(id=presentacion_id[x])
            cantidad_presentacion = cantidad[x]
            
            #Se elimina lo que se pidio en la factura del invetario
            presentacion.unidades_en_stock = presentacion.unidades_en_stock - int(cantidad_presentacion)
            presentacion.save()
            
            #Los demas datos para crear la presentacion declarada
            precio_unidad_presentacion = precio_unidad[x]
            precio_unidad_total = int(cantidad_presentacion) * int(precio_unidad_presentacion)
            
            presentacion_declarada = PresentacionDeclarada(presentacion = presentacion, cantidad = cantidad_presentacion, 
            precio_unidad = precio_unidad_presentacion, precio_total = precio_unidad_total)
            
            presentacion_declarada.save()

            factura.presentaciones.add(presentacion_declarada)
            
        factura.save()
        
        guardar_datos_demanda(factura.fecha.day, factura.fecha.month, factura.fecha.year, presentacion_id, cantidad)
        
        return redirect("facturacion:generarFactura_pdf", id_factura=factura.consecutivo)
        
class verFactura(TemplateView):
    
    def get(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
        
        id_factura = kwargs['id_factura']
        factura = Factura.objects.get(consecutivo=id_factura)
        
    	return render_to_response('visualizar_factura.html',{"factura":factura,},context_instance=RequestContext(request))
    			
    			


        
class editarFactura(TemplateView):
    
    def get(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
        
        id_factura = kwargs['id_factura']
        factura = Factura.objects.get(consecutivo=id_factura)
        
        
        cliente = factura.cliente
        id_contacto = factura.contacto
        contacto = Contacto.objects.get(nombre=id_contacto)
        
        presentaciones = factura.presentaciones
        
        subtotal = factura.subtotal
        iva = factura.iva   
        total = factura.total
        
        
        consecutivo = ""
        
    	return render_to_response('editar_factura.html',{'consecutivo': factura.consecutivo, 'factura' : factura, 'contacto':contacto, 'cliente':cliente, 'subtotal':subtotal, 
    	    'iva':iva, 'total':total},
    			context_instance=RequestContext(request))
    			

    def post(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			

        
        id_factura = kwargs['id_factura']
        factura = Factura.objects.get(consecutivo=id_factura)
        
        cliente_id = request.POST['cliente_id']
        total_input = request.POST['total-input']
        iva = request.POST['iva']
        contacto_id = request.POST['contacto_id']
        subtotal = request.POST['sub']
        validez_oferta = request.POST['validez_oferta']
        condicion_pago = request.POST['condicion_pago']
        tiempo_entrega = request.POST['tiempo_entrega']
        consecutivo = request.POST['consecutivo']

        
        #Traen los datos de la tabla 2
        cantidad = request.POST.getlist('cantidad')
        precio_unidad = request.POST.getlist('precio_unidad')
        presentacion_id = request.POST.getlist('presentacion_id')
        
        #Se crea el objeto Facturacion deseado
        contacto = Contacto.objects.get(id=contacto_id)
        cliente = Cliente.objects.get(nit = cliente_id)
        
        
        factura.validez_oferta = validez_oferta
        factura.tiempo_entrega = tiempo_entrega
        factura.condicion_pago = condicion_pago
        factura.contacto = contacto.nombre
        factura.cliente = cliente
        factura.encargado = (request.user.first_name + request.user.last_name)
        factura.iva = iva
        factura.subtotal = subtotal
        factura.total = total_input
        
        

        

        presentaciones_declaradas = factura.presentaciones.all()

        
        factura.presentaciones.clear()
        
        for x in range (0, len(cantidad)):
           
            presentacion = Presentacion.objects.get(id=presentacion_id[x])
            cantidad_presentacion = cantidad[x]
            precio_unidad_presentacion = precio_unidad[x]
            precio_unidad_total = int(cantidad_presentacion) * int(precio_unidad_presentacion)
            
            presentacion_declarada = presentaciones_declaradas[x]
            
            presentacion_declarada.presentacion = presentacion
            presentacion_declarada.cantidad = cantidad_presentacion
            presentacion_declarada.precio_unidad = precio_unidad_presentacion
            presentacion_declarada.precio_total = precio_unidad_total
            
            presentacion_declarada.save()
            
            factura.presentaciones.add(presentacion_declarada)
            
        factura.save()
        
        return redirect("facturacion:generarFactura_pdf", id_factura=factura.consecutivo)

class eliminar_factura(TemplateView):
    
	def post(self,request,*args,**kwargs):
		mensaje = ""
		
		if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
		if "codigoContacto" in request.POST:
			try:
			    id_producto = request.POST['codigoContacto']
			    Factura.objects.filter(consecutivo=id_producto).delete()
			    mensaje = {'status':'True'}		
			except:
				mensaje = {'status':'False'}
			response = simplejson.dumps(mensaje)
			return HttpResponse(response ,content_type='application/json')
        
class generarFacturadeCotizacion(TemplateView):
    
    def get(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
        
        
        facturas = Factura.objects.all()
        cantidad_facturas = len(facturas)
        ultima_factura = facturas[cantidad_facturas-1]
        consecutivo_ultima = ultima_factura.consecutivo
        consecutivo_ultima = int(consecutivo_ultima) + 1
        consecutivo = str(consecutivo_ultima)
        
        id_cotizacion = kwargs['id_cotizacion']
        cotizacion = Cotizacion.objects.get(id=id_cotizacion)
        
        usuario = request.user
        
        cliente = cotizacion.cliente
        id_contacto = cotizacion.contacto
        contacto = Contacto.objects.get(nombre=id_contacto)
        
        presentaciones = cotizacion.presentaciones
        
        subtotal = 0
        
        subtotal = cotizacion.subtotal
        iva = cotizacion.iva  
        total = cotizacion.total
        
        
    	return render_to_response('generar_factura_cotizacion.html',{'consecutivo': consecutivo,  'contacto':contacto, 'cliente':cliente, 'subtotal':subtotal, 
    	    'iva':iva, 'total':total, 'cotizacion' : cotizacion},
    			context_instance=RequestContext(request))
    			
    			
    def post(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
        cliente_id = request.POST['cliente_id']
        total_input = request.POST['total-input']
        iva = request.POST['iva']
        contacto_id = request.POST['contacto_id']
        subtotal = request.POST['sub']
        validez_oferta = request.POST['validez_oferta']
        condicion_pago = request.POST['condicion_pago']
        tiempo_entrega = request.POST['tiempo_entrega']
        consecutivo = request.POST['consecutivo']

        
        #Traen los datos de la tabla 2
        cantidad = request.POST.getlist('cantidad')
        precio_unidad = request.POST.getlist('precio_unidad')
        presentacion_id = request.POST.getlist('presentacion_id')
        
        #Se crea el objeto Facturacion deseado
        contacto = Contacto.objects.get(id=contacto_id)
        cliente = Cliente.objects.get(nit = cliente_id)
        
        try:
            
            Factura.objects.get(consecutivo = consecutivo)
            mensaje = "El consecutivo es invalido, ya que ha sido usado anteriormente" 
            messages.error(request,mensaje)
            
            facturas = Factura.objects.all()
            cantidad_facturas = len(facturas)
            ultima_factura = facturas[cantidad_facturas-1]
            consecutivo_ultima = ultima_factura.consecutivo
            consecutivo_ultima = int(consecutivo_ultima) + 1
            consecutivo = str(consecutivo_ultima)
            
            id_cotizacion = kwargs['id_cotizacion']
            cotizacion = Cotizacion.objects.get(id=id_cotizacion)
            
            usuario = request.user
            
            cliente = cotizacion.cliente
            id_contacto = cotizacion.contacto
            contacto = Contacto.objects.get(nombre=id_contacto)
            
            presentaciones = cotizacion.presentaciones
            
            subtotal = 0
            
            subtotal = cotizacion.subtotal
            iva = cotizacion.iva  
            total = cotizacion.total
            
            
            return render_to_response('generar_factura_cotizacion.html',{'consecutivo': consecutivo,  'contacto':contacto, 'cliente':cliente, 'subtotal':subtotal, 
                'iva':iva, 'total':total, 'cotizacion' : cotizacion},
            		context_instance=RequestContext(request))
            
            presentaciones = carrito.presentaciones
            
            subtotal = 0
            
            for presentacion in presentaciones.all():
                subtotal = subtotal + presentacion.precio
            
            iva = (subtotal*19)/100    
            total = subtotal + iva
        
            
            return render_to_response('generar_factura.html',{'consecutivo': consecutivo, 'carrito':carrito, 'contacto':contacto, 'cliente':cliente, 'subtotal':subtotal, 
            'iva':iva, 'total':total, 'tipo':'factura'},
            	context_instance=RequestContext(request))
        
        except:
            
            print " Consecutivo valido"
        
        factura = Factura(consecutivo = consecutivo, validez_oferta = validez_oferta, tiempo_entrega = tiempo_entrega, condicion_pago=condicion_pago, contacto = contacto.nombre, cliente = cliente, encargado = (request.user.first_name + request.user.last_name), subtotal = subtotal, iva = iva, 
        total = total_input)
        
        factura.save()
        

        

        for x in range (0, len(cantidad)):
            
            presentacion = Presentacion.objects.get(id=presentacion_id[x])
            cantidad_presentacion = cantidad[x]
            precio_unidad_presentacion = precio_unidad[x]
            precio_unidad_total = int(cantidad_presentacion) * int(precio_unidad_presentacion)
            
            presentacion_declarada = PresentacionDeclarada(presentacion = presentacion, cantidad = cantidad_presentacion, 
            precio_unidad = precio_unidad_presentacion, precio_total = precio_unidad_total)
            
            presentacion_declarada.save()
            

            factura.presentaciones.add(presentacion_declarada)
            
        factura.save()
        
        guardar_datos_demanda(factura.fecha.day, factura.fecha.month, factura.fecha.year, presentacion_id, cantidad)
        
        return redirect("facturacion:generarFactura_pdf", id_factura=factura.consecutivo)

class generarRemision(TemplateView):
    
    def get(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
        
        usuario = request.user
        carrito = Carrito.objects.get(encargado=usuario)
        
        try:
            id_cliente = carrito.cliente
            cliente = Cliente.objects.get(nit=id_cliente)
            id_contacto = carrito.contacto
            contacto = Contacto.objects.get(id=id_contacto)
            
        except:
            clientes = Cliente.objects.all()
            pag = Paginate(request, clientes, 10)
            
            cxt = {
                'posts': pag['queryset'],
                'totPost': clientes,
                'paginator': pag
            }
            
            messages.add_message(request, messages.ERROR, "No tiene seleccionado un Cliente, agregue uno a facturacion")
    
            
            return render_to_response('listar_clientes.html',cxt,
                	context_instance=RequestContext(request))
        
        presentaciones = carrito.presentaciones
        
        subtotal = 0
        
        for presentacion in presentaciones.all():
            subtotal = subtotal + presentacion.precio
        
        iva = (subtotal*19)/100    
        total = subtotal + iva
        
        
        consecutivo = ""
    	return render_to_response('generar_remision.html',{'carrito':carrito, 'contacto':contacto, 'cliente':cliente, 'subtotal':subtotal, 
    	    'iva':iva, 'total':total, 'tipo':'remision'},
    			context_instance=RequestContext(request))
    			

    def post(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
 
        
        cliente_id = request.POST['cliente_id']
        total_input = request.POST['total-input']
        iva = request.POST['iva']
        contacto_id = request.POST['contacto_id']
        subtotal = request.POST['sub']
        validez_oferta = request.POST['validez_oferta']
        condicion_pago = request.POST['condicion_pago']
        tiempo_entrega = request.POST['tiempo_entrega']

        
        #Traen los datos de la tabla 2
        cantidad = request.POST.getlist('cantidad')
        precio_unidad = request.POST.getlist('precio_unidad')
        presentacion_id = request.POST.getlist('presentacion_id')
        
        #Se crea el objeto Facturacion deseado
        contacto = Contacto.objects.get(id=contacto_id)
        cliente = Cliente.objects.get(nit = cliente_id)
        
        
        remision = Remision(validez_oferta = validez_oferta, tiempo_entrega = tiempo_entrega, condicion_pago=condicion_pago, contacto = contacto.nombre, cliente = cliente, encargado = (request.user.first_name + request.user.last_name), subtotal = subtotal, iva = iva, 
        total = total_input)
        
        remision.save()
        

        for x in range (0, len(cantidad)):
            
            presentacion = Presentacion.objects.get(id=presentacion_id[x])
            cantidad_presentacion = cantidad[x]
            precio_unidad_presentacion = precio_unidad[x]
            precio_unidad_total = int(cantidad_presentacion) * int(precio_unidad_presentacion)
            
            presentacion_declarada = PresentacionDeclarada(presentacion = presentacion, cantidad = cantidad_presentacion, 
            precio_unidad = precio_unidad_presentacion, precio_total = precio_unidad_total)
            
            presentacion_declarada.save()
            

            remision.presentaciones.add(presentacion_declarada)
            
        remision.save()
        
        return redirect("facturacion:generarRemision_pdf", id_remision=remision.id)
        	
class eliminarPresentacionCarrito(TemplateView):
    def post(self,request,*args,**kwargs):
		mensaje = ""

		if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
		if "codigoContacto" in request.POST:
			try:
			    usuario = request.user
			    carrito = Carrito.objects.get(encargado=usuario)
			    id_presentacion = request.POST['codigoContacto']
			    
			    presentacion = Presentacion.objects.get(id=id_presentacion)
			    carrito.presentaciones.remove(presentacion)
			    
			    mensaje = {'status':'True','row':id_presentacion}			
			except:
				mensaje = {'status':'False'}
			response = simplejson.dumps(mensaje)
			
			return HttpResponse(response ,content_type='application/json')
	
@csrf_exempt			
def validar_consecutivo(request):
    
	if not request.user.is_authenticated() or not request.user.is_active:
		return HttpResponseRedirect(reverse("usuario:error_403"))
		
	if "consecutivo" in request.POST:
	    
		try:
		    
		    consecutivo = request.POST['consecutivo']
		    
		    factura = Factura.objects.get(consecutivo = consecutivo)
		    
		    mensaje = {'status':'False'}		
		    
		except:
		    
			mensaje = {'status':'True'}
			
		response = simplejson.dumps(mensaje)
		print mensaje
		return HttpResponse(response ,content_type='application/json')

#Documentos Comerciales
        
class listarFacturacion(TemplateView):
    
    def get(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
        
        id_cliente = kwargs['id_cliente']
        cliente = Cliente.objects.get(nit = id_cliente)
        cotizaciones = Cotizacion.objects.filter(cliente = cliente).order_by('-fecha')
        pag = Paginate(request, cotizaciones, 10)
        
        contexto = {
            'cotizaciones': pag['queryset'],
            'paginator': pag,
            'cliente' : cliente
        }
        

    	return render_to_response('listar_cotizaciones.html', contexto,
    			context_instance=RequestContext(request))

    def post(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
            
        id_cliente = kwargs['id_cliente']
        cliente = Cliente.objects.get(nit = id_cliente)
        tipo_documento = request.POST['tipo_documento']
        
        
        if tipo_documento == 'Cotizaciones':
            return HttpResponseRedirect(reverse('facturacion:listar_cotizaciones', args=[id_cliente]))
        			
        elif tipo_documento == 'Facturas':
            return HttpResponseRedirect(reverse('facturacion:listar_facturas', args=[id_cliente]))
            
        else:
            return HttpResponseRedirect(reverse('facturacion:listar_remisiones', args=[id_cliente]))
 
def listar_facturas(request, id_cliente):
    
    if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
        
    cliente = Cliente.objects.get(nit = id_cliente)
    facturas = Factura.objects.filter(cliente = cliente).order_by('-fecha')
    pag = Paginate(request, facturas, 10)
    
    contexto = {
        'facturas': pag['queryset'],
        'paginator': pag,
        'cliente' : cliente
    }
    
    return render_to_response('listar_facturas.html', contexto,
			context_instance=RequestContext(request))
			
def listar_cotizaciones(request, id_cliente):
    
    if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
        
    cliente = Cliente.objects.get(nit = id_cliente)
    cotizaciones = Cotizacion.objects.filter(cliente = cliente).order_by('-fecha')
    pag = Paginate(request, cotizaciones, 10)
    
    contexto = {
        'cotizaciones': pag['queryset'],
        'paginator': pag,
        'cliente' : cliente
    }
    
    return render_to_response('listar_cotizaciones.html', contexto,
			context_instance=RequestContext(request))

def listar_remisiones(request, id_cliente):
    
    if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
        
    cliente = Cliente.objects.get(nit = id_cliente)
    remisiones = Remision.objects.filter(cliente = cliente).order_by('-fecha')
    pag = Paginate(request, remisiones, 10)
    
    contexto = {
        'remisiones': pag['queryset'],
        'paginator': pag,
        'cliente' : cliente
    }
    
    return render_to_response('listar_remisiones.html', contexto,
			context_instance=RequestContext(request))			
			
def limpiar_carrito(request, documento):
    
    if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
    usuario = request.user
    carrito = Carrito.objects.get(encargado = usuario)
    presentaciones = carrito.presentaciones.all()
    
    for presentacion in presentaciones:
        carrito.presentaciones.remove(presentacion)
    
    if documento == "cotizacion":
        return HttpResponseRedirect(reverse("facturacion:generar_cotizacion"))
    elif documento == "factura":
        return HttpResponseRedirect(reverse("facturacion:generar_factura"))
    elif documento == "remision":
        return HttpResponseRedirect(reverse("facturacion:generar_remision"))
    elif documento == "aplicacion":
        return HttpResponseRedirect(reverse("demanda:crear_aplicacion_futura"))
        
def Paginate(request, queryset, pages):
       
        # Retorna el objeto paginator para comenzar el trabajo
        result_list = Paginator(queryset, pages)
        
     
        try:
            # Tomamos el valor de parametro page, usando GET
            page = int(request.GET.get('page'))
           
        except:
            page = 1
     
        # Si es menor o igual a 0 igualo en 1
        if page <= 0:
            page = 1
     
        # Si viene un parametro que es mayor a la cantidad
        # de paginas le igualo el parametro con las cant de paginas
        if(page > result_list.num_pages):
            page = result_list.num_pages
     
        # Verificamos si esta dentro del rango
        if (result_list.num_pages >= page):
            
            pagina = result_list.page(page)
        
            context = {
                'queryset': pagina.object_list,
                'page': page,
                'pages': result_list.num_pages,
                'has_next': pagina.has_next(),
                'has_prev': pagina.has_previous(),
                'next_page': page+1,
                'prev_page': page-1,
                'firstPage': 1,
            }
     
        return context	    				

#Generacion de PDF    
class generarCotizacionPDF(View):

    def cabecera(self, pdf, cotizacion):
        
        archivo_imagen = settings.MEDIA_ROOT+'/logo.png'
        pdf.drawImage(archivo_imagen, 40, 740, 140, 100,preserveAspectRatio=True)
        
        
        pdf.setFont("Helvetica-Bold", 17)
        pdf.drawString(250, 740, u"Cotizacion")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(198, 720, u"Soluciones Tecnicas Aplicadas S.A.S")
        
        #Datos cliente
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 670, u"Santiago de Cali, " + str(cotizacion.fecha.date()))
        
        pdf.setFont("Helvetica", 10)
        pdf.drawString(350, 630, u"Cotizacion No. " + str(cotizacion.id))
        
        #1
        pdf.drawString(60, 630, u"Cliente:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(130, 630, u"" + cotizacion.cliente.sigla)
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 620, u"Ciudad:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(130, 620, u"" + cotizacion.cliente.ciudad)
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 610, u"Nit:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(130, 610, u"" + str(cotizacion.cliente.nit))
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 600, u"Contacto:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(130, 600, u"" + cotizacion.contacto)
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 590, u"Telefono:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(130, 590, u"" + str(cotizacion.cliente.telefono))
        
        
        
    
        
    def tablaProductos(self,pdf,y, presentaciones, subtotal, iva, total):
        
        encabezados = ('Cantidad', 'Referencia', 'Presentacion', 'Valor Unitario', 'Valor Total')
        
        detalles = [(presentacion.cantidad, (presentacion.presentacion.producto.marca + " " +presentacion.presentacion.producto.referencia), 
        (str(presentacion.presentacion.numero_elementos) + " " + str(presentacion.presentacion.empaque) + " x " + str(presentacion.presentacion.cantidad) + str(presentacion.presentacion.tipo_cantidad)), 
        ("$ " + str(presentacion.precio_unidad)), ("$ " + str(presentacion.precio_unidad))) for presentacion in presentaciones.all()]
        
        
        cantidad_presentaciones = len(presentaciones.all())
        
        for x in range (0, (14 - cantidad_presentaciones)):
            espacio = ["","", "", "", "" ]
            detalles.append(espacio)
        
        espacio_final = ["","", "", "", "" ]
        subtotal = ["","", "", "Subtotal", "$ " + subtotal ]
        iva = ["","", "", "Iva 19%", "$ " + iva ]
        total = ["","", "", "Total", "$ " + total  ]
        
        detalles.append(espacio_final)
        detalles.append(subtotal)
        detalles.append(iva)
        detalles.append(total)
        
        detalle_orden = Table([encabezados] + detalles, colWidths=[2 * 4, 4 * 4, 4* 4, 3.5* 4])
        detalle_orden.setStyle(TableStyle(
        [
                
                ('ALIGN',(0,0),(3,0),'CENTER'),
                
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ]
        ))
        
        detalle_orden.wrapOn(pdf, 800, 600)
        detalle_orden.drawOn(pdf, 60,y)
        
    
    
    
    def footer(self, pdf, y, cotizacion, usuario):
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, y, u"Condicion de Pago:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(170, y, u"" + cotizacion.condicion_pago)
        #----
        pdf.setFont("Helvetica", 10)
        pdf.drawString(350, y, u"Nombre:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(400, y, u"" + "Andre Rivas")
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, y-10, u"Validez de Oferta:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(170, y-10, u"" + cotizacion.validez_oferta)
        #----
        pdf.setFont("Helvetica", 10)
        pdf.drawString(350, y-10, u"Cargo:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(400, y-10, u"Gerente")
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, y-20, u"Tiempo de Entrega:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(170, y-20, u"" + cotizacion.tiempo_entrega)
        #----
        pdf.setFont("Helvetica", 10)
        pdf.drawString(350, y-20, u"Celular:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(400, y-20, u"3135923343")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(350, y-30, u"Correo:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(400, y-30, u"" + "ventas@soltecaindustrial.co")
        
        
        archivo_imagen = settings.MEDIA_ROOT+'/lubriplate_logo.jpg'
        pdf.drawImage(archivo_imagen, 100, 10, 140, 100,preserveAspectRatio=True)
        
        archivo_imagen = settings.MEDIA_ROOT+'/omicron_logo.png'
        pdf.drawImage(archivo_imagen, 350, 10, 140, 100,preserveAspectRatio=True)
        
        
        

    def get(self, request, *args, **kwargs):
        
        id_cotizacion =  kwargs['id_cotizacion']
        cotizacion = Cotizacion.objects.get(id=id_cotizacion)
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        self.cabecera(pdf, cotizacion)
        y = 220
        self.tablaProductos(pdf, y, cotizacion.presentaciones, cotizacion.subtotal, cotizacion.iva, cotizacion.total)
        y = 170
        self.footer(pdf,y, cotizacion, request.user)
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

class generarFacturaPDF(View):

    def cabecera(self, pdf, cotizacion):
        
        archivo_imagen = settings.MEDIA_ROOT+'/logo.png'
        pdf.drawImage(archivo_imagen, 40, 740, 140, 100,preserveAspectRatio=True)
        
        
        pdf.setFont("Helvetica-Bold", 17)
        pdf.drawString(250, 740, u"Factura")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(198, 720, u"Soluciones Tecnicas Aplicadas S.A.S")
        
        #Datos cliente
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 670, u"Santiago de Cali, " + str(cotizacion.fecha.date()))
        
        pdf.setFont("Helvetica", 10)
        pdf.drawString(350, 630, u"Factura No. " + str(cotizacion.consecutivo))
        
        #1
        pdf.drawString(60, 630, u"Cliente:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(130, 630, u"" + cotizacion.cliente.sigla)
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 620, u"Ciudad:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(130, 620, u"" + cotizacion.cliente.ciudad)
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 610, u"Nit:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(130, 610, u"" + str(cotizacion.cliente.nit))
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 600, u"Contacto:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(130, 600, u"" + cotizacion.contacto)
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 590, u"Telefono:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(130, 590, u"" + str(cotizacion.cliente.telefono))
        
        
        
    
        
    def tablaProductos(self,pdf,y, presentaciones, subtotal, iva, total):
        
        encabezados = ('Cantidad', 'Referencia', 'Presentacion', 'Valor Unitario', 'Valor Total')
        
        detalles = [(presentacion.cantidad, (presentacion.presentacion.producto.marca + " " +presentacion.presentacion.producto.referencia), 
        (str(presentacion.presentacion.numero_elementos) + " " + str(presentacion.presentacion.empaque) + " x " + str(presentacion.presentacion.cantidad) + str(presentacion.presentacion.tipo_cantidad)), 
        ("$ " + str(presentacion.precio_unidad)), ("$ " + str(presentacion.precio_unidad))) for presentacion in presentaciones.all()]
        
        
        cantidad_presentaciones = len(presentaciones.all())
        
        for x in range (0, (14 - cantidad_presentaciones)):
            espacio = ["","", "", "", "" ]
            detalles.append(espacio)
        
        espacio_final = ["","", "", "", "" ]
        subtotal = ["","", "", "Subtotal", "$ " + subtotal ]
        iva = ["","", "", "Iva 19%", "$ " + iva ]
        total = ["","", "", "Total", "$ " + total  ]
        
        detalles.append(espacio_final)
        detalles.append(subtotal)
        detalles.append(iva)
        detalles.append(total)
        
        detalle_orden = Table([encabezados] + detalles, colWidths=[2 * 4, 4 * 4, 4* 4, 3.5* 4])
        detalle_orden.setStyle(TableStyle(
        [
                
                ('ALIGN',(0,0),(3,0),'CENTER'),
                
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ]
        ))
        
        detalle_orden.wrapOn(pdf, 800, 600)
        detalle_orden.drawOn(pdf, 60,y)
        
    
    
    
    def footer(self, pdf, y, cotizacion, usuario):
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, y, u"Condicion de Pago:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(170, y, u"" + cotizacion.condicion_pago)
        #----
        pdf.setFont("Helvetica", 10)
        pdf.drawString(350, y, u"Nombre:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(400, y, u"" + "Andres Rivas")
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, y-10, u"Validez de Oferta:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(170, y-10, u"" + cotizacion.validez_oferta)
        #----
        pdf.setFont("Helvetica", 10)
        pdf.drawString(350, y-10, u"Cargo:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(400, y-10, u"Gerente")
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, y-20, u"Tiempo de Entrega:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(170, y-20, u"" + cotizacion.tiempo_entrega)
        #----
        pdf.setFont("Helvetica", 10)
        pdf.drawString(350, y-20, u"Celular:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(400, y-20, u"3135923343")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(350, y-30, u"Correo:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(400, y-30, u"" + "ventas@soltecaindustrial.co")
        
        
        archivo_imagen = settings.MEDIA_ROOT+'/lubriplate_logo.jpg'
        pdf.drawImage(archivo_imagen, 100, 10, 140, 100,preserveAspectRatio=True)
        
        archivo_imagen = settings.MEDIA_ROOT+'/omicron_logo.png'
        pdf.drawImage(archivo_imagen, 350, 10, 140, 100,preserveAspectRatio=True)
        
        
        

    def get(self, request, *args, **kwargs):
        
        id_factura =  kwargs['id_factura']
        cotizacion = Factura.objects.get(consecutivo=id_factura)
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        self.cabecera(pdf, cotizacion)
        y = 220
        self.tablaProductos(pdf, y, cotizacion.presentaciones, cotizacion.subtotal, cotizacion.iva, cotizacion.total)
        y = 170
        self.footer(pdf,y, cotizacion, request.user)
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
        
class generarRemisionPDF(View):

    def cabecera(self, pdf, cotizacion):
        
        archivo_imagen = settings.MEDIA_ROOT+'/logo.png'
        pdf.drawImage(archivo_imagen, 40, 740, 140, 100,preserveAspectRatio=True)
        
        
        pdf.setFont("Helvetica-Bold", 17)
        pdf.drawString(250, 740, u"Remision")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(198, 720, u"Soluciones Tecnicas Aplicadas S.A.S")
        
        #Datos cliente
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 670, u"Santiago de Cali, " + str(cotizacion.fecha.date()))
        
        pdf.setFont("Helvetica", 10)
        pdf.drawString(350, 630, u"Remision No. " + str(cotizacion.id))
        
        #1
        pdf.drawString(60, 630, u"Cliente:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(130, 630, u"" + cotizacion.cliente.sigla)
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 620, u"Ciudad:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(130, 620, u"" + cotizacion.cliente.ciudad)
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 610, u"Nit:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(130, 610, u"" + str(cotizacion.cliente.nit))
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 600, u"Contacto:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(130, 600, u"" + cotizacion.contacto)
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 590, u"Telefono:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(130, 590, u"" + str(cotizacion.cliente.telefono))
        
        
        
    
        
    def tablaProductos(self,pdf,y, presentaciones, subtotal, iva, total):
        
        encabezados = ('Cantidad', 'Referencia', 'Presentacion', 'Valor Unitario', 'Valor Total')
        
        detalles = [(presentacion.cantidad, (presentacion.presentacion.producto.marca + " " +presentacion.presentacion.producto.referencia), 
        (str(presentacion.presentacion.numero_elementos) + " " + str(presentacion.presentacion.empaque) + " x " + str(presentacion.presentacion.cantidad) + str(presentacion.presentacion.tipo_cantidad)), 
        ("$ " + str(presentacion.precio_unidad)), ("$ " + str(presentacion.precio_unidad))) for presentacion in presentaciones.all()]
        
        
        cantidad_presentaciones = len(presentaciones.all())
        
        for x in range (0, (14 - cantidad_presentaciones)):
            espacio = ["","", "", "", "" ]
            detalles.append(espacio)
        
        espacio_final = ["","", "", "", "" ]
        subtotal = ["","", "", "Subtotal", "$ " + subtotal ]
        iva = ["","", "", "Iva 19%", "$ " + iva ]
        total = ["","", "", "Total", "$ " + total  ]
        
        detalles.append(espacio_final)
        detalles.append(subtotal)
        detalles.append(iva)
        detalles.append(total)
        
        detalle_orden = Table([encabezados] + detalles, colWidths=[2 * 4, 4 * 4, 4* 4, 3.5* 4])
        detalle_orden.setStyle(TableStyle(
        [
                
                ('ALIGN',(0,0),(3,0),'CENTER'),
                
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ]
        ))
        
        detalle_orden.wrapOn(pdf, 800, 600)
        detalle_orden.drawOn(pdf, 60,y)
        
    
    
    
    def footer(self, pdf, y, cotizacion, usuario):
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, y, u"Condicion de Pago:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(170, y, u"" + cotizacion.condicion_pago)
        #----
        pdf.setFont("Helvetica", 10)
        pdf.drawString(350, y, u"Nombre:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(400, y, u"" + "Andres Rivas")
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, y-10, u"Validez de Oferta:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(170, y-10, u"" + cotizacion.validez_oferta)
        #----
        pdf.setFont("Helvetica", 10)
        pdf.drawString(350, y-10, u"Cargo:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(400, y-10, u"Gerente")
        
        #1
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, y-20, u"Tiempo de Entrega:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(170, y-20, u"" + cotizacion.tiempo_entrega)
        #----
        pdf.setFont("Helvetica", 10)
        pdf.drawString(350, y-20, u"Celular:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(400, y-20, u"3135923343")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(350, y-30, u"Correo:")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(400, y-30, u"" + "ventas@soltecaindustrial.co")
        
        
        archivo_imagen = settings.MEDIA_ROOT+'/lubriplate_logo.jpg'
        pdf.drawImage(archivo_imagen, 100, 10, 140, 100,preserveAspectRatio=True)
        
        archivo_imagen = settings.MEDIA_ROOT+'/omicron_logo.png'
        pdf.drawImage(archivo_imagen, 350, 10, 140, 100,preserveAspectRatio=True)
        
        
        

    def get(self, request, *args, **kwargs):
        
        id_remision =  kwargs['id_remision']
        cotizacion = Remision.objects.get(id=id_remision)
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        self.cabecera(pdf, cotizacion)
        y = 220
        self.tablaProductos(pdf, y, cotizacion.presentaciones, cotizacion.subtotal, cotizacion.iva, cotizacion.total)
        y = 170
        self.footer(pdf,y, cotizacion, request.user)
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response