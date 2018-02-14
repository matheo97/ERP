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
#Paginador
from django.core.paginator import Paginator


#CRUD CLIENTES
class CrearCliente(TemplateView):
    
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
    	return render_to_response('formulario_crear_cliente.html',{},
    			context_instance=RequestContext(request))


    def post(self,request,*args,**kwargs):
    	
    	if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
        razon_social = request.POST['razon_social']
        nit = request.POST['nit']
        sigla = request.POST['sigla']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        conti = request.POST['conti']
        pais = request.POST['pais']
        tipo = request.POST['tipo']
        
        if conti == 'Departamento' or pais == 'Ciudad':
            
            mensaje = "Los campos departamento y ciudad son obligatorios"
            messages.info(request,mensaje)
            
            return render(request, 'formulario_crear_cliente.html', {})
        
        elif pais == '':
            
            mensaje = "Los campos departamento y ciudad son obligatorios"
            messages.info(request,mensaje)
            
            return render(request, 'formulario_crear_cliente.html', {})
        	
        try:
            cliente = Cliente.objects.get(nit=nit)
            mensaje = "Ya existe un Cliente con ese NIT"
            messages.info(request,mensaje)
            
            return render(request, 'formulario_crear_cliente.html', {})
            
        except:
        	
        	cliente = Cliente(nit = nit, razon_social = razon_social, telefono = telefono, sigla = sigla, direccion = direccion,
        						departamento = conti, ciudad = pais, tipo = tipo)
        	cliente.save()
        	
        	return render(request, 'formulario_crear_cliente.html', {})
        	
class ModificarCliente(TemplateView):
    
    def get(self,request,*args,**kwargs):
    	if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
    	
    	id = kwargs['id_cliente']
    	cliente = Cliente.objects.get(nit=id)
    	
    	
    	contexto = {
    	    
    	    'cliente':cliente, 
    	    "razon_social":cliente.razon_social, 
    	    "sigla":cliente.sigla, 
    	    "direccion" : cliente.direccion, 
    	    "telefono": cliente.telefono
    	}
    	
        return render_to_response('formulario_modificar_cliente.html', contexto,
        	context_instance=RequestContext(request))
    
    
			
    def post(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
        razon_social = request.POST['razon_social']
        sigla = request.POST['sigla']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        
        id = kwargs['id_cliente']
    	cliente = Cliente.objects.get(nit=id)
    	
    	cliente.razon_social = razon_social
    	cliente.sigla = sigla
    	cliente.direccion = direccion
    	cliente.telefono = telefono
    	
        cliente.save()
        	
        return HttpResponseRedirect(reverse("cliente:listar_clientes"))
        
class listar_clientes(TemplateView):
    
    def get(self,request,*args,**kwargs):
    	if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
    	
    	    
        clientes = Cliente.objects.all()
        pag = self.Paginate(request, clientes, 10)
        
        cxt = {
            'posts': pag['queryset'],
            'totPost': clientes,
            'paginator': pag
        }
        
            
        
        return render(request, 'listar_clientes.html', cxt)
    
        
    def Paginate(self, request, queryset, pages):
       
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
        
def visualizar_cliente(request, id_cliente):
    if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
    cliente = get_object_or_404(Cliente, nit=id_cliente)
    return render(request, 'visualizar_cliente.html', {'cliente':cliente})

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
        
class buscar_cliente(TemplateView):
    
    
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
        
        try:
            buscar = request.GET['csrfmiddlewaretoken']
            nombre = request.GET.get('nombre')
        except:
            nombre = request.GET.get('nombre_re')
        
        try:
            buscar = request.GET['csrfmiddlewaretoken']
            departamento = request.GET.get('select_departamento')
        except:
            departamento = request.GET.get('departamento_re')
            
        try:
            buscar = request.GET['csrfmiddlewaretoken']
            tipo = request.GET.get('select_tipo')
        except:
            tipo = request.GET.get('tipo_re')
            
        
        
        if departamento == "Departamento" and tipo == "Tipo" and nombre == "":
            clientes = Cliente.objects.all()
            
        elif departamento == "Departamento" and tipo == "Tipo":
            clientes = Cliente.objects.filter(sigla__contains=nombre)
        elif nombre == "" and tipo == "Tipo":
            clientes = Cliente.objects.filter(departamento=departamento)
        elif nombre == "" and departamento == "Departamento":
            clientes = Cliente.objects.filter(tipo=tipo)
            
        elif departamento == "Departamento":
            clientes = Cliente.objects.filter(tipo = tipo, sigla__contains=nombre)
        elif tipo == "Tipo":
            clientes = Cliente.objects.filter(departamento = departamento, sigla__contains=nombre)
        elif nombre == "":
            clientes = Cliente.objects.filter(departamento = departamento, tipo=tipo)
            
        else:
            clientes = Cliente.objects.filter(departamento = departamento, tipo = tipo, sigla__contains=nombre)
        
        
        pag = Paginate(request, clientes, 10)
        
        cxt = {
            'posts': pag['queryset'],
            'totPost': clientes,
            'paginator': pag,
            'tipo' : tipo,
            'departamento' : departamento,
            'nombre' : nombre
        }
        
        return render(request, 'listar_clientes.html', cxt)
    
    
#CRUD CONTACTOS
    
class CrearContacto(TemplateView):
    
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
        print kwargs
    	id = kwargs['id_cliente']
    	cliente = Cliente.objects.get(nit=id)
    	
        return render_to_response('formulario_crear_contacto.html',{"cliente":cliente},
        	context_instance=RequestContext(request))


    def post(self,request,*args,**kwargs):
    	if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
    	print kwargs
    	id = kwargs['id_cliente']
    	cliente = Cliente.objects.get(nit=id)
    	
        nombre = request.POST['nombre']
        correo_electronico = request.POST['correo']
        telefono = request.POST['telefono']
        extension = request.POST['extension']
        telefono = request.POST['telefono']
        celular = request.POST['celular']
        cargo = request.POST['cargo']
 
    	contacto = Contacto(nombre = nombre, correo_electronico = correo_electronico, telefono = telefono, celular = celular,
    						cargo = cargo, empresa = cliente, extension=extension)
    	contacto.save()
    	
    	return redirect(reverse('cliente:listar_contactos', args = (cliente.nit,)))
    	#return render(request, 'formulario_crear_cliente.html', {})

def listar_contactos(request, id_cliente):
    if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
    cliente = Cliente.objects.get(nit=id_cliente)
    contactos = Contacto.objects.filter(empresa=cliente.nit)
    
    pag = Paginate(request, contactos, 10)
        
    cxt = {
        'posts': pag['queryset'],
        'totPost': contactos,
        'paginator': pag,
        'cliente' : cliente
    }
        
    return render(request, 'listar_contacto.html', cxt)
    
class ModificarContacto(TemplateView):
    
    def get(self,request,*args,**kwargs):
    	if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
    	print kwargs
    	id = kwargs['id_contacto']
    	contacto = Contacto.objects.get(id=id)
    	
        return render_to_response('formulario_modificar_contacto.html',{'contacto':contacto},
        	context_instance=RequestContext(request))
    
	
			
    def post(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
        nombre = request.POST['nombre']
        correo_electronico = request.POST['correo']
        telefono = request.POST['telefono']
        extension = request.POST['extension']
        celular = request.POST['celular']
        cargo = request.POST['cargo']
    	
    	id = kwargs['id_contacto']
    	
    	contacto = Contacto.objects.get(id=id)
    	contacto.nombre = nombre
    	contacto.correo_electronico = correo_electronico
    	contacto.telefono = telefono
    	contacto.celular = celular
    	contacto.cargo = cargo
    	contacto.extension = extension
    	
        contacto.save()
        	
        return redirect(reverse('cliente:listar_contactos', args = (contacto.empresa.nit,)))
    
class DesactivarContacto(TemplateView):
	def post(self,request,*args,**kwargs):
		mensaje = ""
		if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
		if "codigoContacto" in request.POST:
			try:
			    id_contacto = request.POST['codigoContacto']
			    Contacto.objects.filter(id=id_contacto).delete()
			    
			    mensaje = {'status':'True','codigoUsuario':id_contacto}			
			except:
				mensaje = {'status':'False'}
			response = simplejson.dumps(mensaje)
			print mensaje
			return HttpResponse(response ,content_type='application/json')
		
def carrito_contacto(request, id_contacto):
    
    if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
    
    usuario = request.user
    carrito = Carrito.objects.get(encargado=usuario)
    contacto = Contacto.objects.get(id=id_contacto)
    carrito.contacto = contacto.id
    carrito.cliente = contacto.empresa.nit
    carrito.save()
    
    messages.add_message(request, messages.SUCCESS, "Se ha agregado el contacto exitosamente.")
    
    cliente = Cliente.objects.get(nit=contacto.empresa.nit)
    contactos = Contacto.objects.filter(empresa=cliente.nit)
    
    return render_to_response('listar_contacto.html',{"posts":contactos, "cliente":cliente},
        	context_instance=RequestContext(request))
        
		