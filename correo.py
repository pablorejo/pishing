import smtplib 
from email.message import EmailMessage 
import chatgpt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import variables
import random
import time


tiempo_inicio = time.time()



# Set smtp server and port
server = smtplib.SMTP(variables.EMAIL_SMPT, variables.PUERTO_SMPT)

# Identify this client to the SMTP server
server.ehlo()

# Secure the SMTP connection
server.starttls()

# Login to email account
server.login(variables.CORREO_EMISOR, variables.CLAVE_CORREO)

nombres_y_objetivos = []

if (variables.GENERAR_OBJETIVOS):
    print("\nEsta seleccionado el modo generador de nombres de empresas\n")
    nombres_y_objetivos = chatgpt.GenerarNombresYObjetivos()


# Saber cual es el array que vamos a usar
array = []
if variables.GENERAR_CORREOS:
    array = chatgpt.GenerarCorreos()
else:   
    print("Obteniendo correos de la lista predefinida")
    contenido = ""
    with open('correos.txt', 'r') as archivo:
        contenido = archivo.read()  # Lee todo el contenido del archivo
    array = str(contenido).split("\n")

for correo in array:
    if correo == "" or "@" not in correo: # Esto indica el final de la lista de correos
        print(correo)
        break
    
    correo = str(correo).strip()

    #Variables
    if (variables.GENERAR_OBJETIVOS):
        numero_aleatorio = random.randint(0, variables.NUMERO_DE_EMPRESAS)
        if numero_aleatorio >= len(nombres_y_objetivos):
            numero_aleatorio = len(nombres_y_objetivos)-1

        nombre_empresa=nombres_y_objetivos[numero_aleatorio][0]
        objetivo_empresa=nombres_y_objetivos[numero_aleatorio][1]

        print(f"El nombre de la empresa será: {nombre_empresa} y su objetivo será: {objetivo_empresa}")
        contenido = chatgpt.CrearCorreo(correo=correo,nombre_empresa=nombre_empresa,objetivo_empresa=objetivo_empresa)
        asunto = chatgpt.ObtenerAsunto(objetivo=nombres_y_objetivos[numero_aleatorio][1])

    else:
        contenido = chatgpt.CrearCorreo(correo=correo,nombre_empresa=nombres_y_objetivos)
        asunto = chatgpt.ObtenerAsunto()

    print("Enviando el correo")

    # Crear el mensaje MIME multipart
    message = MIMEMultipart()
    message['Subject'] = asunto
    message['From'] = variables.CORREO_EMISOR
    message['To'] = correo

    contenido_html = contenido

    contenido_correo = MIMEText(contenido_html, 'html')
    message.attach(contenido_correo)
    
    if (variables.GENERAR_OBJETIVOS):
        for n in range(0,variables.NUMERO_DE_IMAGENES):
            # Adjuntar la imagen
            with open(f'{variables.CARPETA_IMAGENES}nombre_de_la_imagen_{n}.jpg', 'rb') as imagen_file:
                imagen = MIMEImage(imagen_file.read())
                imagen.add_header('Content-Disposition', 'inline', filename=f'{variables.CARPETA_IMAGENES}nombre_de_la_imagen_{n}.jpg')
                imagen.add_header('Content-ID', f'<imagen_adjunta_{n}>')
                message.attach(imagen)
            
    # Send email
    server.send_message(message)
    print (f"Correo Enviado a {correo}\n\n")


server.quit()
tiempo_fin = time.time()
tiempo_total = tiempo_fin - tiempo_inicio

print(f"El programa tardó {tiempo_total:.2f} segundos en ejecutarse.")