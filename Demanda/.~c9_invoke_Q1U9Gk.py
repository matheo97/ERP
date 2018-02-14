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
from Producto.models import *
from Facturacion.models import *
import datetime
from django.shortcuts import redirect
from Demanda.models import *
from django.core.paginator import Paginator

#Demanda crear periodo inicial

def crear_periodo_inicial(request):
    if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
			
    
    # # Listado_Productos.objects.filter(referencia_periodo = "1-2016").delete()
    # Listado_Productos.objects.filter(referencia_periodo = "2-2017").delete()
    # Listado_Productos.objects.filter(referencia_periodo = "1-2017").delete()
    # listado_productos = Listado_Productos(referencia_periodo = "1-2017")
    # listado_productos.save()
    
    # productos = Producto.objects.all()
    
    # pronostico = 0
    
    # # Si se agrega un producto automaticamente se debe agregar aqui.
    for producto in productos:
        
        if producto.referencia == "86":
            producto.pronostico_inicial = "20"
        elif producto.referencia == "6030":
            producto.pronostico_inicial = "40"
        elif producto.referencia == "710":
            producto.pronostico_inicial = "35"
        elif producto.referencia == "730":
            producto.pronostico_inicial = "50"
        elif producto.referencia == "6120":
            producto.pronostico_inicial = "20"
        elif producto.referencia == "6130":
            producto.pronostico_inicial = "20"
            
        producto.save()
            
    #     producto_importado = Producto_Importacion(tipo_contenido = producto.tipo_contenido, pronostico = pronostico, cantidad = "0", producto = producto)
    #     producto_importado.save()
        
    #     listado_productos.productos.add(producto_importado)
    
    return HttpResponse("Primer periodo creado con exito :)")
    
class mostrarPrediccion(TemplateView):

    
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
            
        hoy = datetime.datetime.today()
            
        dia = hoy.day
        mes = hoy.month
        ano = hoy.year
        
        periodo = 0

        if int(mes) >= 1 and int(mes) <= 4:
            periodo = 1
        elif int(mes) > 4 and int(mes) <= 8:
            periodo = 2
        else:
            periodo = 3
            
        referencia_actual = str(periodo) + "-" + str(ano)
        
        #Cambiar a la referencia actual cuando se este en pruebas con el ultimo periodo de referencia
        listado_productos = Listado_Productos.objects.all()[0]
        listado_productos_aplicacion_futura = Producto_Aplicacion_Futura.objects.filter(referencia_periodo = listado_productos.referencia_periodo)
        listados_productos = Listado_Productos.objects.all()
        
        
        #Ultima tab
        pronostico_final = []
        
        
        for producto_cn in listado_productos.productos.all():
            
            entro = False
            
            for producto_cl in listado_productos_aplicacion_futura:
                
                if(producto_cn.producto == producto_cl.producto):
                    
                    prediccion_final = str(float(producto_cl.pronostico_total) + float(producto_cn.pronostico))
                    
                    
                    
                    dicc = {'producto_base' : producto_cl.producto.marca + producto_cl.producto.referencia, 
                            'pronostico_cuantitativo': producto_cn.pronostico,
                            'pronostico_cualitativo': producto_cl.pronostico_total,
                            'prediccion_final': prediccion_final,
                            'tipo': producto_cn.producto.tipo_contenido
                        
                    }
                    
                    
                    entro = True
                    pronostico_final.append(dicc)
                    break
            
            if(not entro):
                prediccion_final = float(producto_cn.pronostico)
                dicc = {'producto_base' : producto_cn.producto.marca + producto_cn.producto.referencia, 
                        'pronostico_cuantitativo': producto_cn.pronostico,
                        'pronostico_cualitativo': '0',
                        'prediccion_final': prediccion_final,
                        'tipo': producto_cn.producto.tipo_contenido
                }
                
                pronostico_final.append(dicc)
        
       
        for producto_cl in listado_productos_aplicacion_futura:
        
            producto = listado_productos.productos.all()
            producto = producto.filter(producto = producto_cl.producto)
            
            if(len(producto) == 0):
                
                prediccion_final = float(producto_cl.pronostico_total)
                
                dicc = {'producto_base' : producto_cl.producto.marca + producto_cl.producto.referencia, 
                        'pronostico_cuantitativo': '0',
                        'pronostico_cualitativo': producto_cl.pronostico_total,
                        'prediccion_final': prediccion_final,
                        'ti'
                }
                
                pronostico_final.append(dicc)
                    
            
    	return render_to_response('mostrar_prediccion.html',{'listado_productos' : listado_productos, 'listados_productos' : listados_productos, 'listado_futuro': listado_productos_aplicacion_futura, 'pronostico_final':pronostico_final},
    			context_instance=RequestContext(request))
    			
    			

    def post(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
        periodo = request.POST['periodo']
        
        
    	listado_productos = Listado_Productos.objects.get(referencia_periodo = periodo)
        listado_productos_aplicacion_futura = Producto_Aplicacion_Futura.objects.filter(referencia_periodo = periodo)
        listados_productos = Listado_Productos.objects.all()
        
        
        #Ultima tab
        pronostico_final = []
        
        
        for producto_cn in listado_productos.productos.all():
            
            entro = False
            
            for producto_cl in listado_productos_aplicacion_futura:
                
                if(producto_cn.producto == producto_cl.producto):
                    
                    prediccion_final = str(float(producto_cl.pronostico_total) + float(producto_cn.pronostico))
                    
                    dicc = {'producto_base' : producto_cl.producto.marca + producto_cl.producto.referencia, 
                            'pronostico_cuantitativo': producto_cn.pronostico,
                            'pronostico_cualitativo': producto_cl.pronostico_total,
                            'prediccion_final': prediccion_final
                    }
                    
                    
                    entro = True
                    pronostico_final.append(dicc)
                    break
            
            if(not entro):
                prediccion_final = float(producto_cn.pronostico)
                dicc = {'producto_base' : producto_cn.producto.marca + producto_cn.producto.referencia, 
                        'pronostico_cuantitativo': producto_cn.pronostico,
                        'pronostico_cualitativo': '0',
                        'prediccion_final': prediccion_final
                }
                
                pronostico_final.append(dicc)
        
       
        for producto_cl in listado_productos_aplicacion_futura:
        
            producto = listado_productos.productos.all()
            producto = producto.filter(producto = producto_cl.producto)
            
            if(len(producto) == 0):
                
                prediccion_final = float(producto_cl.pronostico_total)
                
                dicc = {'producto_base' : producto_cl.producto.marca + producto_cl.producto.referencia, 
                        'pronostico_cuantitativo': '0',
                        'pronostico_cualitativo': producto_cl.pronostico_total,
                        'prediccion_final': prediccion_final
                }
                
                pronostico_final.append(dicc)
                    
            
    	return render_to_response('mostrar_prediccion.html',{'listado_productos' : listado_productos, 'listados_productos' : listados_productos, 'listado_futuro': listado_productos_aplicacion_futura, 'pronostico_final':pronostico_final},
    			context_instance=RequestContext(request))
    			
class generarAplicacionFutura(TemplateView):
    
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
        meses_aplicacion = meses_disponibles(self)
            
        
    	return render_to_response('crear_aplicacion_futura.html',{'carrito':carrito, 'contacto':contacto, 'cliente':cliente, 'meses_aplicacion':meses_aplicacion, 'tipo':'aplicacion'},
    			context_instance=RequestContext(request))

    def post(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
            return HttpResponseRedirect(reverse("usuario:error_403"))
            
        cliente_id = request.POST['cliente_id']
        contacto_id = request.POST['contacto_id']
        probabilidad = request.POST['probabilidad']
        mes_tentivo = request.POST['mes_tentivo']
        
        #Traen los datos de la tabla 2
        numero_elementos = request.POST.getlist('cantidad')
        presentacion_id = request.POST.getlist('presentacion_id')
        
        
        #Se crea el objeto Facturacion deseado
        contacto = Contacto.objects.get(id=contacto_id)
        cliente = Cliente.objects.get(nit = cliente_id)
        
        referencia_periodo = self.extraerPeriodo(mes_tentivo)
         
        #Ni idea porque toca poner este import aqui            
        from Demanda.models import Producto_Aplicacion_Futura
        
        listado_productos_aplicacion_futura = Producto_Aplicacion_Futura.objects.all()
        
        listado_periodo = listado_productos_aplicacion_futura.filter(referencia_periodo = referencia_periodo)
        
        
        
        for x in range (0, len(numero_elementos)):
            
            presentacion = Presentacion.objects.get(id = presentacion_id[x])
            
            #Pasar de mililitros a Litros
            tipo_cantidad = presentacion.tipo_cantidad
            
            
            if int(numero_elementos[x]) >= 1:
                
                if tipo_cantidad == 'mL':
                    cantidad = str(presentacion.numero_elementos * int(numero_elementos[x]) * int(presentacion.cantidad))
                    cantidad = str(float(cantidad)/1000)
                    
                else:
                    cantidad = str(presentacion.numero_elementos * int(numero_elementos[x]) * int(presentacion.cantidad))
                    
                    
            else:
                
                messages.add_message(request, messages.ERROR, "No se pueden agregar cantidades de productos negativas")

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
                meses_aplicacion = meses_disponibles(self)
                    
                
            	return render_to_response('crear_aplicacion_futura.html',{'carrito':carrito, 'contacto':contacto, 'cliente':cliente, 'meses_aplicacion':meses_aplicacion, 'tipo':'aplicacion'},
            			context_instance=RequestContext(request))
            			
            			
            if len(listado_periodo) == 0:
                from Demanda.models import Producto_Aplicacion_Futura
                #Si no existe ningun producto con este periodo se crea un producto y se agrega una prediccion con el periodo dado
                Producto_Aplicacion_Futura = Producto_Aplicacion_Futura(referencia_periodo = referencia_periodo, producto = presentacion.producto, pronostico_total = '0')
                Producto_Aplicacion_Futura.save()
                from Demanda.models import Aplicacion_Futura
                Aplicacion_Futura = Aplicacion_Futura(probabilidad = probabilidad, pronostico_individual = cantidad, contacto = contacto.nombre, cliente = cliente.razon_social)
                Aplicacion_Futura.save()
                Producto_Aplicacion_Futura.pronostico_total = float(Producto_Aplicacion_Futura.pronostico_total) + float(cantidad)
                Producto_Aplicacion_Futura.predicciones.add(Aplicacion_Futura)
                Producto_Aplicacion_Futura.save()
                
                print "1"
                
            else:
                
                if len(listado_periodo.filter(producto = presentacion.producto)) == 0:
                    from Demanda.models import Producto_Aplicacion_Futura
                    #Si no existe ningun producto con este periodo se crea un producto y se agrega una prediccion con el periodo dado
                    Producto_Aplicacion_Futura = Producto_Aplicacion_Futura(referencia_periodo = referencia_periodo, producto = presentacion.producto, pronostico_total = '0')
                    Producto_Aplicacion_Futura.save()
                    from Demanda.models import Aplicacion_Futura
                    Aplicacion_Futura = Aplicacion_Futura(probabilidad = probabilidad, pronostico_individual = cantidad, contacto = contacto.nombre, cliente = cliente.razon_social)
                    Aplicacion_Futura.save()
                    Producto_Aplicacion_Futura.pronostico_total = float(Producto_Aplicacion_Futura.pronostico_total) + float(cantidad)
                    Producto_Aplicacion_Futura.predicciones.add(Aplicacion_Futura)
                    Producto_Aplicacion_Futura.save()
                    
                    print "2"
                    
                else:
                    from Demanda.models import Producto_Aplicacion_Futura
                    #Si existe el producto en el periodo especificado, se extrae este y se le agrega una prediccion
                    producto_aplicacion_futura = listado_periodo.filter(producto = presentacion.producto)[0]
                    from Demanda.models import Aplicacion_Futura
                    Aplicacion_Futura = Aplicacion_Futura(probabilidad = probabilidad, pronostico_individual = cantidad, contacto = contacto.nombre, cliente = cliente.razon_social)
                    Aplicacion_Futura.save()
                    producto_aplicacion_futura.pronostico_total = float(producto_aplicacion_futura.pronostico_total) + float(cantidad)
                    producto_aplicacion_futura.predicciones.add(Aplicacion_Futura)
                    producto_aplicacion_futura.save()
                    
                    print "3"
            
            
        return redirect("demanda:mostrar_prediccion")
        
    def extraerPeriodo(self, mes):
        
        mes = mes.split("-")
        mes1 = mes[0]
        periodo = mes[1]
        mes = int(mes1)
        
        if mes >= 1 and mes <= 4:
            referencia_periodo = "1-" + str(periodo)
            
        elif mes >= 5 and mes <= 8:
            referencia_periodo = "2-" + str(periodo)
        else:
            referencia_periodo = "3-" + str(periodo)
            
        return referencia_periodo
             
def meses_disponibles(self):
        
        meses_aplicacion = []
        
        hoy = datetime.datetime.today()
            
        mes = hoy.month
        ano = hoy.year
        
        
        meses_aplicacion = []
        
        if int(mes) >= 1 and int(mes) <= 4:
            limite = 9
            for x in range (int(mes), limite):
                meses_aplicacion.append(str(x) + "-" + str(ano))
                
        elif int(mes) <= 5 and int(mes) <=8:
            limite = 13
            for x in range (int(mes), limite):
                meses_aplicacion.append(str(x) + "-" + str(ano))
        else:
            limite = 13
            
            for x in range (int(mes), limite):
                meses_aplicacion.append(str(x) + "-" + str(ano))
                
            limite_2 = 5
            ano_2 = int(ano) + 1
            
            for x in range (1, limite_2):
                meses_aplicacion.append(str(x) + "-" + str(ano_2))
                
        return meses_aplicacion    
        
class eliminar_pronostico_individual(TemplateView):
	def post(self,request,*args,**kwargs):
		mensaje = ""
		
		if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
		if "codigoContacto" in request.POST:
			try:
			    data = request.POST['codigoContacto']
			    data = data.split("-")
			    id_pronostico = data[0]
			    id_producto = data[1]
			    
			       
			    aplicacion = Aplicacion_Futura.objects.filter(id=id_pronostico)[0]
			    cantidad_restar = aplicacion.pronostico_individual
			    producto  = Producto_Aplicacion_Futura.objects.get(id = id_producto)
			    
			    
			    producto.pronostico_total = str(float(producto.pronostico_total) - float(cantidad_restar))
			    producto.save()
			    aplicacion.delete()
			    
			    mensaje = {'status':'True','codigoUsuario':id_pronostico}			
			except:
				mensaje = {'status':'False'}
				
			response = simplejson.dumps(mensaje)
			return HttpResponse(response ,content_type='application/json')
			
def Paginate(request, queryset, pages):
       
        # Retorna el objeto paginator para comenzar el trabajo
        result_list = Paginator(queryset, pages)
        print result_list.object_list
        print pages
     
        try:
            # Tomamos el valor de parametro page, usando GET
            page = int(request.GET.get('page'))
            print page
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
            # Obtengo el listado correspondiente al page
            print "page" + str(page)
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
        