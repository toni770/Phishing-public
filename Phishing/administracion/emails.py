#from redmail import outlook

import smtplib
from datetime import date

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def enviar( usuario, contraseña, destino, asunto, contenido, link_status, link_login):
    # print("Enviando correo")
    # print("Usuario: " + usuario)
    # print("Contraseña: " + contraseña)
    # print("Destino: " + str(destino))
    # print("Asunto: " + asunto)
    # print("Contenido: " + contenido)

    #Variables de configuración
    mail_origen = str(usuario)
    password = contraseña
    mail_destino = str(destino)

    #Creamos el  mensaje con MIME
    contenido_mensaje = MIMEMultipart()
    contenido_mensaje['From'] = 'Info'#mail_origen
    contenido_mensaje['To'] = mail_destino
    contenido_mensaje['Subject'] = asunto
    contenido_mensaje['Date'] = str(date.today())

    print (contenido_mensaje)
    #Remplazamos los enlaces
    contenido = contenido.replace("8888", link_status)
    contenido = contenido.replace("9999", link_login)
    #contenido = contenido.replace("pruebaprueba", 'https://www.google.es/')
    
    #Adjuntamos el contenido como html
    contenido_mensaje.attach(MIMEText(contenido,"html"))

    #Lo transformamos en string
    email_string = contenido_mensaje.as_string()

    #Enviamos el mensaje
    s = smtplib.SMTP("mail.wallaputas.com",587)
    s.starttls()
    s.login(mail_origen, password)
    s.sendmail(mail_origen, mail_destino, email_string)
    s.quit()

    
    # outlook.username = 'acount.googIe@outlook.es'
    # outlook.password = 'O@CBHec1D#'

    # outlook.send(
    #     receivers=['toni-mr-1996@hotmail.com'],
    #     subject=asunto,
    #     text=email_string,
    # )