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
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from Facturacion.models import Carrito
from django.core.mail import EmailMessage
# Create your views here.


class CrearUsuario(TemplateView):
    
    def get(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
    	return render_to_response('formulario_crear_usuario.html',{},
	    		context_instance=RequestContext(request))
		    			

    def post(self,request,*args,**kwargs):
    	
    	if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
        nombres = request.POST['nombre']
        apellido = request.POST['apellido']
        email = request.POST['email']
        inputPassword = request.POST['inputPassword']
        nombreDeUsuario = request.POST['nombredeusuario']
        
        
        try:
            
            usuario = User(first_name=nombres, last_name = apellido, email = email, username = nombreDeUsuario)
            usuario.save()
            usuario.set_password(inputPassword)
            usuario.save()
            
            print "y"
            carrito = Carrito(encargado=usuario)
            carrito.save()
            print "w"
            
            return HttpResponseRedirect(reverse("usuario:listar_usuarios"))
            
        except Exception as e:
            
            print str(e)
            mensaje = "Error al crear el Usuario"
            messages.info(request,mensaje)
            
            return render_to_response('formulario_crear_usuario.html',{},
                context_instance=RequestContext(request))
                
def listar_usuarios(request):
    if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
    usuarios = User.objects.all()
    return render_to_response('listar_usuarios.html',{'usuarios':usuarios},
	    		context_instance=RequestContext(request))
	    		
class ModificarUsuario(TemplateView):
    
    def get(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
        try:

            id = request.GET['codigoUsuario']
            usuario = User.objects.get(id=id)
            
            try:
                nombres = request.GET['nombres']
                apellido = request.GET['apellido']
                email = request.GET['email']
                
                usuario.first_name = nombres
                usuario.last_name = apellido
                usuario.email = email
                
            except:
                mensaje = "Error al editar el Usuario"
                messages.info(request,mensaje)
                
                return render_to_response('formulario_modificar_usuario.html',{},
                    context_instance=RequestContext(request))
                    
            
            usuario.save()
            
            try:
                
                inputPassword = request.GET['inputPassword']
                
                if inputPassword != "":
                    usuario.set_password(inputPassword)
                    usuario.save()
                    
                    
                return HttpResponseRedirect(reverse("usuario:listar_usuarios"))
                
            except:
                
                return HttpResponseRedirect(reverse("usuario:listar_usuarios"))
            
         
        except:   
            id = kwargs['id_usuario']
            usuario = User.objects.get(id=id)
            
            return render_to_response('formulario_modificar_usuario.html',{'usuario':usuario, 'id':usuario.id},
            		context_instance=RequestContext(request))

class eliminar_usuario(TemplateView):
    
	def post(self,request,*args,**kwargs):
		mensaje = ""
		
		if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
			
		if "codigoContacto" in request.POST:
			try:
			    id_contacto = request.POST['codigoContacto']
			    usuario = User.objects.get(id=id_contacto)
			    usuario.is_active = False
			    usuario.save()
			    
			    
			    mensaje = {'status':'True','codigoUsuario':id_contacto}			
			except:
				mensaje = {'status':'False'}
			response = simplejson.dumps(mensaje)
			print mensaje
			return HttpResponse(response ,content_type='application/json')    
			
class activar_usuario(TemplateView):
    
	def post(self,request,*args,**kwargs):
		mensaje = ""
		
		if not request.user.is_authenticated() or not request.user.is_active:
			return HttpResponseRedirect(reverse("usuario:error_403"))
		if "codigoContacto" in request.POST:
			try:
			    id_contacto = request.POST['codigoContacto']
			    usuario = User.objects.get(id=id_contacto)
			    usuario.is_active = True
			    usuario.save()
			    
			    
			    mensaje = {'status':'True','codigoUsuario':id_contacto}			
			except:
				mensaje = {'status':'False'}
			response = simplejson.dumps(mensaje)
			print mensaje
			return HttpResponse(response ,content_type='application/json')    
			
def loginIn(request):

	if request.method == 'POST':
			
			usuario = request.POST['username']
			clave = request.POST['password']
			
			print usuario
			print clave
			
			user = authenticate(username=usuario, password=clave)
			
			if user is not None:
			
				if user.is_active:
				
					login(request, user)
					usuario = User.objects.get(id=user.id)
					
					return HttpResponseRedirect(reverse("usuario:listar_usuarios"))
				
				
				else:
				
					messages.error(request, 'No esta activado este usuario por favor hablar con un administrador')
					print "No esta activo"
					return render(request, "login.html")
			
			else:
			
				username = None
				if request.user.is_authenticated():
					username = request.user.username
			
				messages.error(request, 'Hubo un problema con el usuario y/o contrasena')
				return render(request, "login.html", {"usuario" : username})
				
	else:
	    return render(request, "login.html", {})
		
def logout_view(request):
    
    logout(request)
    
    return HttpResponseRedirect(reverse("home"))
    
def error_403(request):
    return render(request, "extra_403_error.html", {})
    
class coming_soon(TemplateView):
    
    def get(self,request,*args,**kwargs):
        return render(request, "extra_coming_soon.html", {})
        
    def post(self,request,*args,**kwargs):
        
        correo = request.POST['correo']
        
        cuerpo = "El correo " + correo + " desea ser contactado."
        email = EmailMessage('Peticion Contactenos Pagina Web', cuerpo, to=['ventas@soltecaindustrial.co'])
        email.send()
        
        return render(request, "index.html", {})
        
    
    
    
