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
from Facturacion.models import Carrito
from django.db.models import Q
import datetime
from Demanda.models import *
#Paginador
from django.core.paginator import Paginator


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
            # Obtengo el listado correspondiente al page
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
        
#CRUD CATEGORIA   	
class CrearCategoria(TemplateView):
    
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
    	return render_to_response('formulario_crear_categoria.html',{},
    			context_instance=RequestContext(request))

    def post(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
        tipo = request.POST['tipo']
        nombre = request.POST['nombre']
        
        try:
            imagen= request.FILES['imagen']
            
            mensaje = "El campo imagen debe tener un formato de imagen valido"
            messages.info(request,mensaje)
            
            ini, fin =  imagen.name.split(".")
            valid_extensions = ['jpg', 'png', 'jpge']
            if not fin in valid_extensions:
                return render_to_response('formulario_crear_categoria.html',{},
        			context_instance=RequestContext(request))
        			
        except:
            mensaje = "El campo imagen No puede ser vacio"
            messages.info(request,mensaje)
            
            return render_to_response('formulario_crear_categoria.html',{},
    			context_instance=RequestContext(request))
    			
        try:
            categoria = Categoria.objects.get(nombre=nombre)
            mensaje = "Ya existe una Categoria con este Nombre"
            messages.error(request,mensaje)
            
            return render_to_response('formulario_crear_categoria.html',{},
            context_instance=RequestContext(request))
            
        except:
        	categoria = Categoria(tipo = tipo, nombre = nombre, imagen = imagen)
        	categoria.save()
        	
        	return HttpResponseRedirect(reverse("producto:listar_categorias"))
        	
class ModificarCategoria(TemplateView):
    
    def get(self,request,*args,**kwargs):
    	if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
    	print kwargs
    	id = kwargs['id_categoria']
    	categoria = Categoria.objects.get(id=id)
    	
        return render_to_response('formulario_modificar_categoria.html',{'categoria':categoria},
        	context_instance=RequestContext(request))
    
	
			
    def post(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
    	id = kwargs['id_categoria']
    	categoria = Categoria.objects.get(id=id)
    	print categoria.nombre
        tipo = request.POST['tipo']
        
        try:
            imagen= request.FILES['imagen']
            mensaje = "El campo imagen debe tener un formato de imagen valido"
            messages.info(request,mensaje)
            ini, fin =  imagen.name.split(".")
            valid_extensions = ['jpg', 'png']
            
            if not fin in valid_extensions:
                return render_to_response('formulario_modificar_categoria.html',{'categoria':categoria},
                context_instance=RequestContext(request))
            
            categoria.tipo = tipo
            categoria.imagen = imagen
            categoria.save()
            	
            return HttpResponseRedirect(reverse("producto:listar_categorias"))		
        			
			
        except:
    			
        	categoria.tipo = tipo
        	categoria.save()
        	
        	return HttpResponseRedirect(reverse("producto:listar_categorias"))

class ListarCategoria(TemplateView):
    
    def get(self,request,*args,**kwargs):
    	
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
        
        categorias = Categoria.objects.all()
        pag = Paginate(request, categorias, 6)
        
        contexto = {
            'categorias': pag['queryset'],
            'paginator': pag
        }
        
    	return render(request, 'listar_categorias.html', contexto)

def filtrar_categorias(request):
    
    if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
            
    try:
        buscar = request.GET['csrfmiddlewaretoken']
        tipo = request.GET.get('tipo')
    except:
        tipo = request.GET.get('tipo_re')        
    
    if tipo == 'Todos':
        return HttpResponseRedirect(reverse('producto:listar_categorias'))
    else:
        categorias = Categoria.objects.filter(tipo=tipo)
        pag = Paginate(request, categorias, 10)
        
        contexto = {
            'categorias': pag['queryset'],
            'paginator': pag,
            'tipo' : tipo
        }
        
        return render(request, 'listar_categorias.html', contexto)

class desactivar_categoria(TemplateView):
    
	def post(self,request,*args,**kwargs):
		mensaje = ""
		
		if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
		if "codigoContacto" in request.POST:
			try:
			    id_contacto = request.POST['codigoContacto']
			    categoria = Categoria.objects.get(id=id_contacto)
			    categoria.disponible = False
			    categoria.save()
			    
			    mensaje = {'status':'True','codigoUsuario':id_contacto}			
			except:
				mensaje = {'status':'False'}
			response = simplejson.dumps(mensaje)
			
			return HttpResponse(response ,content_type='application/json')

class activar_categoria(TemplateView):
    
	def post(self,request,*args,**kwargs):
		mensaje = ""
		
		if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
		if "codigoContacto" in request.POST:
			try:
			    
			    id_contacto = request.POST['codigoContacto']
			    print id_contacto
			    categoria = Categoria.objects.get(id=id_contacto)
			    
			    categoria.disponible = True
			    categoria.save()
			    
			    mensaje = {'status':'True','codigoUsuario':id_contacto}			
			except:
			    
			    mensaje = {'status':'False'}
			response = simplejson.dumps(mensaje)
			
			return HttpResponse(response ,content_type='application/json')
    
    
#CRUD PRODUCTO
class CrearProducto(TemplateView):
    
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
    	return render_to_response('formulario_crear_producto.html',{},
    			context_instance=RequestContext(request))


    def post(self,request,*args,**kwargs):
    	
    	if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
        referencia = request.POST['referencia']
        marca = request.POST['marca']
        descripcion = request.POST['descripcion']
        categoria = request.POST['categoria']
        tipo = request.POST['tipo']
        ficha_tecnica = ""
        ficha_seguridad = ""
        ficha_comercial_litografias = ""
        ficha_comercial_alimentaria = ""
        ficha_comercial_gruas = ""
        ficha_comercial_cementeras = ""
        
        if categoria == '':
            mensaje = "El campo Categoria no puede ser vacio!"
            messages.info(request,mensaje)
             
            return render_to_response('formulario_crear_producto.html',{},
    			context_instance=RequestContext(request))
    			
        if tipo == 'Tipo':
            mensaje = "El campo Tipo no puede ser vacio!"
            messages.info(request,mensaje)
             
            return render_to_response('formulario_crear_producto.html',{},
    			context_instance=RequestContext(request))
    			
        grado_alimenticio = request.POST['grado_alimenticio']
        
        #Validacion para la imagen
#         try:
#             imagen= request.FILES['imagen']
            
#             ini, fin =  imagen.name.split(".")
#             valid_extensions = ['jpg', 'png']
#             if not fin in valid_extensions:
#                 mensaje = "El campo imagen debe tener un formato de imagen valido"
#                 messages.info(request,mensaje)
                 
#                 return render_to_response('formulario_crear_producto.html',{},
#         			context_instance=RequestContext(request))
#         except:
#             mensaje = "El campo imagen No puede ser vacio"
#             messages.info(request,mensaje)
            
#             return render_to_response('formulario_crear_producto.html',{},
# 			context_instance=RequestContext(request))
        
        #Validacion para Ficha Comercial
        try:
            ficha_comercial = request.FILES['ficha_comercial']
            
            ini, fin =  ficha_comercial.name.split(".")
            valid_extensions = ['pdf']
            if not fin in valid_extensions:
                mensaje = "El campo Ficha Comercial debe ser en formato PDF"
                messages.info(request,mensaje)
            
                return render_to_response('formulario_crear_producto.html',{},
        			context_instance=RequestContext(request))
        			
        except:
            mensaje = "El campo Ficha Comercial no puede ser vacia"
            messages.info(request,mensaje)
            
            return render_to_response('formulario_crear_producto.html',{},
            context_instance=RequestContext(request))
            
        
            
            
        #Validacion Ficha Tecnica
        try:
            ficha_tecnica = request.FILES['ficha_tecnica']
            
            ini, fin =  ficha_comercial.name.split(".")
            valid_extensions = ['pdf']
            if not fin in valid_extensions:
                mensaje = "El campo Ficha Tecnica debe ser en formato PDF"
                messages.info(request,mensaje)
            
                return render_to_response('formulario_crear_producto.html',{},
        			context_instance=RequestContext(request))
        except:
            print "El campo ficha tecnica esta vacio"
        
        #Validacion Ficha de Seguridad
        try:
            ficha_seguridad = request.FILES['ficha_seguridad']
            
            ini, fin =  ficha_comercial.name.split(".")
            valid_extensions = ['pdf']
            if not fin in valid_extensions:
                mensaje = "El campo Ficha Seguridad debe ser en formato PDF"
                messages.info(request,mensaje)
            
                return render_to_response('formulario_crear_producto.html',{},
        			context_instance=RequestContext(request))
        except:
            print "Ficha de seguridad esta vacia"
			
			
		#Validacion para Ficha Comercial Litografias
        try:
            ficha_comercial_litografias = request.FILES['ficha_comercial_litografias']
            print "URL LITO"
            print ficha_comercial_litografias
            
            ini, fin =  ficha_comercial_litografias.name.split(".")
            valid_extensions = ['pdf']
            if not fin in valid_extensions:
                mensaje = "El campo Ficha Comercial Litografias debe ser en formato PDF"
                messages.info(request,mensaje)
            
                return render_to_response('formulario_crear_producto.html',{},
        			context_instance=RequestContext(request))

        except:
            print "es vacia la ficha comercial litografias"
            
            
        #Validacion para Ficha Comercial Gruas
        try:
            ficha_comercial_gruas = request.FILES['ficha_comercial_gruas']
            
            ini, fin =  ficha_comercial_gruas.name.split(".")
            valid_extensions = ['pdf']
            if not fin in valid_extensions:
                mensaje = "El campo Ficha Comercial Gruas debe ser en formato PDF"
                messages.info(request,mensaje)
            
                return render_to_response('formulario_crear_producto.html',{},
        			context_instance=RequestContext(request))
        	
        except:
            print "es vacia la ficha comercial gruas"
            
            
        #Validacion para Ficha Comercial Alimentarias
        try:
            ficha_comercial_alimentaria = request.FILES['ficha_comercial_alimentaria']
            
            ini, fin =  ficha_comercial_alimentaria.name.split(".")
            valid_extensions = ['pdf']
            if not fin in valid_extensions:
                mensaje = "El campo Ficha Comercial Alimentaria debe ser en formato PDF"
                messages.info(request,mensaje)
            
                return render_to_response('formulario_crear_producto.html',{},
        			context_instance=RequestContext(request))
        	
        	
        except:
            print "es vacia la ficha comercial alimentaria"
        
        
        #Validacion para Ficha Comercial Cementera
        try:
            ficha_comercial_cementeras = request.FILES['ficha_comercial_cementeras']
            
            ini, fin =  ficha_comercial_cementeras.name.split(".")
            valid_extensions = ['pdf']
            if not fin in valid_extensions:
                mensaje = "El campo Ficha Comercial Alimentaria debe ser en formato PDF"
                messages.info(request,mensaje)
            
                return render_to_response('formulario_crear_producto.html',{},
        			context_instance=RequestContext(request))
            
        except:
            print "es vacia la ficha comercial cementeras"
                
        # try:
            
        if tipo == "Lubricantes Industriales":
            tipo_contenido = "Litros"
        elif tipo == "Grasa":
            tipo_contenido = "Libras"
        elif tipo == "Aditivos":
            tipo_contenido = "Litros"
        elif tipo == "Soldadura para Antorcha":
            tipo_contenido = "Libras"
        elif tipo == "Soldadura para Arco":
            tipo_contenido = "Libras"
        else:
            tipo_contenido = "Litros"
        
        pronostico_inicial = request.POST['pronostico']
        
        categoria = Categoria.objects.get(nombre = categoria)
        producto = Producto(referencia=referencia,marca=marca,categoria=categoria,
                    ficha_comercial=ficha_comercial, ficha_tecnica=ficha_tecnica, ficha_seguridad=ficha_seguridad,
                    grado_alimenticio=grado_alimenticio, tipo = tipo, descripcion = descripcion, 
                    tipo_contenido = tipo_contenido, ficha_comercial_alimentaria = ficha_comercial_alimentaria, ficha_comercial_cementeras = ficha_comercial_cementeras, 
                    ficha_comercial_gruas = ficha_comercial_gruas, ficha_comercial_litografias = ficha_comercial_litografias, pronostico_inicial = pronostico_inicial)
                    
        producto.save()
        

        # try:
            
        #     pronostico_inicial = request.POST['pronostico']
            
        # except:
            
        #     pronostico_inicial = "30"
            
        # hoy = datetime.datetime.today()
        
        # dia = hoy.day
        # mes = hoy.month
        # ano = hoy.year
        
        # periodo = 0

        # if int(mes) >= 1 and int(mes) <= 4:
        #     periodo = 1
        # elif int(mes) > 4 and int(mes) <= 8:
        #     periodo = 2
        # else:
        #     periodo = 3
            
        # referencia_actual = str(periodo) + "-" + str(ano)
        
        # if periodo <= 2:
        #     periodo = periodo + 1
        
        # else:
        #     periodo = 1
        #     ano = int(ano) + 1
            
        # referencia_futura = str(periodo) + "-" + str(ano)
        
        
        # #Se agrega el producto al listado de productos demanda actual
        # listado_productos_actual = Listado_Productos.objects.get(referencia_periodo = referencia_actual)
        # producto_nuevo = Producto_Importacion(producto = producto, cantidad = "0", pronostico = pronostico_inicial)
        # producto_nuevo.save()
        # listado_productos_actual.productos.add(producto_nuevo)
        # listado_productos_actual.save()
        
        
        # try:
        #     #Si existe la futura, se agrega a ella, de lo contrario no.
        #     listado_productos_futuro = Listado_Productos.objects.get(referencia_periodo = referencia_futura)
        #     producto_nuevo = Producto_Importacion(producto = producto, cantidad = "0", pronostico = pronostico_inicial)
        #     producto_nuevo.save()
        #     listado_productos_futuro.productos.add(producto_nuevo)
        #     listado_productos_futuro.save()
            
        # except:
        #     print "1"
        
            
        return HttpResponseRedirect(reverse("producto:listar_productos"))
			
class CargarCategorias(TemplateView):
    
	def get(self,request,*args,**kwargs):
		mensaje = ""
		if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
		
		for i in request.GET:
		    tipo = i
		    
		try:
		    
		   if(tipo != 'Tipo'):
		       categorias = Categoria.objects.filter(tipo=tipo)
		       
		       mensaje = {'status':'True'}	
		       n=0
		       
		       for categoria in categorias:
		           mensaje[str(n)] = categoria.nombre
		           n = n + 1
		   else:
		       mensaje = {'status':'Tipo'}
		      
		except:
			mensaje = {'status':'False'}
			
		response = simplejson.dumps(mensaje)
		print mensaje
		return HttpResponse(response ,content_type='application/json')
		
class ListarProductos(TemplateView):
    
    def get(self,request,*args,**kwargs):
    	if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
    	    
    	productos = Producto.objects.all()
    	pag = Paginate(request, productos, 7)
    
        cxt = {
            'posts': pag['queryset'],
            'totPost': productos,
            'paginator': pag
        }
        
        # for producto in productos:
        #     if producto.tipo == 'Grasas':
        #         producto.tipo_contenido = "Libras"
        #         producto.save()
        # for producto in productos:
            
        #     if producto.tipo == 'Grasas':
                
        #         presentacion1 = Presentacion(
        #                         producto=producto,
        #                         disponibilidad = "Si",
        #                         precio=5000000,
        #                         numero_elementos = 1,
        #                         tipo_cantidad = "Libras",
        #                         cantidad = "10",
        #                         empaque = "Cunete",
        #                         )
                                
        #         presentacion1.save()
                
        #         presentacion2 = Presentacion(
        #                         producto=producto,
        #                         disponibilidad = "Si",
        #                         precio=12000000,
        #                         numero_elementos = 1,
        #                         tipo_cantidad = "Libras",
        #                         cantidad = "30",
        #                         empaque = "Cunete",
        #                         )
                                
        #         presentacion2.save()
                
        #     else:
                
        #         presentacion1 = Presentacion(
        #                         producto=producto,
        #                         disponibilidad = "Si",
        #                         precio=3000000,
        #                         numero_elementos = 1,
        #                         tipo_cantidad = "Litros",
        #                         cantidad = "5",
        #                         empaque = "Cunete",
        #                         )
                                
        #         presentacion1.save()
                
        #         presentacion1 = Presentacion(
        #                         producto=producto,
        #                         disponibilidad = "Si",
        #                         precio=10000000,
        #                         numero_elementos = 1,
        #                         tipo_cantidad = "Litros",
        #                         cantidad = "20",
        #                         empaque = "Cunete",
        #                         )
                                
        #         presentacion1.save()
                
        #         presentacion1 = Presentacion(
        #                         producto=producto,
        #                         disponibilidad = "Si",
        #                         precio=10000000,
        #                         numero_elementos = 12,
        #                         tipo_cantidad = "mL",
        #                         cantidad = "500",
        #                         empaque = "Aerosol",
        #                         )
                                
        #         presentacion1.save()
                
        
    	return render(request, 'listar_productos.html', cxt)
    
def filtrar_productos(request):
    
    if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
    
    try:
        buscar = request.GET['csrfmiddlewaretoken']
        tipo = request.GET.get('tipo')
        
    except:
        tipo = request.GET.get('tipo_re')
        
    if tipo == 'Todos':
        
        productos = Producto.objects.all()
        
    else:
        
        productos = Producto.objects.filter(tipo = tipo)
    
    pag = Paginate(request, productos, 10)
    
    contexto = {
        'posts': pag['queryset'],
        'totPost': productos,
        'paginator': pag,
        'tipo':tipo,
    }
    
    return render_to_response('listar_productos.html',contexto,
            context_instance=RequestContext(request))
    
class ModificarProducto(TemplateView):
    
    def get(self,request,*args,**kwargs):
    	
    	if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
    	print kwargs
    	id = kwargs['id_producto']
    	producto = Producto.objects.get(referencia=id)
    	
        return render_to_response('formulario_modificar_producto.html',{'producto':producto},
        	context_instance=RequestContext(request))
    
	
			
    def post(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
        print kwargs
    	id = kwargs['id_producto']
    	producto = Producto.objects.get(referencia=id)

        marca = request.POST['marca']
        tipo = request.POST['tipo']
        descripcion = request.POST['descripcion']
        
        if tipo == 'Tipo':
            mensaje = "El campo Tipo no puede ser vacio!"
            messages.info(request,mensaje)
             
            return render_to_response('formulario_modificar_producto.html',{'producto' : producto},
    			context_instance=RequestContext(request))
        
        try:
            categoria = request.POST['categoria']
        except:
            mensaje = "El campo Categoria no es valido!"
            messages.info(request,mensaje)
             
            return render_to_response('formulario_modificar_producto.html',{'producto' : producto},
    			context_instance=RequestContext(request))
            
        disponibilidad = request.POST['disponibilidad']
        grado_alimenticio = request.POST['grado_alimenticio']
        banderaImagen= False 
        banderaFS= False 
        banderaFT= False 
        banderaFC = False
        banderaFCA = False
        banderaFCL = False
        banderaFCG = False
        banderaFCC = False
        
        
        if categoria == '':
            mensaje = "El campo Categoria no puede ser vacio!"
            messages.info(request,mensaje)
             
            return render_to_response('formulario_modificar_producto.html',{'producto' : producto},
    			context_instance=RequestContext(request))
        
        #Validacion para la imagen
        try:
            imagen= request.FILES['imagen']
            
            ini, fin =  imagen.name.split(".")
            valid_extensions = ['jpg', 'png']
            if not fin in valid_extensions:
                mensaje = "El campo imagen debe tener un formato de imagen valido"
                messages.info(request,mensaje)
                 
                return render_to_response('formulario_modificar_producto.html',{'producto' : producto},
    			context_instance=RequestContext(request))
        except:
            banderaImagen = True
        
        #Validacion para Ficha Comercial
        try:
            ficha_comercial = request.FILES['ficha_comercial']
            
            ini, fin =  ficha_comercial.name.split(".")
            valid_extensions = ['pdf']
            if not fin in valid_extensions:
                mensaje = "El campo Ficha Comercial debe ser en formato PDF"
                messages.info(request,mensaje)
            
                return render_to_response('formulario_modificar_producto.html',{'producto' : producto},
    			context_instance=RequestContext(request))
        			
        except:
            banderaFC = True
            
        #Validacion para Ficha Comercial Litografias
        try:
            ficha_comercial_litografias = request.FILES['ficha_comercial_litografias']
            
            ini, fin =  ficha_comercial_litografias.name.split(".")
            valid_extensions = ['pdf']
            if not fin in valid_extensions:
                mensaje = "El campo Ficha Comercial Litografias debe ser en formato PDF"
                messages.info(request,mensaje)
            
                return render_to_response('formulario_modificar_producto.html',{'producto' : producto},
    			context_instance=RequestContext(request))
        			
        except:
            banderaFCL = True
            
        #Validacion para Ficha Comercial Gruas
        try:
            ficha_comercial_gruas = request.FILES['ficha_comercial_gruas']
            
            ini, fin =  ficha_comercial_gruas.name.split(".")
            valid_extensions = ['pdf']
            if not fin in valid_extensions:
                mensaje = "El campo Ficha Comercial gruas debe ser en formato PDF"
                messages.info(request,mensaje)
            
                return render_to_response('formulario_modificar_producto.html',{'producto' : producto},
    			context_instance=RequestContext(request))
        			
        except:
            banderaFCG = True
            
        #Validacion para Ficha Comercial Cementeras
        try:
            ficha_comercial_cementeras = request.FILES['ficha_comercial_cementeras']
            
            ini, fin =  ficha_comercial_cementeras.name.split(".")
            valid_extensions = ['pdf']
            if not fin in valid_extensions:
                mensaje = "El campo Ficha Comercial cementeras debe ser en formato PDF"
                messages.info(request,mensaje)
            
                return render_to_response('formulario_modificar_producto.html',{'producto' : producto},
    			context_instance=RequestContext(request))
        			
        except:
            banderaFCC = True
            
        #Validacion para Ficha Comercial Alimentaria
        try:
            ficha_comercial_alimentaria = request.FILES['ficha_comercial_alimentaria']
            
            ini, fin =  ficha_comercial_alimentaria.name.split(".")
            valid_extensions = ['pdf']
            if not fin in valid_extensions:
                mensaje = "El campo Ficha Comercial alimentaria debe ser en formato PDF"
                messages.info(request,mensaje)
            
                return render_to_response('formulario_modificar_producto.html',{'producto' : producto},
    			context_instance=RequestContext(request))
        			
        except:
            banderaFCA = True
        
        #Validacion Ficha Tecnica
        try:
            ficha_tecnica = request.FILES['ficha_tecnica']
            
            ini, fin =  ficha_tecnica.name.split(".")
            valid_extensions = ['pdf']
            if not fin in valid_extensions:
                mensaje = "El campo Ficha Tecnica debe ser en formato PDF"
                messages.info(request,mensaje)
            
                return render_to_response('formulario_modificar_producto.html',{'producto' : producto},
    			context_instance=RequestContext(request))
        except:
            banderaFT = True
        
        #Validacion Ficha de Seguridad
        try:
            ficha_seguridad = request.FILES['ficha_seguridad']
            
            ini, fin =  ficha_seguridad.name.split(".")
            valid_extensions = ['pdf']
            if not fin in valid_extensions:
                mensaje = "El campo Ficha Seguridad debe ser en formato PDF"
                messages.info(request,mensaje)
            
                return render_to_response('formulario_modificar_producto.html',{'producto' : producto},
                context_instance=RequestContext(request))
        except:
            banderaFS = True
                
        try:
            
            producto.marca = marca
            producto.disponibilidad = disponibilidad
            categoria = Categoria.objects.get(nombre=categoria)
            producto.categoria = categoria
            producto.tipo = tipo
            producto.descripcion = descripcion
            producto.grado_alimenticio = grado_alimenticio
            
            if not banderaFC:
                producto.ficha_comercial = ficha_comercial
            
            if not banderaFCL:
                producto.ficha_comercial_litografias = ficha_comercial_litografias
            
            if not banderaFCG:
                producto.ficha_comercial_gruas = ficha_comercial_gruas
                
            if not banderaFCA:
                producto.ficha_comercial_alimentaria = ficha_comercial_alimentaria
                
            if not banderaFCC:
                producto.ficha_comercial_cementeras = ficha_comercial_cementeras
                
            if not banderaFS:
                producto.ficha_seguridad = ficha_seguridad
                
            if not banderaFT:
                producto.ficha_tecnica = ficha_tecnica
                
            if not banderaImagen:
                producto.imagen = imagen
                
            producto.save()
            
            return HttpResponseRedirect(reverse("producto:listar_productos"))
            
        except Exception as e:
            
            print str(e)
            mensaje = "Hubo un error al cargar los datos"
            messages.info(request,mensaje)
            
            return render_to_response('formulario_modificar_producto.html',{'producto' : producto},
                context_instance=RequestContext(request))
        	
class eliminar_producto(TemplateView):
    
	def post(self,request,*args,**kwargs):
		mensaje = ""
		
		if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
		if "codigoContacto" in request.POST:
			try:
			    id_producto = request.POST['codigoContacto']
			    producto = Producto.objects.filter(referencia=id_producto)[0]
			    print producto.referencia
			    producto.disponibilidad = "No"
			    producto.save()
			    print producto.disponibilidad
			    
			    #Se eliminan del carrito todas las presentaciones del producto que se acaba de desactivar
			    usuario = request.user
			    carrito = Carrito.objects.get(encargado = usuario)
			    
			    presentaciones = carrito.presentaciones.all()
			 
			    for presentacion in presentaciones:
			        if presentacion.producto == producto: 
			            carrito.presentaciones.remove(presentacion)
			    
			    
			    mensaje = {'status':'True'}		
			    print mensaje
			except:
				mensaje = {'status':'False'}
			response = simplejson.dumps(mensaje)
			print mensaje
			return HttpResponse(response ,content_type='application/json')
			
def activar_producto(request, referencia_producto):
    
    if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
    producto = Producto.objects.get(referencia=referencia_producto)
    producto.disponibilidad = "Si"
    producto.save()


    return HttpResponseRedirect(reverse("producto:listar_productos"))
    
			
			

#CRUD PRESENTACIONES

def listar_presentaciones(request, referencia_producto):
    
    if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
    producto = Producto.objects.get(referencia=referencia_producto)
    presentaciones = Presentacion.objects.filter(producto=producto)
    
    pag = Paginate(request, presentaciones, 10)
    
    contexto = {
        'presentaciones': pag['queryset'],
        'totPost': presentaciones,
        'paginator': pag,
        'producto':producto,
    }
    
    
    return render(request, 'listar_presentaciones.html', contexto)
    
class CrearPresentacion(TemplateView):
    
    def get(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
        print kwargs
    	id = kwargs['referencia_producto']
    	producto = Producto.objects.get(referencia=id)
    	
        return render_to_response('formulario_crear_presentacion.html',{"producto":producto},
        	context_instance=RequestContext(request))


    def post(self,request,*args,**kwargs):
    	
    	if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
        print kwargs
    	id = kwargs['referencia_producto']
    	producto = Producto.objects.get(referencia=id)
    	
        disponibilidad = request.POST['disponibilidad']
        precio = request.POST['precio']
        numero_elementos = request.POST['numero_elementos']
        tipo_cantidad = request.POST['tipo_cantidad']
        cantidad = request.POST['cantidad']
        empaque = request.POST['empaque']
        unidades_en_stock = request.POST['unidades_en_stock']
        
 
    	presentacion = Presentacion(disponibilidad=disponibilidad,precio=precio,numero_elementos=numero_elementos,
    	    tipo_cantidad=tipo_cantidad,cantidad=cantidad,producto=producto, empaque=empaque, unidades_en_stock=int(unidades_en_stock))
    	presentacion.save()
    	
    	return redirect(reverse('producto:listar_presentaciones', args = (producto.referencia,)))
    	
class ModificarPresentacion(TemplateView):
    
    def get(self,request,*args,**kwargs):
    	if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
    	print kwargs
    	id = kwargs['id_presentacion']
    	presentacion = Presentacion.objects.get(id=id)
    	
        return render_to_response('formulario_modificar_presentacion.html',{'presentacion':presentacion},
        	context_instance=RequestContext(request))
    
	
			
    def post(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
        
        precio = request.POST['precio']
        cantidad = request.POST['cantidad']
        numero_elementos = request.POST['numero_elementos']
        empaque = request.POST['empaque']
        unidades_en_stock = request.POST['unidades_en_stock']
        
        try:
            disponibilidad = request.POST['disponibilidad']
            tipo_cantidad = request.POST['tipo_cantidad']
            
        except:
            mensaje = "El campo Disponibilidad o Tipo de Cantidad de Contenido tienen errores"
            messages.info(request,mensaje)
             
            return render_to_response('formulario_modificar_presentacion.html',{},
    			context_instance=RequestContext(request))
        
    	
    	id = kwargs['id_presentacion']
    	
    	presentacion = Presentacion.objects.get(id=id)
    	presentacion.precio = precio
    	presentacion.cantidad = cantidad
    	presentacion.tipo_cantidad = tipo_cantidad
    	presentacion.numero_elementos = numero_elementos
    	presentacion.disponibilidad = disponibilidad
    	presentacion.unidades_en_stock = int(unidades_en_stock)
        presentacion.save()
        	
        return redirect(reverse('producto:listar_presentaciones', args = (presentacion.producto.referencia,)))
    
class eliminar_presentacion(TemplateView):
	def post(self,request,*args,**kwargs):
		mensaje = ""
		
		if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
		if "codigoContacto" in request.POST:
			try:
			    
			    id_presentacion = request.POST['codigoContacto']
			    print id_presentacion
			    presentacion = Presentacion.objects.get(id=id_presentacion)
			    presentacion.disponible = False
			    presentacion.save()
			    
			    usuario = request.user
			    carrito = Carrito.objects.get(encargado = usuario)
			    
			    presentaciones = carrito.presentaciones.all()
			    
			    for presentacion_p in presentaciones:
			        if(presentacion_p == presentacion):
			            carrito.presentaciones.remove(presentacion_p)
			    
			    
			    mensaje = {'status':'True','codigoUsuario':id_presentacion}			
			except:
				mensaje = {'status':'False'}
			response = simplejson.dumps(mensaje)
			print mensaje
			return HttpResponse(response ,content_type='application/json')
			
class activar_presentacion(TemplateView):
	def post(self,request,*args,**kwargs):
		mensaje = ""
		
		if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
		if "codigoContacto" in request.POST:
			try:
			    
			    id_presentacion = request.POST['codigoContacto']
			    print id_presentacion
			    presentacion = Presentacion.objects.get(id=id_presentacion)
			    presentacion.disponible = True
			    presentacion.save()
			    
			    
			    mensaje = {'status':'True','codigoUsuario':id_presentacion}			
			except:
				mensaje = {'status':'False'}
			response = simplejson.dumps(mensaje)
			print mensaje
			return HttpResponse(response ,content_type='application/json')
			
def carrito_presentacion(request, id_presentacion):
    
    if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
    
    usuario = request.user
    carrito = Carrito.objects.get(encargado=usuario)
    presentacion = Presentacion.objects.get(id=id_presentacion)
    
    if len(carrito.presentaciones.all()) == 13:
        producto = Producto.objects.get(referencia=presentacion.producto.referencia)
        presentaciones = Presentacion.objects.filter(producto=producto)
    
        mensaje = "El Carrito de compra esta lleno! max 14 unidades."
        messages.info(request,mensaje)
        
        return render(request, 'listar_presentaciones.html', {"producto":producto, "presentaciones":presentaciones})
        
    carrito.presentaciones.add(presentacion)
    carrito.save()
    
    mensaje = "Se ha agregado el item exitosamente."
    messages.info(request,mensaje)
    
    producto = Producto.objects.get(referencia=presentacion.producto.referencia)
    presentaciones = Presentacion.objects.filter(producto=producto)
    
    return render(request, 'listar_presentaciones.html', {"producto":producto, "presentaciones":presentaciones})
    	
    	

#CRUD INDUSTRIA

class crearIndustria(TemplateView):

    
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
        
        lubricantes_industriales = Producto.objects.filter(tipo="Lubricantes Industriales")
        grasas = Producto.objects.filter(tipo="Grasas")
        print grasas 
        aditivos= Producto.objects.filter(tipo="Aditivos")
        soldadura_antorcha = Producto.objects.filter(tipo="Soldadura para Antorcha")
        soldadura_arco = Producto.objects.filter(tipo="Soldadura para Arco")
        soldadura_tig = Producto.objects.filter(tipo="Soldadura TIG")
        quimicos = Producto.objects.filter(tipo="Quimicos")
        otros = Producto.objects.filter(tipo="Otros")
        
        context = {
             
            'lubricantes_industriales':lubricantes_industriales,
            'grasas' : grasas,
            'aditivos' : aditivos,
            'soldadura_antorcha':soldadura_antorcha,
            'soldadura_arco' : soldadura_arco,
            'quimicos' : quimicos,
            'otros' : otros
        }
        
    	return render_to_response('formulario_crear_industria.html',context,
    			context_instance=RequestContext(request))
    			
    			

    def post(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
        nombre = request.POST['nombre']
        productos = request.POST.getlist('productos')
        
        #Validacion para la imagen
        try:
            imagen= request.FILES['imagen']
            
            ini, fin =  imagen.name.split(".")
            valid_extensions = ['jpg', 'png']
            if not fin in valid_extensions:
                mensaje = "El campo imagen debe tener un formato de imagen valido"
                messages.info(request,mensaje)
                 
                return render_to_response('formulario_crear_industria.html',{},
        			context_instance=RequestContext(request))
        			
        except:
            mensaje = "El campo imagen No puede ser vacio"
            messages.info(request,mensaje)
            
            return render_to_response('formulario_crear_industria.html',{},
			context_instance=RequestContext(request))
        
        
        industria = Industria(nombre = nombre, imagen = imagen)
        
        industria.save()
        
        for producto in productos:
            
            producto = Producto.objects.get(referencia = producto)
            industria.productos.add(producto)
        
        industria.save()
        
            
        return HttpResponseRedirect(reverse("producto:listar_industrias"))
        
class listarIndustria(TemplateView):
    
    def get(self,request,*args,**kwargs):
    
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
        
        industrias = Industria.objects.all()
        
        for industria in industrias:
            primera_industria = industria.nombre
            primera_industria_id = industria.id
            productos_primera_industria = industria.productos.all()
            break
        
        pag = Paginate(request, productos_primera_industria, 10)
        
        contexto = {
            'productos_primera_industria' : pag['queryset'],
            'paginator' : pag,
            'industrias' : industrias,
            'primera_industria' : primera_industria,
            'primera_industria_id' : primera_industria_id,
            'industria_objecto': industria,
        }
        
        print industria.disponible
        
        return render_to_response('listar_industria.html', contexto,
        			context_instance=RequestContext(request))
    	
def filtrar_industrias(request):
    
    if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
    
    try:
        buscar = request.GET['csrfmiddlewaretoken']
        industria_id = request.GET.get('industria_id')
    except:
        industria_id = request.GET.get('industria_id_re')
        
    
    industrias = Industria.objects.all()
    industria = Industria.objects.get(id=industria_id)
    
    
    primera_industria = industria.nombre
    primera_industria_id = industria.id
    productos_primera_industria = industria.productos.all()
    
        
    pag = Paginate(request, productos_primera_industria, 10)
        
    contexto = {
        'productos_primera_industria' : pag['queryset'],
        'paginator' : pag,
        'industrias' : industrias,
        'primera_industria' : primera_industria,
        'primera_industria_id' : primera_industria_id,
        'industria' : industria_id,
        'industria_objecto': industria,
    }
    
    return render_to_response('listar_industria.html', contexto,
    			context_instance=RequestContext(request))
        
class eliminar_industria(TemplateView):
	def post(self,request,*args,**kwargs):
		mensaje = ""
		
		if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
		if "codigoContacto" in request.POST:
			try:
			    id_industria = request.POST['codigoContacto']
			    industria = Industria.objects.get(id=id_industria)
			    industria.disponible = False
			    industria.save()
			    
			    mensaje = {'status':'True','codigoUsuario':id_industria}			
			except:
				mensaje = {'status':'False'}
			response = simplejson.dumps(mensaje)
			print mensaje
			return HttpResponse(response ,content_type='application/json')
			
class activar_industria(TemplateView):
	def post(self,request,*args,**kwargs):
		mensaje = ""
		
		if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
		if "codigoContacto" in request.POST:
			try:
			    id_industria = request.POST['codigoContacto']
			    industria = Industria.objects.get(id=id_industria)
			  
			    industria.disponible = True
			    industria.save()
			    
			    mensaje = {'status':'True','codigoUsuario':id_industria}			
			except:
				mensaje = {'status':'False'}
			response = simplejson.dumps(mensaje)
			print mensaje
			return HttpResponse(response ,content_type='application/json')
			
class ModificarIndustria(TemplateView):
    
    def get(self,request,*args,**kwargs):
    	if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
    	print kwargs
    	id = kwargs['id_industria']
    	industria = Industria.objects.get(id=id)
    	productos = industria.productos.all()
    	productos_id = []
    	
    	for producto in productos:
    	    productos_id.append(producto.referencia)
    	    
    	productos_filtrados = Producto.objects.all().exclude(referencia__in=productos_id)
    	
    	lubricantes_industriales = productos_filtrados.filter(tipo="Lubricantes Industriales")
        grasas = productos_filtrados.filter(tipo="Grasas")
        aditivos= productos_filtrados.filter(tipo="Aditivos")
        soldadura_antorcha = productos_filtrados.filter(tipo="Soldadura para Antorcha")
        soldadura_arco = productos_filtrados.filter(tipo="Soldadura para Arco")
        soldadura_tig = productos_filtrados.filter(tipo="Soldadura TIG")
        quimicos = productos_filtrados.filter(tipo="Quimicos")
        otros = productos_filtrados.filter(tipo="Otros")
        
        context = {
             
            'lubricantes_industriales':lubricantes_industriales,
            'grasas' : grasas,
            'aditivos' : aditivos,
            'soldadura_antorcha':soldadura_antorcha,
            'soldadura_arco' : soldadura_arco,
            'quimicos' : quimicos,
            'industria':industria,
            'otros' : otros
        }
    	
        return render_to_response('formulario_modificar_industria.html',context,
        	context_instance=RequestContext(request))
    
	
			
    def post(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
            
        id = kwargs['id_industria']
        industria = Industria.objects.get(id=id)
        nombre = request.POST['nombre']
        productos = request.POST.getlist('productos')
        
        
        try:
            imagen= request.FILES['imagen']
            mensaje = "El campo imagen debe tener un formato de imagen valido"
            messages.info(request,mensaje)
            ini, fin =  imagen.name.split(".")
            valid_extensions = ['jpg', 'png']
            
            if not fin in valid_extensions:
                return render_to_response('formulario_modificar_industria.html',{'industria':industria},
                context_instance=RequestContext(request))
            
            industria.nombre = nombre
            industria.imagen = imagen
            
            for producto in productos:
            
                producto = Producto.objects.get(referencia = producto)
                industria.productos.add(producto)
            
            industria.save()
            	
            return HttpResponseRedirect(reverse("producto:listar_industrias"))		
        			
			
        except:
    			
        	industria.nombre = nombre
        	
        	for producto in productos:
        	    producto = Producto.objects.get(referencia = producto)
        	    industria.productos.add(producto)
                
        	industria.save()
        	
        	return HttpResponseRedirect(reverse("producto:listar_industrias"))
        
class eliminar_producto_industria(TemplateView):
    
	def post(self,request,*args,**kwargs):
		mensaje = ""
		
		if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
		
		id = kwargs['id_industria']
		
		if "codigoContacto" in request.POST:
			try:
			    id_producto = request.POST['codigoContacto']
			    producto = Producto.objects.get(referencia=id_producto)
			    industria = Industria.objects.get(id=id)
			    industria.productos.remove(producto)
			    
			    mensaje = {'status':'True','codigoUsuario':id_producto}			
			except:
				mensaje = {'status':'False'}
			response = simplejson.dumps(mensaje)
			print mensaje
			return HttpResponse(response ,content_type='application/json')
    
    
    
    			
            
                
def generar_presentaciones_automaticas(request):
    
    
    # productos = Producto.objects.all()
    # carrito = Carrito.objects.get(encargado = request.user)
    
    # for producto in productos:
        
    #     if(producto.tipo == "Lubricantes Industriales"):
            
    #         presentacion = Presentacion(disponibilidad="Si",precio="5000000",numero_elementos="1",
    # 	    tipo_cantidad="Litros",cantidad="5",producto=producto, empaque="Cunete", unidades_en_stock=100)
    	    
    # 	    presentacion.save()
    	    
    # 	    carrito.presentaciones.add(presentacion)
    	    
    # 	elif producto.tipo == "Quimicos":
    	    
    # 	    presentacion = Presentacion(disponibilidad="Si",precio="1500000",numero_elementos="12",
    # 	    tipo_cantidad="mL",cantidad="500",producto=producto, empaque="Aerosoles", unidades_en_stock=100)
    	    
    # 	    presentacion.save()
    	    
    # 	    carrito.presentaciones.add(presentacion)
    	    
    # 	elif producto.tipo == "Grasas":
    	    
    # 	    presentacion = Presentacion(disponibilidad="Si",precio="1500000",numero_elementos="1",
    # 	    tipo_cantidad="Libras",cantidad="10",producto=producto, empaque="Cunete", unidades_en_stock=100)
    	    
    # 	    presentacion.save()
    	    
    # 	    carrito.presentaciones.add(presentacion)
    
    # Producto.objects.get(referencia = "1234567898").delete()	    
    return HttpResponseRedirect(reverse('facturacion:generar_factura'))	    