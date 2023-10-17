# Correo desde el que vamos a enviar los mensajes
CORREO_EMISOR = "tu-correo@lo-que-sea"

# Configuracion del servidor SMTP
EMAIL_SMPT = "smtp.gmail.com" 
PUERTO_SMPT = '587'

# Modelo que vamos a usar en el chat
Modelos_de_chat = {1:"gpt-3.5-turbo" , 2:"gpt-4"}
MODELO_DEL_CHAT = Modelos_de_chat[2]

# Elegir si queremos un objetivo en concreto o queremos que se generen automaticamente
GENERAR_OBJETIVOS = True

# Numero de empresas a generar
NUMERO_DE_EMPRESAS = 3

#Nombre de la persona que enviara el correo
NOMBRE_PERSONA_EMPRESA = "Geremias Atrusti"

#Url a la que se enlazara con la donacion
URL_DONACION = "ayudanos.com"

# Numero maximo y minimo de lineas en el correo electronico
NUMERO_DE_LINEAS_MIN = 100
NUMERO_DE_LINEAS_MAX = 200

# En caso de que queramos que sea con un objetivo en concreto
NOMBRE_EMPRESA = "Perros sin casa"
IMAGEN_EMPRESA = "https://imgmedia.larepublica.pe/640x371/larepublica/original/2022/07/27/62e168ce1c95403984781dba.webp"
OBJETIVO_EMPRESA = "Eres una organizacion que busca ayudar a los perros callejeros"

# Numero de imagenes maximo en caso de generar automaticamente las empresas
NUMERO_DE_IMAGENES = 1
# Carpeta donde se guardaran las imagenes
CARPETA_IMAGENES = "imagenes/"


##### GENERACION DE CORREOS #####
GENERAR_CORREOS = False # En caso de querer generar los correos aleatoriamente

# if (GENERAR_CORREOS):
NUMERO_DE_CORREOS = 1000000 # Es aproximado al alza es decir nunca va ser menor que este numero 
TERMINACIONES_CORREOS = ["hotmail.com","yahoo.com","outlook.com","yahoo.co.uk","gmail.com"]
GUARDAR_EN_FICHERO = True

FICHERO_DIRECCION_CORREOS_GEUARDAR = 'correos_2.txt' # El lugar donde se van a guardar las direcciones de correos electronicos generadas
NUMERO_MAX_GENERADO_CHAT = 50 # Esta opcion sera la que diga el numero maximo de nombres y apellidos que el chat puede generar.

# else:
FICHERO_DIRECCION_CORREOS_ENVIAR = 'correos.txt'

# CLAVES DE API Y DE CORREO
CLAVE_API = "CLAVE-DE-LA-API-DE-OPENAI"
CLAVE_CORREO = "CLAVE-DE-TU-CORREO-ELECTRONICO"

import os

# Verifica si el directorio ya existe
if not os.path.exists(CARPETA_IMAGENES):
    os.makedirs(CARPETA_IMAGENES)
    print(f"Directorio '{CARPETA_IMAGENES}' creado.")


if not os.path.exists(FICHERO_DIRECCION_CORREOS_ENVIAR):
    print(f"\n\nERROR:\nEl archivo '{FICHERO_DIRECCION_CORREOS_ENVIAR}' no existe.\n")
    exit(-1)
