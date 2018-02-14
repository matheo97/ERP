from django.shortcuts import render
from Producto.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

def home(request):
	return render(request, "index.html", {})
	
def about_us(request):
	return render(request, "about-us.html", {})

class contact_us(TemplateView):
	
	def get(self,request,*args,**kwargs):
		
		return render(request, "contact-us.html", {})
	@csrf_exempt
	def post(self,request,*args,**kwargs):
		
		nombre = request.POST['nombre']
		apellido = request.POST['apellido']
		correo = request.POST['email']
		mensaje = request.POST['mensaje']
		
		cuerpo = "Nombre: " + nombre + " " + apellido + "\n\n" + "Email: " + correo + "\n\n" + mensaje
		
		email = EmailMessage('Peticion Contactenos Pagina Web', cuerpo, to=['ventas@soltecaindustrial.co'])
		email.send()
		
		return render(request, "contact-us.html", {})
        
def portafolio(request, id_tipo):
	
	if id_tipo == "1":
		categorias = Categoria.objects.filter(tipo = "Lubricantes Industriales")
		return render(request, "categorias.html", {'categorias':categorias, 'tipo' : 'Lubricantes Industriales'})
	elif id_tipo == "2":
		categorias = Categoria.objects.filter(tipo = "Grasas")
		return render(request, "categorias.html", {'categorias':categorias, 'tipo' : 'Grasas'})
	elif id_tipo == "3":
		categorias = Categoria.objects.filter(tipo = "Aditivos")
		return render(request, "categorias.html", {'categorias':categorias, 'tipo' : 'Aditivos'})
	elif id_tipo == "4":
		categorias = Categoria.objects.filter(tipo = "Soldadura para Antorcha")
		return render(request, "categorias.html", {'categorias':categorias, 'tipo' : 'Lubricantes Industriales'})
	elif id_tipo == "5":
		categorias = Categoria.objects.filter(tipo = "Soldadura para Arco")
		return render(request, "categorias.html", {'categorias':categorias, 'tipo' : 'Soldadura para Arco'})
	elif id_tipo == "6":
		categorias = Categoria.objects.filter(tipo = "Soldadura TIG")
		return render(request, "categorias.html", {'categorias':categorias, 'tipo' : 'Soldadura TIG'})
	elif id_tipo == "7":
		categorias = Categoria.objects.filter(tipo = "Quimicos")
		return render(request, "categorias.html", {'categorias':categorias, 'tipo' : 'Quimicos'})
	else:
		categorias = Categoria.objects.filter(tipo = "Otros")
		return render(request, "categorias.html", {'categorias':categorias, 'tipo' : 'Otros'})
	
def productos_categoria(request, id_categoria):
	categoria = Categoria.objects.get(id= id_categoria)
	productos = Producto.objects.filter(categoria = categoria)
	return render(request, "productos.html", {'categoria' : categoria.nombre, 'productos':productos})
	
def productos_industria(request, id_industria):
	
	industria = Industria.objects.get(id= id_industria)
	productos = industria.productos.all()
	
	
	if industria.nombre == "Litografias":
		
		if len(productos) == 0:
			return HttpResponseRedirect(reverse('usuario:coming_soon'))
		else:
			return render(request, "productos_litografias.html", {'industria' : industria.nombre, 'productos':productos})
		
		
	elif industria.nombre == "Cementeras":
		
		if len(productos) == 0:
			return HttpResponseRedirect(reverse('usuario:coming_soon'))
		else:
			return render(request, "productos.html", {'industria' : industria.nombre, 'productos':productos})
		
	elif industria.nombre == "Gruas":
		
		if len(productos) == 0:
			return HttpResponseRedirect(reverse('usuario:coming_soon'))
		else:
			return render(request, "productos.html", {'industria' : industria.nombre, 'productos':productos})
		
	elif industria.nombre == "Alimentaria":
		
		if len(productos) == 0:
			return HttpResponseRedirect(reverse('usuario:coming_soon'))
		else:
			return render(request, "productos.html", {'industria' : industria.nombre, 'productos':productos})
			
	else:
		
		if len(productos) == 0:
			return HttpResponseRedirect(reverse('usuario:coming_soon'))
		else:
			return render(request, "productos.html", {'industria' : industria.nombre, 'productos':productos})
	
def mostrar_grado_alimenticio(request):
	#return render(request, "alimenticio_por_productos.html")
	return HttpResponseRedirect(reverse('usuario:coming_soon'))
	
def resultado_productos(request,id_tipo):
	
	productos = Producto.objects.filter(grado_alimenticio = "Si")
	
	if id_tipo == "1":
		productos = productos.filter(tipo = "Lubricantes Industriales")
		return render(request, "productos.html", {'productos':productos})
	elif id_tipo == "2":
		productos = productos.filter(tipo =  "Grasas")
		return render(request, "productos.html", {'productos':productos})
	elif id_tipo == "3":
		productos = productos.filter(tipo =  "Aditivos")
		return render(request, "productos.html", {'productos':productos})
	elif id_tipo == "4":
		productos = productos.filter(tipo =  "Soldadura para Antorcha")
		return render(request, "productos.html", {'productos':productos})
	elif id_tipo == "5":
		productos = productos.filter(tipo = "Soldadura para Arco")
		return render(request, "productos.html", {'productos':productos})
	elif id_tipo == "6":
		productos = productos.filter(tipo =  "Soldadura TIG")
		return render(request, "productos.html", {'productos':productos})
	elif id_tipo == "7":
		productos = productos.filter(tipo =  "Quimicos")
		return render(request, "productos.html", {'productos':productos})
	else:
		productos = productos.filter(tipo =  "Otros")
		return render(request, "productos.html", {'productos':productos})
	
def industria(request):
	industrias = Industria.objects.all()
	return render(request, "industrias.html", {'industrias':industrias})
	
def videos(request):
	return render(request, "videos.html")
	
def email_contactenos(request):
	
	if request.POST:
		
		try:
			nombre = request.POST['nombre']
			apellido = request.POST['apellido']
			email = request.POST['email']
			mensaje = request.POST['mensaje']
			
			print nombre
			print apellido
			
		except:
			print ""
			
